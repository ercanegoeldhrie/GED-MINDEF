import os
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import DocumentMilitaire


def get_storage_size(path='media'):
    """Calcule la taille réelle occupée par les fichiers sur le serveur"""
    total_size = 0
    if os.path.exists(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)  # Taille en Mo


@login_required  # Force la connexion pour accéder au menu principal
def liste_documents(request):
    query = request.GET.get('q')
    documents = DocumentMilitaire.objects.all().order_by('-archive_le')

    # Moteur de recherche tactique
    if query:
        documents = documents.filter(
            Q(reference__icontains=query) | Q(titre__icontains=query)
        )

    # Données pour le tableau de bord
    stats = {
        'total': DocumentMilitaire.objects.count(),
        'secret': DocumentMilitaire.objects.filter(classification='SECRET_DEFENSE').count(),
        'poids_media': get_storage_size(),
        'version': "2.8.0-PRO"
    }

    return render(request, 'gestion_docs/index.html', {
        'documents': documents,
        'stats': stats
    })