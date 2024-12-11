from django.urls import path

from ArcheryApp.training.views import EditNotesView, DeleteNoteView

urlpatterns = [
    path('<int:pk>/edit/', EditNotesView.as_view(), name='edit-notes'),
    path('<int:pk>/delete/', DeleteNoteView.as_view(), name='delete-notes'),
]
