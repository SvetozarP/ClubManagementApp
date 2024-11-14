from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UserRegistrationForm, LoginForm, CompleteProfileForm
from .models import MemberProfile

class RegisterUserView(FormView):
    template_name = "membership/create-user.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("complete_profile")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        csrf_token = form.cleaned_data["csrf_token"]

        profile = MemberProfile.objects.get(email=email, csrf_token=csrf_token, is_registered=False)
        profile.is_registered = True
        profile.clear_csrf_token()
        profile.save()

        login(self.request, profile)
        return super().form_valid(form)


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid login credentials")
    else:
        form = LoginForm()
    return render(request, "membership/login.html", {"form": form})


class CompleteProfileView(LoginRequiredMixin, FormView):
    template_name = "membership/register.html"
    form_class = CompleteProfileForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile_completed:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data["username"]
        user.set_password(form.cleaned_data["password"])
        user.profile_completed = True  # Mark profile as completed
        user.save()

        update_session_auth_hash(self.request, user)

        messages.success(self.request, "Your profile has been completed successfully.")
        return super().form_valid(form)
