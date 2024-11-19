from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

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
