from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_("Nom / Entreprise"),
        widget=forms.TextInput(attrs={
            "placeholder": _("Votre nom / entreprise"),
            "class": "form-input"
        })
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            "placeholder": _("Votre email"),
            "class": "form-input"
        })
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "placeholder": _("Décrivez votre projet ou votre besoin"),
            "class": "form-textarea",
            "rows": 5
        })
    )

    # 🛑 Honeypot invisible
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput
    )
