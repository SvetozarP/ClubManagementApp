from django import forms

from ArcheryApp.fieldbookings.models import FieldBookings


class FieldBookingBaseForm(forms.ModelForm):
    class Meta:
        model = FieldBookings
        exclude = ['archer']


class CreateBookingForm(FieldBookingBaseForm):
    class Meta(FieldBookingBaseForm.Meta):
        exclude = ['archer']

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'time_from': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
            'time_to': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
        }


class UpdateBookingForm(FieldBookingBaseForm):
    class Meta(FieldBookingBaseForm.Meta):
        exclude = ['archer']

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'time_from': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
            'time_to': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
        }