from django.contrib import admin

from ArcheryApp.events.models import ClubEvents


# Register your models here.
@admin.register(ClubEvents)
class ClubEventsAdmin(admin.ModelAdmin):
    pass