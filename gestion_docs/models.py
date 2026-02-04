from django.db import models
from django.contrib.auth.models import User

class DocumentMilitaire(models.Model):
    CLASSIFICATION_CHOICES = [
        ('NON_PROTEGE', 'Non Protege'),
        ('DIFFUSION_RESTREINTE', 'Diffusion Restreinte'),
        ('CONFIDENTIEL_DEFENSE', 'Confidentiel Defense'),
        ('SECRET_DEFENSE', 'Secret Defense'),
    ]

    CATEGORIE_CHOICES = [
        ('ORDRE_OPERATION', 'Ordre Operation (OPORD)'),
        ('BULLETIN_RENSEIGNEMENT', 'Bulletin de Renseignement (BR)'),
        ('NOTE_EXPLICATIVE', 'Note Express'),
        ('FEUILLE_DE_ROUTE', 'Feuille de Route'),
        ('RAPPORT_MISSION', 'Rapport de Fin de Mission'),
    ]

    reference = models.CharField(max_length=100, unique=True)
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='mindef/archives/')
    classification = models.CharField(max_length=30, choices=CLASSIFICATION_CHOICES, default='NON_PROTEGE')
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)
    unite_emettrice = models.CharField(max_length=100)
    date_signature = models.DateField(null=True, blank=True)
    signataire = models.CharField(max_length=255)
    archive_le = models.DateTimeField(auto_now_add=True)
    officier_traitant = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Document Militaire"
        verbose_name_plural = "Archives de la Defense"

    def __str__(self):
        return f"[{self.reference}] - {self.titre}"