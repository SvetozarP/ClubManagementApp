from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

from ArcheryApp.common.mixins import StaffRestrictedAdminMixin, RestrictedToStaffMixin
from ArcheryApp.web.models import ClubMission, Testimonials, ClubHistory, MembershipInfo, ContactRequest, \
    HandleContactRequest


# Register your models here.
# Registering models for edit from the admin panel. Hold modification history with SimpleHistory
@admin.register(ClubMission)
class ClubMissionAdmin(StaffRestrictedAdminMixin, ModelAdmin, SimpleHistoryAdmin):
    pass


@admin.register(ClubHistory)
class ClubHistoryAdmin(StaffRestrictedAdminMixin, ModelAdmin, SimpleHistoryAdmin):
    pass


@admin.register(MembershipInfo)
class MembershipInfoAdmin(StaffRestrictedAdminMixin, ModelAdmin, SimpleHistoryAdmin):
    pass

@admin.register(Testimonials)
class TestimonialsAdmin(StaffRestrictedAdminMixin, ModelAdmin):
    pass

# Enable search fields and filters for contact requests
@admin.register(ContactRequest)
class ContactRequestAdmin(RestrictedToStaffMixin, ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_filter = ['created_at']

# Register actions taken for contact requests
@admin.register(HandleContactRequest)
class HandleContactRequest(RestrictedToStaffMixin, ModelAdmin):
    list_display = ['action_by', 'contact_request']
