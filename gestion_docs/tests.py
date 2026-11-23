import shutil
import tempfile

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import DocumentMilitaire

MEDIA_TEMP = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TEMP)
class GedTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMP, ignore_errors=True)

    def setUp(self):
        self.agent = User.objects.create_user("agent", password="MotDePasse-Test-123")
        self.archiviste = User.objects.create_user("archiviste", password="MotDePasse-Test-123")
        self.archiviste.user_permissions.add(
            Permission.objects.get(codename="add_documentmilitaire")
        )
        self.officier = User.objects.create_user(
            "officier", password="MotDePasse-Test-123", is_staff=True
        )

    def creer_document(self, reference="OPS-001", classification="NON_PROTEGE"):
        return DocumentMilitaire.objects.create(
            reference=reference,
            titre="Ordre d'opération test",
            fichier=SimpleUploadedFile("ordre.pdf", b"%PDF-1.4 test"),
            classification=classification,
            categorie="ORDRE_OPERATION",
            unite_emettrice="1er BIR",
            signataire="Col. Test",
            officier_traitant=self.officier,
        )

    def formulaire(self, **extra):
        data = {
            "reference": "br-2026-01",
            "titre": "Bulletin de renseignement",
            "categorie": "BULLETIN_RENSEIGNEMENT",
            "classification": "SECRET_DEFENSE",
            "unite_emettrice": "DRM",
            "signataire": "Cdt. Test",
            "date_signature": "2026-11-20",
            "fichier": SimpleUploadedFile("br.pdf", b"%PDF-1.4 contenu"),
        }
        data.update(extra)
        return data

    # Connexion
    def test_accueil_redirige_vers_connexion(self):
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, reverse("login") + "?next=/")

    def test_page_connexion_accessible(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Se connecter")

    def test_connexion_agent_non_staff(self):
        response = self.client.post(
            reverse("login"), {"username": "agent", "password": "MotDePasse-Test-123"}
        )
        self.assertRedirects(response, reverse("index"))

    def test_mauvais_mot_de_passe(self):
        response = self.client.post(reverse("login"), {"username": "agent", "password": "faux"})
        self.assertContains(response, "incorrect")

    def test_deconnexion(self):
        self.client.force_login(self.agent)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    # Liste et recherche
    def test_liste_et_recherche(self):
        self.creer_document("OPS-001")
        self.creer_document("LOG-777")
        self.client.force_login(self.agent)
        response = self.client.get(reverse("index"), {"q": "log"})
        self.assertContains(response, "LOG-777")
        self.assertNotContains(response, "OPS-001")

    def test_bouton_ajout_selon_permission(self):
        self.client.force_login(self.agent)
        self.assertNotContains(self.client.get(reverse("index")), "Archiver un document")
        self.client.force_login(self.archiviste)
        self.assertContains(self.client.get(reverse("index")), "Archiver un document")

    # Ajout de documents
    def test_ajout_refuse_sans_permission(self):
        self.client.force_login(self.agent)
        response = self.client.post(reverse("ajouter_document"), self.formulaire())
        self.assertEqual(response.status_code, 403)
        self.assertFalse(DocumentMilitaire.objects.exists())

    def test_ajout_document(self):
        self.client.force_login(self.archiviste)
        response = self.client.post(reverse("ajouter_document"), self.formulaire())
        self.assertRedirects(response, reverse("index"))
        doc = DocumentMilitaire.objects.get()
        self.assertEqual(doc.reference, "BR-2026-01")
        self.assertEqual(doc.officier_traitant, self.archiviste)

    def test_ajout_extension_interdite(self):
        self.client.force_login(self.archiviste)
        data = self.formulaire(fichier=SimpleUploadedFile("virus.exe", b"MZ"))
        response = self.client.post(reverse("ajouter_document"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Format non autorisé")
        self.assertFalse(DocumentMilitaire.objects.exists())

    def test_ajout_reference_en_double(self):
        self.creer_document("BR-2026-01")
        self.client.force_login(self.archiviste)
        response = self.client.post(reverse("ajouter_document"), self.formulaire())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DocumentMilitaire.objects.count(), 1)

    # Accès aux fichiers
    def test_fichier_protege(self):
        doc = self.creer_document()
        url = reverse("telecharger_document", args=[doc.pk])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.agent)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"%PDF-1.4 test")

    def test_telechargement_reserve_au_personnel(self):
        doc = self.creer_document()
        url = reverse("telecharger_document", args=[doc.pk]) + "?telecharger=1"
        self.client.force_login(self.agent)
        self.assertNotIn("attachment", self.client.get(url)["Content-Disposition"])
        self.client.force_login(self.officier)
        self.assertIn("attachment", self.client.get(url)["Content-Disposition"])
