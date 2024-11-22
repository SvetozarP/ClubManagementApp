from django import forms

from ArcheryApp.news.models import ClubNews, ClubAnnouncements


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


class CreateNewsForm(NewsBaseForm):
    class Meta(NewsBaseForm.Meta):
        exclude = ['author', 'is_active']


class UpdateNewsForm(NewsBaseForm):
    class Meta(NewsBaseForm.Meta):
        pass


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


class CreateNewAnnouncementForm(AnnouncementBaseForm):
    class Meta(AnnouncementBaseForm.Meta):
        exclude = ['created_at', 'author', 'read_by']


class UpdateAnnouncementForm(AnnouncementBaseForm):
    class Meta(AnnouncementBaseForm.Meta):
        exclude = ['created_at', 'author', 'read_by']