from pathlib import Path

from django import forms
from django.conf import settings

from .models import DocumentMilitaire

EXTENSIONS_AUTORISEES = {".pdf", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".jpg", ".jpeg", ".png", ".txt"}


class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentMilitaire
        fields = (
            "reference",
            "titre",
            "categorie",
            "classification",
            "unite_emettrice",
            "signataire",
            "date_signature",
            "fichier",
        )
        widgets = {
            "date_signature": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
        labels = {
            "reference": "Référence",
            "titre": "Objet",
            "categorie": "Catégorie",
            "unite_emettrice": "Unité émettrice",
            "date_signature": "Date de signature",
            "fichier": "Fichier",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs.setdefault("class", css)

    def clean_reference(self):
        return self.cleaned_data["reference"].strip().upper()

    def clean_fichier(self):
        fichier = self.cleaned_data["fichier"]
        extension = Path(fichier.name).suffix.lower()
        if extension not in EXTENSIONS_AUTORISEES:
            raise forms.ValidationError(
                "Format non autorisé. Formats acceptés : "
                + ", ".join(sorted(e.lstrip(".") for e in EXTENSIONS_AUTORISEES))
                + "."
            )
        limite = settings.GED_MAX_UPLOAD_MB * 1024 * 1024
        if fichier.size > limite:
            raise forms.ValidationError(
                f"Fichier trop lourd : {settings.GED_MAX_UPLOAD_MB} Mo maximum."
            )
        return fichier
