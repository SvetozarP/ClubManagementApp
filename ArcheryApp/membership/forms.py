from django import forms
from django.utils.timezone import now

from .models import MemberProfile

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
            }
        ),
        label=''
    )
    # csrf_token = forms.CharField(widget=forms.HiddenInput)
    csrf_token = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the token you have received',
            }
        ),
        label=''
    )

    class Meta:
        model = MemberProfile
        fields = ['email', 'csrf_token']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        csrf_token = cleaned_data.get("csrf_token")

        try:
            profile = MemberProfile.objects.get(email=email, csrf_token=csrf_token, is_registered=False)
        except MemberProfile.DoesNotExist:
            self.add_error(None, "Invalid or expired CSRF token.")
        return cleaned_data

class MemberProfileCreationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter new user email',
            }
        ),
        label=''
    )


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


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not MemberProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Please enter valid email.")
        return email


class PasswordResetForm(forms.Form):
    reset_token = forms.UUIDField()
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        reset_token = cleaned_data.get("reset_token")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # Validate token
        try:
            profile = MemberProfile.objects.get(reset_token=reset_token)
            if profile.reset_token_expiry < now():
                raise forms.ValidationError("Reset token has expired.")
        except MemberProfile.DoesNotExist:
            raise forms.ValidationError("Invalid reset token.")
        return cleaned_data