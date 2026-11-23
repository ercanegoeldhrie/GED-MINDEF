from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from gestion_docs import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.liste_documents, name="index"),
    path("documents/ajouter/", views.ajouter_document, name="ajouter_document"),
    path("documents/<int:pk>/fichier/", views.telecharger_document, name="telecharger_document"),
    path(
        "connexion/",
        auth_views.LoginView.as_view(
            template_name="gestion_docs/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
]

# Les fichiers de MEDIA_ROOT ne sont volontairement pas exposés ici :
# ils sont servis par la vue protégée "telecharger_document".
