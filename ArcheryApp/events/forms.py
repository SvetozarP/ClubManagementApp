from django import forms
from django.utils.timezone import make_aware

from ArcheryApp.events.models import ClubEvents


class EventBaseForm(forms.ModelForm):
    class Meta:
        model = ClubEvents
        labels = {
            'title': '',
            'start_date': '',
            'end_date': '',
            'image': '',
            'hosted_by': '',
            'event_description': '',
            'author': 'Event author:',
            'is_archived': 'Archive:',
        }
        help_texts = {
            'image': 'Please upload image (optional). Max size 5mb',
            'start_date': 'Please enter the start date and time',
            'end_date': 'Please enter the end date and time',
        }
        exclude = ['participants']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Event Title',
                }
            ),
            'start_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                }
            ),
            'end_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                }
            ),
            'image': forms.FileInput(),
            'hosted_by': forms.TextInput(
                attrs={
                    'placeholder': 'Event Host',
                }
            ),
            'event_description': forms.Textarea(
                attrs={
                    'placeholder': 'Event Description',
                }
            ),
        }


class CreateEventForm(EventBaseForm):
    class Meta(EventBaseForm.Meta):
        exclude = ['is_archived', 'author',]


class UpdateEventForm(EventBaseForm):
    class Meta(EventBaseForm.Meta):
        pass
