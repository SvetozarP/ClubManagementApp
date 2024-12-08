from django import forms

from ArcheryApp.training.models import ShootSessionDetails

# Adding notes towards a shooting session - can record specific details like wind speed, what was the objective of
# the session, what was the outcome etc. Can be expanded further with Golden Records functionality.
class AddTrainingNotesForm(forms.ModelForm):
    class Meta:
        model = ShootSessionDetails
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'placeholder': 'Enter details...'}),
        }