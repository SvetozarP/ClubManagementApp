from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated and not request.user.profile_completed:

            if not request.path == reverse("complete_profile"):
                return redirect("complete_profile")
        return self.get_response(request)