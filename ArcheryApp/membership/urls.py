from django.contrib.auth.views import LogoutView
from django.urls import path

from ArcheryApp.membership.views import RegisterUserView, CompleteProfileView, login_user, MemberProfileView, \
    logout_view, CreateUserView

urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register_user'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', MemberProfileView.as_view(), name='profile-view'),
]