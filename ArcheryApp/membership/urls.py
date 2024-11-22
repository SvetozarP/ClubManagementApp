from django.contrib.auth.views import LogoutView
from django.urls import path

from ArcheryApp.membership.views import RegisterUserView, CompleteProfileView, MemberProfileView, \
    logout_view, CreateUserView, LoginUserView, RequestResetTokenView, PasswordResetView, EditProfileView, \
    StaffEditProfileView, MembersListView

urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register-user'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete-profile'),
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', MemberProfileView.as_view(), name='profile-view'),
    path('request-reset-token/', RequestResetTokenView.as_view(), name="request-reset-token"),
    path('reset-password/', PasswordResetView.as_view(), name="reset-password"),
    path('edit/', EditProfileView.as_view(), name="edit-profile"),
    path('<int:pk>/edit/', StaffEditProfileView.as_view(), name="staff-edit-profile"),
    path('list/', MembersListView.as_view(), name="members-list"),
]
