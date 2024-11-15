from django.contrib import admin

from ArcheryApp.web.models import ClubMission, Testimonials


# Register your models here.

@admin.register(ClubMission)
class ClubMissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    pass