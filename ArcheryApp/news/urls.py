from django.urls import path

from ArcheryApp.news.views import NewsListView, NewsDetailView, PastNewsView

urlpatterns = [
    path('', NewsListView.as_view(), name='club-news'),
    path('past-news/', PastNewsView.as_view(), name='club-past-news'),
    path('<int:pk>/detail/', NewsDetailView.as_view(), name='club-news-detail'),
]
