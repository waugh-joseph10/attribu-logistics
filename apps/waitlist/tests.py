import json
from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import WaitlistEntry
from .tasks import send_admin_notification, send_confirmation_email


class WaitlistJoinViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("waitlist-join")

    def _post_json(self, data):
        return self.client.post(
            self.url,
            data=json.dumps(data),
            content_type="application/json",
        )

    @patch("apps.waitlist.views.send_admin_notification")
    @patch("apps.waitlist.views.send_confirmation_email")
    def test_valid_signup(self, mock_confirm, mock_admin):
        response = self._post_json({"email": "test@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "You're on the list."})
        self.assertTrue(WaitlistEntry.objects.filter(email="test@example.com").exists())
        mock_confirm.delay.assert_called_once_with("test@example.com")
        mock_admin.delay.assert_called_once_with("test@example.com")

    @patch("apps.waitlist.views.send_admin_notification")
    @patch("apps.waitlist.views.send_confirmation_email")
    def test_duplicate_email_returns_200(self, mock_confirm, mock_admin):
        WaitlistEntry.objects.create(email="existing@example.com")
        response = self._post_json({"email": "existing@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Already on the list."})
        mock_confirm.delay.assert_not_called()
        mock_admin.delay.assert_not_called()

    def test_invalid_email_format(self):
        response = self._post_json({"email": "notanemail"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_empty_email(self):
        response = self._post_json({"email": ""})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Email required."})

    def test_missing_email_key(self):
        response = self._post_json({})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Email required."})

    def test_malformed_json(self):
        response = self.client.post(
            self.url,
            data="not-json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request."})

    def test_get_method_rejected(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    @patch("apps.waitlist.views.send_admin_notification")
    @patch("apps.waitlist.views.send_confirmation_email")
    def test_email_normalized_to_lowercase(self, mock_confirm, mock_admin):
        response = self._post_json({"email": "USER@EXAMPLE.COM"})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(WaitlistEntry.objects.filter(email="user@example.com").exists())
        mock_confirm.delay.assert_called_once_with("user@example.com")

    @patch("apps.waitlist.views.send_admin_notification")
    @patch("apps.waitlist.views.send_confirmation_email")
    def test_email_whitespace_stripped(self, mock_confirm, mock_admin):
        response = self._post_json({"email": "  user@example.com  "})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(WaitlistEntry.objects.filter(email="user@example.com").exists())


class SendConfirmationEmailTaskTests(TestCase):
    @override_settings(
        RESEND_API_KEY="test_key",
        DEFAULT_FROM_EMAIL="noreply@attribu.io",
    )
    @patch("resend.Emails.send")
    def test_sends_to_correct_address(self, mock_send):
        send_confirmation_email("user@example.com")
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]
        self.assertEqual(call_args["to"], ["user@example.com"])

    @override_settings(
        RESEND_API_KEY="test_key",
        DEFAULT_FROM_EMAIL="noreply@attribu.io",
    )
    @patch("resend.Emails.send")
    def test_email_subject_and_content(self, mock_send):
        send_confirmation_email("user@example.com")
        call_args = mock_send.call_args[0][0]
        self.assertIn("waitlist", call_args["subject"].lower())
        self.assertIn("Attribu", call_args["text"])


class SendAdminNotificationTaskTests(TestCase):
    @override_settings(
        RESEND_API_KEY="test_key",
        DEFAULT_FROM_EMAIL="noreply@attribu.io",
        ADMIN_EMAIL="joe@attribu.io",
    )
    @patch("resend.Emails.send")
    def test_sends_to_admin(self, mock_send):
        send_admin_notification("user@example.com")
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]
        self.assertIn("joe@attribu.io", call_args["to"])

    @override_settings(
        RESEND_API_KEY="test_key",
        DEFAULT_FROM_EMAIL="noreply@attribu.io",
        ADMIN_EMAIL="joe@attribu.io",
    )
    @patch("resend.Emails.send")
    def test_includes_signup_email_in_body(self, mock_send):
        send_admin_notification("user@example.com")
        call_args = mock_send.call_args[0][0]
        self.assertIn("user@example.com", call_args["text"])
