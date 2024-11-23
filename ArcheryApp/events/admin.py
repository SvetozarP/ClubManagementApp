from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from ArcheryApp.events.models import ClubEvents


# Register your models here.
@admin.register(ClubEvents)
class ClubEventsAdmin(ModelAdmin):
    list_display = ['title', 'hosted_by', 'start_date', 'end_date', 'is_archived']
    list_filter = [
        ('start_date', RangeDateFilter),
        ('end_date', RangeDateFilter),
    ]
    list_filter_submit = True
    search_fields = ['title', 'event_description', 'hosted_by']
    ordering = ['start_date']