from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from ArcheryApp.fieldbookings.forms import CreateBookingForm
from ArcheryApp.fieldbookings.models import FieldBookings


# Create your views here.

def bookings(request):
    pass

class CreateFieldBookingsView(LoginRequiredMixin, CreateView):
    model = FieldBookings
    form_class = CreateBookingForm
    template_name= 'fieldbooking/create.html'
    success_url = reverse_lazy('create-booking')

    def form_valid(self, form):
        form.instance.archer = self.request.user
        return super().form_valid(form)


class ListBookingsView(LoginRequiredMixin, ListView):
    model = FieldBookings
    template_name = 'fieldbooking/bookings_list.html'
    paginate_by = 10

    def get_queryset(self):
        return FieldBookings.objects.filter(archer=self.request.user)

@login_required
def create_event(request, date):
    try:
        event_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise Http404("Invalid date format.")

    if request.method == "POST":
        form = CreateBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.archer_id = request.user.id
            booking.date = event_date
            booking.save()
            return redirect('calendar-view')
    else:
        form = CreateBookingForm(initial={'date': event_date})

    return render(request, "fieldbooking/create.html", {"form": form})