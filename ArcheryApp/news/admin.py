from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from ArcheryApp.news.models import ClubNews, ClubAnnouncements


# Register your models here.
@admin.register(ClubNews)
class ClubNewsAdmin(ModelAdmin):
    list_display = ['title', 'author', 'is_active']
    search_fields = ['title', 'news_text']
    list_filter = ['created_at', 'author', 'is_active']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

@admin.register(ClubAnnouncements)
class ClubAnnouncementsAdmin(ModelAdmin):
    list_display = ['title', 'author']
    search_fields = ['title', 'text', 'read_by__first_name', 'read_by__last_name', 'read_by__username', 'read_by__email']
    ordering = ['-created_at']
    list_filter = [('created_at', RangeDateFilter)]
