from django import forms

from ArcheryApp.news.models import ClubNews, ClubAnnouncements

# Base form for announcements. Allowing inheritance for different purposes.
class NewsBaseForm(forms.ModelForm):
    class Meta:
        model = ClubNews
        labels = {
            'title': '',
            'news_text': '',
            'image': '',
            'is_active': 'Deactivate:',
            'author': 'News author',
        }
        help_texts = {
            'image': 'Please upload image (optional). Max size 5mb',
        }
        exclude = ['created_at']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'News Title',
                }
            ),
            'image': forms.FileInput(),
            'news_text': forms.Textarea(
                attrs={
                    'placeholder': 'News Text',
                }
            ),
        }

# Create news, inherits base form and disables author and is_active fields.
class CreateNewsForm(NewsBaseForm):
    class Meta(NewsBaseForm.Meta):
        exclude = ['author', 'is_active']

# News can be updated
class UpdateNewsForm(NewsBaseForm):
    class Meta(NewsBaseForm.Meta):
        pass

# Announcement base form, inherit for specific uses.
class AnnouncementBaseForm(forms.ModelForm):
    class Meta:
        model = ClubAnnouncements
        labels = {
            'title': '',
            'text': '',
        }
        help_texts = {
            'title': '',
            'text': ''
        }
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Announcement Title',
                }
            ),
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Announcement Text',
                }
            ),
        }


# Create new announcement
class CreateNewAnnouncementForm(AnnouncementBaseForm):
    class Meta(AnnouncementBaseForm.Meta):
        exclude = ['created_at', 'author', 'read_by']

# Update new announcement
class UpdateAnnouncementForm(AnnouncementBaseForm):
    class Meta(AnnouncementBaseForm.Meta):
        exclude = ['created_at', 'author', 'read_by']