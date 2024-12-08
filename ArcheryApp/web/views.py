from datetime import date

from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from ArcheryApp.events.models import ClubEvents
from ArcheryApp.fieldbookings.models import FieldBookings
from ArcheryApp.news.models import ClubNews
from ArcheryApp.web.forms import ContactForm, HandleContactRequestForm
from ArcheryApp.web.models import ClubMission, Testimonials, ClubHistory, MembershipInfo, ContactRequest, \
    HandleContactRequest


# Create your views here.

# IndexView - collects data from mission, events, news, shooting sessions and testimonials and passes them to the main template
class IndexView(TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['mission'] = ClubMission.objects.first()
        context['events'] = ClubEvents.objects.filter(Q(end_date__gte=date.today()) & Q(is_archived=False)).order_by('-created_at')[:3]
        context['news'] = ClubNews.objects.filter(is_active=True).order_by('-created_at')[:3]
        context['archers_shooting'] = FieldBookings.objects.filter(date=date.today()).count()
        context['testimonials'] = Testimonials.objects.all()

        return context

# Club History - ListView which simply displays entries for club history. Used to get better formatting in the template
class HistoryList(ListView):
    model = ClubHistory
    template_name = 'web/history.html'


# This is only the front page where users are told how to become members.
class MembershipDetailsView(TemplateView):
    template_name = 'membership/membership.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['membership_info'] = MembershipInfo.objects.first()

        return context

# contact us form. Not working with Celery / Redis currently. This can be added as additional logic.
async def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            await sync_to_async(ContactRequest.objects.create)(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    form = ContactForm()
    return render(request, 'web/contact_us.html', {'form': form})

# Async view for staff to see submissions - All contact requests are saved in the database. Response to requests is recorded (action taken)
# Only is_staff users can see contact requests and answer contact_requests. This is visible in the profile page for is_staff users
@user_passes_test(lambda u: u.is_staff)
async def contact_requests(request):
    contact_requests = await sync_to_async(list)(ContactRequest.objects.all())
    return render(request, 'membership/profile.html', {'contact_requests': contact_requests})

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

# is_staff users can see contact requests and answer contact_requests. Answers are recorded as one-to-one with the request.
class ContactRequestDetailsView(UserPassesTestMixin, FormMixin, DetailView):
    model = ContactRequest
    fields = ['name', 'email', 'message']
    template_name = 'membership/contact_us_detail.html'
    form_class = HandleContactRequestForm

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():

            handle_request = form.save(commit=False)
            handle_request.action_by = request.user
            handle_request.contact_request = self.object
            handle_request.save()

            self.object.is_answered = True
            self.object.save()

            messages.success(request, "Your response has been recorded.")
            return redirect("contact-us-detail", pk=self.object.pk)
        else:
            messages.error(request, "There was an error with your submission.")
            return self.form_invalid(form)