from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView, TemplateView, UpdateView, ListView

from ArcheryApp.fieldbookings.models import FieldBookings
from ArcheryApp.membership.forms import UserRegistrationForm, LoginForm, CompleteProfileForm, MemberProfileCreationForm, \
    PasswordResetRequestForm, PasswordResetForm, UserEditProfileForm, StaffEditProfileForm
from ArcheryApp.membership.models import MemberProfile
from ArcheryApp.events.models import ClubEvents
from ArcheryApp.news.models import ClubAnnouncements
from ArcheryApp.training.models import ShootSessionDetails
from ArcheryApp.web.models import ContactRequest


class RegisterUserView(FormView):
    template_name = "membership/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("complete-profile")

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
    template_name = "membership/create.html"
    form_class = MemberProfileCreationForm
    success_url = reverse_lazy("create-user")

    # Only allow access to staff members
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_user'] = True
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone = form.cleaned_data.get("phone_number")
        address = form.cleaned_data.get("address")

        # Check if the profile already exists
        if MemberProfile.objects.filter(email=email).exists():
            messages.error(self.request, "A profile with this email already exists.")
            return self.form_invalid(form)  # Re-render the form with errors
        else:
            # Create profile and generate CSRF token
            profile = MemberProfile(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                address=address,
            )
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

        if not request.user.is_authenticated:
            return redirect("home")

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

        # messages.success(self.request, "Your profile has been completed successfully.")
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
        context['field_bookings'] = FieldBookings.objects.filter(Q(archer=self.request.user) & Q(date__lte=next_week))
        context['contact_requests'] = ContactRequest.objects.filter(is_answered=False)
        context['session_details'] = (ShootSessionDetails.objects.filter(archer=self.request.user)
                                        .order_by('-shoot_session__date')[:5])

        return context

def logout_view(request):
    logout(request)
    return redirect("home")


class RequestResetTokenView(FormView):
    template_name = "membership/request_reset_token.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("reset-password")

    def form_valid(self, form):
        email = form.cleaned_data['email']
        profile = MemberProfile.objects.get(email=email)

        # Check if the user has requested a reset in the past hour
        if profile.last_reset_request and profile.last_reset_request > now() - timedelta(hours=1):
            messages.error(self.request, "You can only request a password reset once per hour.")
            return self.form_invalid(form)

        # Generate reset token
        profile.generate_reset_token()

        ContactRequest.objects.create(
            name=f"{profile.first_name} {profile.last_name}" if profile.first_name and profile.last_name else "N/A",
            email=profile.email,
            message=f"Password reset token requested - {profile.reset_token}",
        )


        # # Inform the user
        # messages.success(
        #     self.request,
        #     f"Your password reset token is: {profile.reset_token}. Use it within 1 hour."
        # )
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

        # messages.success(self.request, "Your password has been reset. You can now log in.")
        return super().form_valid(form)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = MemberProfile
    form_class = UserEditProfileForm
    template_name = 'membership/edit_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('staff-edit-profile', pk=self.request.user.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, **args):
        return self.request.user

    def form_valid(self, form):
        form.save()

        password = form.cleaned_data.get('password')
        if password:
            self.request.user.set_password(password)
            self.request.user.save()
            update_session_auth_hash(self.request, self.request.user)

        return redirect('profile')

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_user'] = True
        return context


class StaffEditProfileView(PermissionRequiredMixin, UpdateView):
    model = MemberProfile
    form_class = StaffEditProfileForm
    template_name = 'membership/edit_profile.html'
    permission_required = 'auth.change_user'

    def form_valid(self, form):
        form.save()
        # messages.success(self.request, "Profile updated successfully.")
        return redirect('profile-view')

    def post(self, request, *args, **kwargs):
        if 'generate_reset_token' in request.POST:
            profile = self.get_object()
            try:
                profile.generate_reset_token()
                messages.success(request, f"Reset token generated: {profile.reset_token}")
            except Exception as e:
                messages.error(request, str(e))

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_user'] = True
        return context


class MembersListView(UserPassesTestMixin, ListView):
    model = MemberProfile
    template_name = 'membership/members_list.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def get_queryset(self):
        return MemberProfile.objects.filter(Q(is_superuser=False) & Q(is_staff=False))