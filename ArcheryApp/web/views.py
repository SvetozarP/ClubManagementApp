from datetime import date

from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from ArcheryApp.events.models import ClubEvents
from ArcheryApp.fieldbookings.models import FieldBookings
from ArcheryApp.news.models import ClubNews
from ArcheryApp.web.forms import ContactForm
from ArcheryApp.web.models import ClubMission, Testimonials, ClubHistory, MembershipInfo, ContactRequest


# Create your views here.
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

class HistoryList(ListView):
    model = ClubHistory
    template_name = 'web/history.html'


class MembershipDetailsView(TemplateView):
    template_name = 'membership/membership.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['membership_info'] = MembershipInfo.objects.first()

        return context


class NewsListView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubNews.objects.filter(is_active=True).order_by('-created_at')
        return context


class EventsListView(ListView):
    model = ClubEvents
    template_name = 'events/events.html'

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
    return render(request, 'web/contact-us.html', {'form': form})

# Async view for staff to see submissions
@user_passes_test(lambda u: u.is_staff)
async def contact_requests(request):
    contact_requests = await sync_to_async(list)(ContactRequest.objects.all())
    return render(request, 'membership/profile.html', {'contact_requests': contact_requests})

class PastNewsView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubNews.objects.filter(is_active=False).order_by('-created_at')
        context['past_news'] = True
        return context


class PastEventsView(TemplateView):
    template_name = 'events/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubEvents.objects.filter(Q(end_date__lt=date.today()) | Q(is_archived=True)).order_by('-created_at')
        context['past_events'] = True
        return context