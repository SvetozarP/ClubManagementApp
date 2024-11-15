from django.urls import path

from ArcheryApp.membership.views import RegisterUserView, CompleteProfileView, login_user

urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register_user'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('login/', login_user, name='login'),
]