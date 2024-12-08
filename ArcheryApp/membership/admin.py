# from django.contrib import admin - Unfold looks better.
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin

from ArcheryApp.common.mixins import StaffRestrictedAdminMixin
from ArcheryApp.membership.models import MemberProfile

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass



# Register your models here.
@admin.register(MemberProfile)
class MemberProfileAdmin(ModelAdmin, StaffRestrictedAdminMixin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'profile_completed', 'is_registered', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['profile_completed', 'is_registered', 'is_staff', 'is_superuser', 'is_active']
    ordering = ['-is_superuser', '-is_staff', 'created_at']
