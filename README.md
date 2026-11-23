# 🎖️ GED-MINDEF : Gestion Électronique des Documents
Système de gestion d'archives militaires développé avec **Django**.

## 🚀 Fonctionnalités
- Page de connexion dédiée (`/connexion/`) et déconnexion.
- Liste des archives avec recherche par référence, objet, signataire ou unité.
- Archivage d'un document depuis l'application (bouton « Archiver un document »), sans passer par l'admin.
  Formats acceptés : PDF, Word, ODT, Excel, images, texte ; 20 Mo maximum par défaut.
- Fichiers protégés : ils ne sont accessibles qu'aux utilisateurs connectés, le téléchargement est réservé au personnel (`is_staff`).
- Classification jusqu'à « Secret Défense » et tableau de bord (total, documents secrets, espace occupé).
- Lanceur automatisé pour Windows (`Lancer_GED.bat`).

## 👥 Droits
| Profil | Consulter | Archiver | Télécharger |
|---|---|---|---|
| Utilisateur connecté | ✅ | ❌ | ❌ |
| Utilisateur avec la permission « Can add Document Militaire » | ✅ | ✅ | ❌ |
| Personnel (`is_staff`) | ✅ | selon permission | ✅ |
| Superutilisateur | ✅ | ✅ | ✅ |

Les comptes et les permissions se gèrent dans l'admin Django (`/admin/`).

## 🛠️ Installation
1. Cloner le dépôt : `git clone https://github.com/ercanegoeldhrie/GED-MINDEF.git`
2. Créer l'environnement : `python -m venv venv` puis `venv\Scripts\activate`
3. Installer les dépendances : `pip install -r requirements.txt`
4. Copier `.env.example` en `.env` et le remplir :
   - `DJANGO_SECRET_KEY` : générer une clé avec
     `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DB_PASSWORD` : le mot de passe PostgreSQL (ou `DB_ENGINE=sqlite` pour une démo sans PostgreSQL).
5. Créer les tables et un compte : `python manage.py migrate` puis `python manage.py createsuperuser`
6. Lancer via le fichier `Lancer_GED.bat` (ou `python manage.py runserver`).

## ✅ Tests
```bash
python manage.py test gestion_docs
```
Avec `DB_ENGINE=sqlite` dans le `.env`, les tests tournent sans PostgreSQL.

## 🔒 Sécurité
Le fichier `.env` n'est jamais versionné. Sur un serveur : `DJANGO_DEBUG=False`, renseigner
`DJANGO_ALLOWED_HOSTS` et servir le site en HTTPS avec `DJANGO_SECURE_COOKIES=True`.
