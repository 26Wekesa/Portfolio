from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import ContactMessage


class PortfolioPagesTests(TestCase):
    def test_existing_pages_render(self):
        paths = [
            "/",
            "/about.html",
            "/resume.html",
            "/services.html",
            "/portfolio.html",
            "/contact.html",
            "/portfolio-details.html",
            "/service-details.html",
            "/starter-page.html",
        ]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="portfolio@example.com",
    CONTACT_RECIPIENT="owner@example.com",
)
class ContactMessageTests(TestCase):
    def test_valid_contact_submission_is_saved(self):
        response = self.client.post(
            reverse("contact_submit"),
            {
                "name": "A Client",
                "email": "client@example.com",
                "subject": "Website inquiry",
                "message": "I'd like to discuss a project.",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["owner@example.com"])
        self.assertEqual(mail.outbox[0].reply_to, ["client@example.com"])
        self.assertIn("I'd like to discuss a project.", mail.outbox[0].body)

    def test_invalid_contact_submission_is_rejected(self):
        response = self.client.post(
            reverse("contact_submit"),
            {
                "name": "A Client",
                "email": "not-an-email",
                "subject": "",
                "message": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_regular_submission_redirects_to_confirmation(self):
        response = self.client.post(
            reverse("contact_submit"),
            {
                "name": "A Client",
                "email": "client@example.com",
                "subject": "Website inquiry",
                "message": "I'd like to discuss a project.",
            },
        )

        self.assertRedirects(response, "/contact.html?sent=1")
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    @patch("core.views.EmailMessage.send", side_effect=OSError("SMTP unavailable"))
    def test_email_failure_keeps_message_and_reports_failure(self, send_email):
        response = self.client.post(
            reverse("contact_submit"),
            {
                "name": "A Client",
                "email": "client@example.com",
                "subject": "Website inquiry",
                "message": "I'd like to discuss a project.",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Your message was saved", status_code=503)
        self.assertEqual(ContactMessage.objects.count(), 1)
        send_email.assert_called_once_with(fail_silently=False)

    def test_submission_requires_csrf_token(self):
        csrf_client = self.client_class(enforce_csrf_checks=True)
        response = csrf_client.post(
            reverse("contact_submit"),
            {
                "name": "A Client",
                "email": "client@example.com",
                "subject": "Website inquiry",
                "message": "I'd like to discuss a project.",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_page_includes_csrf_token(self):
        response = self.client.get("/contact.html")

        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'action="/forms/contact/"')
