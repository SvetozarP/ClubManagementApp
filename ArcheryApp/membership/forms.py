from django import forms
from .models import MemberProfile

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    csrf_token = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = MemberProfile
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data

class MemberProfileCreationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)