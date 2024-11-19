from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView, TemplateView

from .forms import UserRegistrationForm, LoginForm, CompleteProfileForm, MemberProfileCreationForm, \
    PasswordResetRequestForm, PasswordResetForm
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

# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 form.add_error(None, "Invalid login credentials")
#     else:
#         form = LoginForm()
#     return render(request, "membership/login.html", {"form": form})


class LoginUserView(FormView):
    template_name = "membership/login.html"
    form_class = LoginForm
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        # Initialize login attempt tracking
        if "login_attempts" not in request.session:
            request.session["login_attempts"] = {}

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        # Check for exceeded login attempts
        client_ip = request.META.get("REMOTE_ADDR")
        attempts = request.session["login_attempts"].get(client_ip, [])
        limit_window = now() - timedelta(minutes=15)

        # Convert string timestamps back to datetime for comparison
        recent_attempts = [
            datetime.fromisoformat(attempt) for attempt in attempts if datetime.fromisoformat(attempt) > limit_window
        ]

        # If exceeded the limit, return forbidden response
        if len(recent_attempts) >= 5:
            return HttpResponseForbidden("Too many failed login attempts. Try again later.")

        user = authenticate(request, username=username, password=password)
        if user:
            # Reset attempts on successful login
            request.session["login_attempts"].pop(client_ip, None)
            login(request, user)
            return redirect(self.get_success_url())
        else:
            # Track failed login attempt
            recent_attempts.append(now())
            # Convert datetime objects to ISO format before storing
            request.session["login_attempts"][client_ip] = [attempt.isoformat() for attempt in recent_attempts]
            request.session.modified = True
            form.add_error(None, "Invalid login credentials")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


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


class RequestResetTokenView(FormView):
    template_name = "membership/request_reset_token.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("reset_password")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        profile = MemberProfile.objects.get(email=email)

        # Check if the user has requested a reset in the past hour
        if profile.last_reset_request and profile.last_reset_request > now() - timedelta(hours=1):
            messages.error(self.request, "You can only request a password reset once per hour.")
            return self.form_invalid(form)

        # Generate reset token
        profile.generate_reset_token()

        # Inform the user
        messages.success(
            self.request,
            f"Your password reset token is: {profile.reset_token}. Use it within 1 hour."
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "membership/reset_password.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        reset_token = form.cleaned_data['reset_token']
        new_password = form.cleaned_data['new_password']

        # Update the user's password and clear the reset token
        profile = MemberProfile.objects.get(reset_token=reset_token)
        profile.set_password(new_password)
        profile.clear_reset_token()

        messages.success(self.request, "Your password has been reset. You can now log in.")
        return super().form_valid(form)