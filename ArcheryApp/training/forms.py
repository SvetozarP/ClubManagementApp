from django import forms

from ArcheryApp.training.models import ShootSessionDetails


class AddTrainingNotesForm(forms.ModelForm):
    class Meta:
        model = ShootSessionDetails
        fields = ['details']
        widgets = {
            'details': forms.Textarea(attrs={'placeholder': 'Enter details...'}),
        }