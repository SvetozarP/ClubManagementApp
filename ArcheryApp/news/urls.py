from django.urls import path, include

from ArcheryApp.news.forms import UpdateAnnouncementForm
from ArcheryApp.news.views import NewsListView, NewsDetailView, PastNewsView, CreateNewsView, UpdateNewsView, \
    ClubAnnouncementView, CreateAnnouncementView, AnnouncementDetailView, AnnouncementUpdateView, DeleteAnnouncementView

urlpatterns = [
    path('', NewsListView.as_view(), name='club-news'),
    path('past-news/', PastNewsView.as_view(), name='club-past-news'),
    path('create/', CreateNewsView.as_view(), name='club-news-create'),
    path('<int:pk>/detail/', NewsDetailView.as_view(), name='club-news-detail'),
    path('<int:pk>/edit/', UpdateNewsView.as_view(), name='club-news-edit'),
    path('announcements/', ClubAnnouncementView.as_view(), name='club-announcements'),
    path('create-announcement/', CreateAnnouncementView.as_view(), name='create-club-announcements'),
    path('announcements/<int:pk>/', include([
        path('detail/', AnnouncementDetailView.as_view(), name='detail-club-announcements'),
        path('update/', AnnouncementUpdateView.as_view(), name='update-club-announcements'),
        path('delete/', DeleteAnnouncementView.as_view(), name='delete-club-announcements'),
    ])),
]
