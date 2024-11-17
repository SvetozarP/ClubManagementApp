from django.contrib import admin

from ArcheryApp.news.models import ClubNews
from ArcheryApp.web.models import ClubMission, Testimonials, ClubHistory, MembershipInfo


# Register your models here.

@admin.register(ClubMission)
class ClubMissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    pass

@admin.register(ClubHistory)
class ClubHistoryAdmin(admin.ModelAdmin):
    pass

@admin.register(MembershipInfo)
class MembershipInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(ClubNews)
class ClubNewsAdmin(admin.ModelAdmin):
    pass