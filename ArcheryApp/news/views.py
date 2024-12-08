from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, ListView, DeleteView

from ArcheryApp.news.forms import CreateNewsForm, UpdateNewsForm, CreateNewAnnouncementForm, UpdateAnnouncementForm
from ArcheryApp.news.models import ClubNews, ClubAnnouncements


# Create your views here.
# Select only active news to be visible. Order them by date.
class NewsListView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubNews.objects.filter(is_active=True).order_by('-created_at')
        return context


# Show past news, if someone needs to reference
class PastNewsView(TemplateView):
    template_name = 'news/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ClubNews.objects.filter(is_active=False).order_by('-created_at')
        context['past_news'] = True
        return context


# Details for chosen news - full text etc. is_admin can edit news. Passing is_news variable to the template as one
# template serves news and events.
class NewsDetailView(DetailView):
    model = ClubNews
    template_name = 'common/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_news'] = True
        return context

# Is_staff can create news
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

# Is_staff can update news
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

# List of club announcements - visible for people who have not read them
class ClubAnnouncementView(LoginRequiredMixin, ListView):
    model = ClubAnnouncements
    template_name = 'membership/club_announcements.html'
    exclude = ['read_by']


# Is_staff can create new announcements. These are visible in all profiles details
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

# When announcement is opened, we record that the user has read the announcement. We do not display announcements that
# have been read by the user to the user.
class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = ClubAnnouncements
    template_name = 'membership/announcement_detail.html'

    def get_object(self, queryset=None):

        obj = super().get_object(queryset)

        if self.request.user not in obj.read_by.all():
            obj.read_by.add(self.request.user)

        return obj


# Is_staff can update announcements. When announcement is updated, we clear the read_by field to ensure that all users
# read the updated announcement
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


# is_staff can delete announcements.
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