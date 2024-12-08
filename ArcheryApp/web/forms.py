from django import forms

from ArcheryApp.web.models import HandleContactRequest

# captcha active in the deployed site
#from captcha.fields import ReCaptchaField
#from captcha.widgets import ReCaptchaV2Checkbox

# Collect information from public. Captcha is active in the deployed site
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))
 #   captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

# Answers to requests. is_staff can answer. Logic in ContactRequestDetailsView - record who answers, what the answer is
# and mark the request as answered.
class HandleContactRequestForm(forms.ModelForm):
    class Meta:
        model = HandleContactRequest
        fields = ['action_taken']
        widgets = {
            'action_taken': forms.Textarea(attrs={'placeholder': 'Enter your response here...'}),
        }