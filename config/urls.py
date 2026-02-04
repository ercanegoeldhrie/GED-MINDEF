from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gestion_docs.views import liste_documents # Importez la vue ici

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', liste_documents, name='index'), # L'adresse vide '' correspond à l'accueil
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)