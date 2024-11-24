from django import forms
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from ArcheryApp.common.validators import ArcheryAppPasswordValidator

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
        label='',
    )
    first_name = forms.CharField(
        max_length=MemberProfile.NAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter first name',
            }
        ),
        label='',
    )
    last_name = forms.CharField(
        max_length=MemberProfile.NAME_MAX_LEN,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter last name',
            }
        ),
        label='',
    )
    phone_number = forms.CharField(
        max_length=MemberProfile.MAX_PHONE_NO_LEN,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter phone number',
            }
        ),
        label='',
    )
    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':3,
                'cols':50,
                'placeholder': 'Enter address',
            }

        ),
        label='',
    )


# class CompleteProfileForm(forms.ModelForm):
#     username = forms.CharField(
#         max_length=150,
#     )
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
#
#     class Meta:
#         model = MemberProfile
#         fields = ['username', 'password']
#         help_texts = {
#             'username': 'Username must be between 5 and 150 characters.',
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if password and confirm_password and password != confirm_password:
#             self.add_error("confirm_password", "Passwords do not match.")
#
#         return cleaned_data

class CompleteProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text='<p class="guidance">Username must be between 5 and 150 characters.</p>',
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter new username',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password',
            }
        ),
        help_text='<p class="guidance">Password must be at least 10 characters long</p> '
                  '<p class="guidance">Must contain one special character</p> '
                  '<p class="guidance">One uppercase character</p> '
                  '<p class="guidance">One digit</p>'
                  '<p class="guidance">Must not be like your username</p>'
                  '<p class="guidance">Must not be a dictionary word.</p>',
        label='',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
            }
        ),
        label="",
    )

    class Meta:
        model = MemberProfile
        fields = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        try:
            ArcheryAppPasswordValidator().validate(password, user=None)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

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
    reset_token = forms.UUIDField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the token you received',
            }
        )
    )
    # new_password = forms.CharField(widget=forms.PasswordInput())
    # confirm_password = forms.CharField(widget=forms.PasswordInput())

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password',
            }
        ),
        help_text='<p class="guidance">Password must be at least 10 characters long</p> '
                  '<p class="guidance">Must contain one special character</p> '
                  '<p class="guidance">One uppercase character</p> '
                  '<p class="guidance">One digit</p>'
                  '<p class="guidance">Must not be like your username</p>'
                  '<p class="guidance">Must not be a dictionary word.</p>',
        label='',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
            }
        ),
        label="",
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        try:
            ArcheryAppPasswordValidator().validate(new_password, user=None)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        reset_token = cleaned_data.get("reset_token")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        # Validate token
        try:
            profile = MemberProfile.objects.get(reset_token=reset_token)
            if profile.reset_token_expiry < now():
                raise forms.ValidationError("Reset token has expired.")
        except MemberProfile.DoesNotExist:
            raise forms.ValidationError("Invalid reset token.")
        return cleaned_data


class UserEditProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New Password'}
        ),
        required=False,
        help_text='<p class="guidance">Leave blank if you do not want to change your password.</p>'
                  '<p class="guidance">Password must be at least 10 characters long</p> '
                  '<p class="guidance">Must contain one special character</p> '
                  '<p class="guidance">One uppercase character</p> '
                  '<p class="guidance">One digit</p>'
                  '<p class="guidance">Must not be like your username</p>'
                  '<p class="guidance">Must not be a dictionary word.</p>',
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm New Password'}
        ),
        required=False,
    )

    class Meta:
        model = MemberProfile
        fields = ['image', 'phone_number', 'address']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        try:
            ArcheryAppPasswordValidator().validate(password, user=None)
        except ValidationError as e:
            raise ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class StaffEditProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = [
            'first_name', 'last_name', 'username',
            'phone_number', 'address',
            'is_active', 'image'
        ]

