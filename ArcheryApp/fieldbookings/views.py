from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from ArcheryApp.fieldbookings.forms import CreateBookingForm, UpdateBookingForm
from ArcheryApp.fieldbookings.models import FieldBookings
from ArcheryApp.training.forms import AddTrainingNotesForm


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


class FieldBookingDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model=FieldBookings
    template_name = 'fieldbooking/booking_detail.html'
    form_class = AddTrainingNotesForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():

            add_details = form.save(commit=False)
            add_details.archer_id = request.user.id
            add_details.shoot_session = self.object
            add_details.save()

            return redirect("booking-detail", pk=self.object.pk)
        else:
            messages.error(request, "There was an error with your submission.")
            return self.form_invalid(form)


class EditBookingView(LoginRequiredMixin, UpdateView):
    model = FieldBookings
    template_name = 'fieldbooking/edit_booking.html'
    form_class = UpdateBookingForm
    success_url = reverse_lazy('list-bookings')

    def form_valid(self, form):
        form.instance.archer = self.request.user
        return super().form_valid(form)


class DeleteBookingView(LoginRequiredMixin, DeleteView):
    model = FieldBookings
    success_url = reverse_lazy('list-bookings')

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
