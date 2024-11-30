from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import datetime, timedelta
import pytz

from ArcheryApp.events.models import ClubEvents
from ArcheryApp.membership.models import MemberProfile


class CreateNewEventViewTest(TestCase):
    #Arrange
    def setUp(self):
        # Create a staff user
        self.staff_user = MemberProfile.objects.create_user(
            email='staffuser@staff.com', username='staffuser', password='dlfkjLKJdlkfj@lkjlkj88', is_staff=True, profile_completed=True)
        self.client.login(username='staffuser', password='dlfkjLKJdlkfj@lkjlkj88')

    def test_create_new_event_success(self):
        # Ensure the user is a staff member - arrange
        self.assertTrue(self.staff_user.is_staff)

        # Create a new event - arrange
        data = {
            'title': 'New Club Event',
            'start_date': datetime.now(pytz.UTC),
            'end_date': datetime.now(pytz.UTC) + timedelta(days=1),
            'event_description': 'This is a new event for the club.'
        }

        # Post the data to create the event - Act
        response = self.client.post(reverse('club-create-event'), data)

        # Check that the response redirects to the event list - Assert
        self.assertRedirects(response, reverse('club-events'))

        # Check that the event was created - Assert
        self.assertTrue(ClubEvents.objects.filter(title="New Club Event").exists())

    def test_create_new_event_no_permission(self):
        # Create a non-staff user and login - Arrange
        non_staff_user = MemberProfile.objects.create_user(email='user@user.com', username='user', password='password', profile_completed=True)
        self.client.login(username='user', password='password')

        # Try to access the create event view - Act
        response = self.client.get(reverse('club-create-event'))

        # Check if the response redirects to the login page or permission page - Assert
        self.assertRedirects(response, reverse('login'))
