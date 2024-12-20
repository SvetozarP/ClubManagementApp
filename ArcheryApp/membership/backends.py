from django.contrib.auth.backends import ModelBackend
from ArcheryApp.membership.models import MemberProfile

# We have to be able to login with email or with username.
class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MemberProfile.objects.get(email=username) if '@' in username else (
                MemberProfile.objects.get(username=username))
        except MemberProfile.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user