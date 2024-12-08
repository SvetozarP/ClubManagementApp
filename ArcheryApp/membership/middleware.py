from django.shortcuts import redirect
from django.urls import reverse

# We want user to complete their profile before using the website.
class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated and not request.user.profile_completed:

            if not request.path == reverse("complete-profile"):
                return redirect("complete-profile")
        return self.get_response(request)