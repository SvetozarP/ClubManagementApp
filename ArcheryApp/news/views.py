from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, ListView, DeleteView

from ArcheryApp.news.forms import CreateNewsForm, UpdateNewsForm, CreateNewAnnouncementForm, UpdateAnnouncementForm
from ArcheryApp.news.models import ClubNews, ClubAnnouncements


# Create your views here.
class NewsListView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubNews.objects.filter(is_active=True).order_by('-created_at')
        return context


class PastNewsView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubNews.objects.filter(is_active=False).order_by('-created_at')
        context['past_news'] = True
        return context


class NewsDetailView(DetailView):
    model = ClubNews
    template_name = 'common/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_news'] = True
        return context


class CreateNewsView(UserPassesTestMixin, CreateView):
    model = ClubNews
    form_class = CreateNewsForm
    template_name = 'common/create_news.html'
    success_url = reverse_lazy('club-news')  # Redirect back to the news list on success

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateNewsView(UserPassesTestMixin, UpdateView):
    model = ClubNews
    template_name = 'common/create_news.html'
    form_class = UpdateNewsForm
    success_url = reverse_lazy('club-news')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")


class ClubAnnouncementView(LoginRequiredMixin, ListView):
    model = ClubAnnouncements
    template_name = 'membership/club_announcements.html'
    exclude = ['read_by']


class CreateAnnouncementView(UserPassesTestMixin, CreateView):
    model = ClubAnnouncements
    template_name = 'membership/create.html'
    form_class = CreateNewAnnouncementForm
    success_url = reverse_lazy('club-announcements')
    exclude = ['read_by', 'author', 'created_at']

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_announcement'] = True
        return context

class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = ClubAnnouncements
    template_name = 'membership/announcement_detail.html'

    def get_object(self, queryset=None):

        obj = super().get_object(queryset)

        if self.request.user not in obj.read_by.all():
            obj.read_by.add(self.request.user)

        return obj

class AnnouncementUpdateView(UserPassesTestMixin, UpdateView):
    model = ClubAnnouncements
    template_name = 'membership/create.html'
    form_class = UpdateAnnouncementForm
    success_url = reverse_lazy('club-announcements')
    exclude = ['read_by', 'author', 'created_at']

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def form_valid(self, form):

        announcement = form.instance
        announcement.read_by.clear()

        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_announcement'] = True
        return context


class DeleteAnnouncementView(UserPassesTestMixin, DeleteView):
    model = ClubAnnouncements
    success_url = reverse_lazy('club-announcements')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("login")

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)