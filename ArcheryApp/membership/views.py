from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UserRegistrationForm, MemberProfileCreationForm
from .models import MemberProfile

class CreateMemberProfileView(UserPassesTestMixin, FormView):
    template_name = "membership/create-user.html"
    form_class = MemberProfileCreationForm
    success_url = reverse_lazy("create_member_profile")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")

        if MemberProfile.objects.filter(email=email).exists():
            messages.error(self.request, "A profile with this email already exists.")
            return self.form_invalid(form)
        else:
            profile = MemberProfile(email=email, username=username)
            profile.generate_csrf_token()
            profile.save()
            messages.success(self.request, f"Profile created. CSRF token: {profile.csrf_token}")

        return super().form_valid(form)


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            csrf_token = form.cleaned_data["csrf_token"]

            try:
                profile = MemberProfile.objects.get(email=email, csrf_token=csrf_token, is_registered=False)
            except MemberProfile.DoesNotExist:
                form.add_error(None, "Invalid or expired CSRF token.")
                return render(request, "membership/register.html", {"form": form})

            profile.username = form.cleaned_data["username"]
            profile.set_password(form.cleaned_data["password"])
            profile.is_registered = True
            profile.clear_csrf_token()
            profile.save()

            login(request, profile)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "membership/register.html", {"form": form})