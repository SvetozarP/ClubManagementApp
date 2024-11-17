from datetime import date

from django.views.generic import TemplateView, ListView

from ArcheryApp.events.models import ClubEvents
from ArcheryApp.fieldbookings.models import FieldBookings
from ArcheryApp.news.models import ClubNews
from ArcheryApp.web.models import ClubMission, Testimonials, ClubHistory, MembershipInfo


# Create your views here.
class IndexView(TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['mission'] = ClubMission.objects.first()
        context['events'] = ClubEvents.objects.filter(end_date__gte=date.today()).order_by('-created_at')[:3]
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


class NewsListView(ListView):
    model = ClubNews
    template_name = 'news/news.html'


class EventsListView(ListView):
    model = ClubEvents
    template_name = 'events/events.html'