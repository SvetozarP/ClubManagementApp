from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy

from ArcheryApp.training.models import ShootSessionDetails


# Create your views here.
def training(request):
    pass

class EditNotesView(LoginRequiredMixin, UpdateView):
    model = ShootSessionDetails
    fields = ['details']
    success_url = reverse_lazy('list-bookings')
    template_name = 'training/edit_notes.html'


class DeleteNoteView(LoginRequiredMixin, DeleteView):
    model = ShootSessionDetails
    success_url = reverse_lazy('list-bookings')

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
