from django.test import TestCase
from django.urls import reverse


from django.contrib import messages

from ArcheryApp.membership.models import MemberProfile


class StaffEditProfileViewTest(TestCase):

    def setUp(self):

        # Create a member profile for the staff user
        self.staff_user = MemberProfile.objects.create(
            email="staffuser@example.com",
            username="staffuser",
            password='dkfjadlkf@KJ34lkj',
            first_name="Staff",
            last_name="User",
            is_staff=True,
            profile_completed=True
        )

        # Create a member profile for the regular user
        self.regular_user = MemberProfile.objects.create(
            email="nonstaffuser@example.com",
            username="nonstaffuser",
            password='dkfjadlkf@KJ34lkj',
            first_name="nonStaff",
            last_name="nonUser",
            is_staff=False,
            profile_completed=True
        )

        self.url = reverse('staff-edit-profile', args=[self.regular_user.pk])

    def test_staff_user_access(self):
        # Log in as staff user and access the edit profile page
        self.client.login(username='staffuser', password='dkfjadlkf@KJ34lkj')
        response = self.client.get(self.url)

        # Ensure the response is a 200 (OK) status code
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_access(self):
        # Log in as a regular user and try to access the edit profile page
        self.client.login(username='nonstaffuser', password='dkfjadlkf@KJ34lkj')
        response = self.client.get(self.url)

        # Ensure the response redirects to the login page
        self.assertRedirects(response, reverse('login'))