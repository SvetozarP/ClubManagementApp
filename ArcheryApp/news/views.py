from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, UpdateView

from ArcheryApp.news.forms import CreateNewsForm, UpdateNewsForm
from ArcheryApp.news.models import ClubNews


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