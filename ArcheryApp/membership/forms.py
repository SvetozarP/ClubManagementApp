from django import forms
from .models import MemberProfile

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    csrf_token = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = MemberProfile
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        csrf_token = cleaned_data.get("csrf_token")

        try:
            profile = MemberProfile.objects.get(email=email, csrf_token=csrf_token, is_registered=False)
        except MemberProfile.DoesNotExist:
            self.add_error(None, "Invalid or expired CSRF token.")
        return cleaned_data


class CompleteProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = MemberProfile
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)