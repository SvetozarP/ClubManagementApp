from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import UserRegistrationForm, LoginForm, CompleteProfileForm, MemberProfileCreationForm
from .models import MemberProfile
from ..events.models import ClubEvents
from ..news.models import ClubAnnouncements


class RegisterUserView(FormView):
    template_name = "membership/register.html"
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



class CreateUserView(UserPassesTestMixin, FormView):
    template_name = "membership/create-user.html"
    form_class = MemberProfileCreationForm
    success_url = reverse_lazy("create_user")  # Redirect back to the form on success

    # Only allow access to staff members
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")  # Redirect to login or another page if not authorized

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        # Check if the profile already exists
        if MemberProfile.objects.filter(email=email).exists():
            messages.error(self.request, "A profile with this email already exists.")
            return self.form_invalid(form)  # Re-render the form with errors
        else:
            # Create profile and generate CSRF token
            profile = MemberProfile(email=email)
            profile.generate_csrf_token()
            profile.save()
            messages.success(self.request, f"Profile created. CSRF token: {profile.csrf_token}")

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



class MemberProfileView(LoginRequiredMixin, TemplateView):
    template_name = "membership/profile.html"

    def get_context_data(self, **kwargs):
        next_week = datetime.now() + timedelta(days=7)
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        context['unread_announcements'] = ((ClubAnnouncements.objects
                                           .exclude(read_by__username=self.request.user.username))
                                           .order_by('-created_at'))
        context['upcoming_events'] = ClubEvents.objects.filter(end_date__lte=next_week)

        return context

def logout_view(request):
    logout(request)
    return redirect("home")