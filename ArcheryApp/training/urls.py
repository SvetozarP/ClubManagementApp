from django.urls import path

from ArcheryApp.training.views import training

urlpatterns = [
    path('', training, name='training'),
]
