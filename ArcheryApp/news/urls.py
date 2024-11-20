from django.urls import path

from ArcheryApp.news.views import NewsListView, NewsDetailView, PastNewsView, CreateNewsView, UpdateNewsView

urlpatterns = [
    path('', NewsListView.as_view(), name='club-news'),
    path('past-news/', PastNewsView.as_view(), name='club-past-news'),
    path('create/', CreateNewsView.as_view(), name='club-news-create'),
    path('<int:pk>/detail/', NewsDetailView.as_view(), name='club-news-detail'),
    path('<int:pk>/edit/', UpdateNewsView.as_view(), name='club-news-edit'),
]
