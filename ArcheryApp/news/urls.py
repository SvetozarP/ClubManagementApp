from django.urls import path

from ArcheryApp.news.views import club_news


urlpatterns = [
    path('', club_news, name='news'),
]
