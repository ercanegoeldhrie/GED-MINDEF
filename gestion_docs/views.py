import os
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentForm
from .models import DocumentMilitaire

VERSION = "2.9.0-PRO"


def get_storage_size(path=None):
    """Calcule la taille réelle occupée par les fichiers sur le serveur (en Mo)."""
    path = path or settings.MEDIA_ROOT
    total_size = 0
    if os.path.exists(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)


@login_required  # Force la connexion pour accéder au menu principal
def liste_documents(request):
    query = request.GET.get("q", "").strip()
    documents = DocumentMilitaire.objects.select_related("officier_traitant").order_by("-archive_le")

    # Moteur de recherche tactique
    if query:
        documents = documents.filter(
            Q(reference__icontains=query)
            | Q(titre__icontains=query)
            | Q(signataire__icontains=query)
            | Q(unite_emettrice__icontains=query)
        )

    # Données pour le tableau de bord
    stats = {
        "total": DocumentMilitaire.objects.count(),
        "secret": DocumentMilitaire.objects.filter(classification="SECRET_DEFENSE").count(),
        "poids_media": get_storage_size(),
        "version": VERSION,
    }

    return render(
        request,
        "gestion_docs/index.html",
        {"documents": documents, "stats": stats, "query": query},
    )


@login_required
@permission_required("gestion_docs.add_documentmilitaire", raise_exception=True)
def ajouter_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.officier_traitant = request.user
            document.save()
            messages.success(request, f"Document {document.reference} archivé avec succès.")
            return redirect("index")
    else:
        form = DocumentForm()
    return render(request, "gestion_docs/ajouter.html", {"form": form})


@login_required
def telecharger_document(request, pk):
    """Sert un fichier uniquement à un utilisateur connecté.
    Consultation dans le navigateur pour tous, téléchargement réservé au personnel."""
    document = get_object_or_404(DocumentMilitaire, pk=pk)
    if not document.fichier:
        raise Http404("Aucun fichier attaché.")
    try:
        fichier = document.fichier.open("rb")
    except FileNotFoundError:
        raise Http404("Fichier introuvable sur le serveur.")
    as_attachment = request.GET.get("telecharger") == "1" and request.user.is_staff
    return FileResponse(
        fichier,
        as_attachment=as_attachment,
        filename=Path(document.fichier.name).name,
    )
