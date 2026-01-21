from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch
import time
from django import forms

class ContactFormTests(TestCase):

    def setUp(self): # Set up the test client and URL
        self.client = Client()
        self.url = reverse("contact")

    @patch("app.views.sib_api_v3_sdk.TransactionalEmailsApi.send_transac_email")
    def test_valid_message_succeeds(self, mock_send): # Test that a valid message is sent successfully
        response = self.client.post(self.url, {
            "name": "Michael",
            "email": "test@example.com",
            "message": "Ceci est un message valide de plus de 10 caractères.",
            "website": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message envoyé avec succès")
        mock_send.assert_called_once()

    def test_message_too_short_is_rejected(self): # Test that a too short message is rejected
        response = self.client.post(self.url, {
            "name": "Michael",
            "email": "test@example.com",
            "message": "Hi",
            "website": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "message est trop court")

    def test_email_header_injection_is_blocked(self): # Test that email header injection is blocked
        response = self.client.post(self.url, {
            "name": "Michael",
            "email": "test@example.com\nBCC:evil@test.com",
            "message": "Message valide mais email invalide.",
            "website": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address")

    def test_honeypot_blocks_bot(self): # Test that the honeypot field blocks bot submissions
        response = self.client.post(self.url, {
            "name": "Bot",
            "email": "bot@test.com",
            "message": "Je suis un bot mais je parle beaucoup.",
            "website": "http://spam.com"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Une erreur est survenue. Envoi non effectué.")

    @patch("app.views.sib_api_v3_sdk.TransactionalEmailsApi.send_transac_email")
    def test_rate_limit_blocks_fast_resend(self, mock_send): # Test that rate limiting blocks rapid resubmissions
        # Initialisation de session
        self.client.get(self.url)

        session = self.client.session
        session["last_contact_time"] = time.time()
        session.save()

        response = self.client.post(self.url, {
            "name": "Michael",
            "email": "test@example.com",
            "message": "Encore un message valide.",
            "website": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Veuillez attendre quelques secondes avant un nouvel envoi.")
        mock_send.assert_not_called()

    @patch("app.views.sib_api_v3_sdk.TransactionalEmailsApi.send_transac_email")
    def test_email_not_sent_on_form_error(self, mock_send):
        self.client.post(self.url, {
            "name": "",
            "email": "bad",
            "message": "Hi",
            "website": ""
        })

        mock_send.assert_not_called()
