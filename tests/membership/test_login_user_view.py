from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden
from datetime import timedelta
from django.utils.timezone import now

class LoginUserViewTest(TestCase):

    def setUp(self):
        # Create a user profile for testing
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="validpassword",
            username="testuser"
        )
        self.url = reverse('login')  # Replace with the correct URL name

    def test_successful_login(self):
        # Send a POST request with valid credentials
        data = {'username': 'testuser', 'password': 'validpassword'}
        response = self.client.post(self.url, data)

        # Check that the user is redirected on successful login
        self.assertEqual(response.status_code, 302)

        # Check that the user is logged in
        user = authenticate(username='testuser', password='validpassword')
        self.assertEqual(self.client.session['_auth_user_id'], str(user.id))

    def test_invalid_login(self):
        # Send a POST request with invalid credentials
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)

        # Check that the form is invalid and the error message is added
        self.assertContains(response, "Invalid login credentials")

    def test_too_many_failed_login_attempts(self):
        # Simulate multiple failed login attempts within 15 minutes
        data = {'username': 'testuser', 'password': 'wrongpassword'}

        for _ in range(5):  # Attempt 5 failed logins
            self.client.post(self.url, data)

        # Send one more invalid login attempt
        response = self.client.post(self.url, data)

        # Check for a forbidden response due to too many failed attempts
        self.assertEqual(response.status_code, 403)
