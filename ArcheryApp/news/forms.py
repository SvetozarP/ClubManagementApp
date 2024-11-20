from django import forms

from ArcheryApp.news.models import ClubNews


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
