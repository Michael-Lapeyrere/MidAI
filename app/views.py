from django.shortcuts import render, redirect
from .forms import ContactForm
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import logging
import time
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

def home(request):
    return render(request, "home.html")

def go_home(request):
    url_home = reverse('home')  # 'home' = le name dans urls.py
    return redirect(url_home) 

def projects(request):
    return render(request, 'projects.html')

def project_vision(request):
    return render(request, "projects/vision.html")

def project_newsletter(request):
    return render(request, "projects/newsletter.html")

def project_midai(request):
    return render(request, "projects/midai.html")

def about(request):
    return render(request, "about.html")

logger = logging.getLogger("contact")

def contact(request):
    # 🕒 Rate limit simple par session (30 secondes)
    last_sent = request.session.get("last_contact_time")
    now = time.time()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if last_sent and now - last_sent < 30:
            form.add_error(
                    "message",
                    _("Veuillez attendre quelques secondes avant un nouvel envoi.")
                )
            return render(
                    request,
                    "contact.html",
                    {
                        "form": form,
                        "success": False
                    }
                )
        
        # Honeypot (bot)

        if request.POST.get("website"):  # ou form.data.get("website")
            form.add_error(
                "message",
                _("Une erreur est survenue lors de l'envoi du message.")
            )
            return render(
                request,
                "contact.html",
                {
                    "form": form,
                    "success": False
                }
            )


        if form.is_valid():

            # Données
            name = form.cleaned_data["name"].strip()
            email = form.cleaned_data["email"].strip()
            message = form.cleaned_data["message"].strip()

            # Validations serveur
            if len(message) < 10:
                form.add_error(
                    "message",
                    _("Le message est trop court (minimum 10 caractères).")
                )
                return render(
                    request,
                    "contact.html",
                    {
                        "form": form,
                        "success": False
                    }
                )

            if "\n" in email or "\r" in email:
                form.add_error(
                    "message",
                    _("Adresse email invalide.")
                )
                return render(
                    request,
                    "contact.html",
                    {
                        "form": form,
                        "success": False
                    }
                )

            # Config Brevo
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key["api-key"] = settings.BREVO_API_KEY
            configuration.timeout = 5

            api_client = sib_api_v3_sdk.ApiClient(configuration)
            email_api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

            # Mail transactionnel
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{
                    "email": settings.CONTACT_EMAIL,
                    "name": "Michael"
                }],
                sender={
                    "email": settings.CONTACT_EMAIL,
                    "name": "MidAi"
                },
                reply_to={
                    "email": email,
                    "name": name
                },
                subject="Nouveau message depuis le site",
                html_content=f"""
                    <h2>Nouveau message reçu :</h2>
                    <p><b>Nom :</b> {name}</p>
                    <p><b>Email :</b> {email}</p>
                    <p><b>Message :</b><br>{message}</p>
                """
            )

            try:
                email_api.send_transac_email(send_smtp_email)

                # Met à jour le rate limit
                request.session["last_contact_time"] = now

                return render(
                    request,
                    "contact.html",
                    {
                        "form": ContactForm(),
                        "success": True
                    }
                )

            except ApiException as e:
                logger.warning("Brevo error", extra={"error": str(e)})
                form.add_error(
                    "message",
                    _("Une erreur est survenue lors de l'envoi du message. Veuillez réessayer plus tard.")
                )
                return render(
                    request,
                    "contact.html",
                    {
                        "form": form,
                        "success": False
                    }
                )

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form, "success": False})