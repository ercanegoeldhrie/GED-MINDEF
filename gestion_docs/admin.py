from django.contrib import admin
from .models import DocumentMilitaire


@admin.register(DocumentMilitaire)
class DocumentMilitaireAdmin(admin.ModelAdmin):
    # Les colonnes qui seront affichées dans la liste
    list_display = ('reference', 'titre', 'classification', 'categorie', 'unite_emettrice', 'date_signature')

    # La barre de recherche (recherche sur la référence, le titre et le signataire)
    search_fields = ('reference', 'titre', 'signataire')

    # Les filtres rapides sur le côté droit
    list_filter = ('classification', 'categorie', 'unite_emettrice', 'date_signature')

    # Organisation du formulaire d'ajout pour plus de clarté
    fieldsets = (
        ('Identification du Document', {
            'fields': ('reference', 'titre', 'categorie')
        }),
        ('Sécurité et Confidentialité', {
            'fields': ('classification', 'officier_traitant')
        }),
        ('Fichier et Origine', {
            'fields': ('fichier', 'unite_emettrice', 'signataire', 'date_signature')
        }),
    )