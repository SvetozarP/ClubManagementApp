from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import CreateEventForm, UpdateEventForm
from .models import ClubEvents
from .serializers import BookingSerializer, FieldBookingSerializer
from ..fieldbookings.models import FieldBookings


@login_required
def calendar_view(request):
    bookings = ClubEvents.objects.all()
    field_bookings = FieldBookings.objects.all()

    booking_serializer = BookingSerializer(bookings, many=True)
    field_booking_serializer = FieldBookingSerializer(field_bookings, many=True)

    data = {
        "bookings": booking_serializer.data,
        "field_bookings": field_booking_serializer.data
    }

    return render(request, 'events/calendar.html', {'data': data})


class CalendarAPIView(APIView):
    def get(self, request, *args, **kwargs):
        bookings = ClubEvents.objects.all()
        field_bookings = FieldBookings.objects.all()

        booking_serializer = BookingSerializer(bookings, many=True)
        field_booking_serializer = FieldBookingSerializer(field_bookings, many=True)

        return Response({
            "bookings": booking_serializer.data,
            "field_bookings": field_booking_serializer.data
        })


class EventsListView(ListView):
    model = ClubEvents
    template_name = 'events/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubEvents.objects.filter(Q(end_date__gte=date.today()) & Q(is_archived=False)).order_by('-created_at')
        return context

class PastEventsView(TemplateView):
    template_name = 'events/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubEvents.objects.filter(Q(end_date__lt=date.today()) | Q(is_archived=True)).order_by('-created_at')
        context['past_events'] = True
        return context


class EventDetailsView(DetailView):
    model = ClubEvents
    template_name = 'common/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_event'] = True
        return context


class CreateNewEventView(UserPassesTestMixin, CreateView):
    model = ClubEvents
    form_class = CreateEventForm
    template_name = 'common/create-new-event.html'
    success_url = reverse_lazy('club-events')  # Redirect back to the events list on success

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateEventView(UserPassesTestMixin, UpdateView):
    model = ClubEvents
    template_name = 'common/create-new-event.html'
    form_class = UpdateEventForm
    success_url = reverse_lazy('club-events')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

@login_required
def participation_functionality(request, pk: int):
    event_object = get_object_or_404(ClubEvents, id=pk)

    if request.user in event_object.participants.all():

        event_object.participants.remove(request.user)
    else:

        event_object.participants.add(request.user)

    return redirect('club-event-detail', pk=pk)
