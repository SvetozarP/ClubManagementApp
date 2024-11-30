from django.test import TestCase
from django.urls import reverse
from ArcheryApp.membership.models import MemberProfile
from ArcheryApp.web.models import ContactRequest


class RequestResetTokenViewTest(TestCase):

    def setUp(self):
        # Create a MemberProfile for testing
        self.profile = MemberProfile.objects.create(
            email="testuser123@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            is_active=True
        )

        self.url = reverse('request-reset-token')  # Make sure the URL is correct

    def test_valid_email_submission(self):
        # Submit a valid email for the password reset request
        data = {'email': 'testuser123@example.com'}

        # Send the POST request
        response = self.client.post(self.url, data)

        # Ensure the reset token is generated
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.reset_token)

        # Ensure the reset token expiry is set
        self.assertIsNotNone(self.profile.reset_token_expiry)

        # Ensure the ContactRequest is created
        contact_request = ContactRequest.objects.get(email='testuser123@example.com')
        self.assertEqual(contact_request.message, f"Password reset token requested - {self.profile.reset_token}")

        # Ensure the user is redirected to the reset password page
        self.assertRedirects(response, reverse('reset-password'))

    def test_invalid_email_submission(self):
        # Submit a valid email for the password reset request
        data = {'email': 'testuser@example.com'}

        # Send the POST request
        response = self.client.post(self.url, data)

        # Ensure the reset token is generated
        self.profile.refresh_from_db()
        self.assertIsNone(self.profile.reset_token)

        # Ensure the reset token expiry is set
        self.assertIsNone(self.profile.reset_token_expiry)


    def test_multiple_reset_requests_within_hour(self):
        data = {'email': 'testuser123@example.com'}
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertContains(response, "You can only request a password reset once per hour.")
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.reset_token)
        self.assertIsNotNone(self.profile.reset_token_expiry)
        self.assertEqual(ContactRequest.objects.filter(email='testuser123@example.com').count(), 1)

    def test_successful_form_submission(self):
        data = {'email': 'testuser123@example.com'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('reset-password'))