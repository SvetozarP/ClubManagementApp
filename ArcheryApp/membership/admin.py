from django.contrib import admin

from ArcheryApp.membership.models import MemberProfile


# Register your models here.
@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    pass