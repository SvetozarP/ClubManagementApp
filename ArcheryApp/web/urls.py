from django.urls import path

from ArcheryApp.web.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
]
