from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

from ArcheryApp.fieldbookings.models import FieldConfiguration


# Register your models here.

class FieldConfigurationAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ['lane_no', 'distance', 'max_archers']
    list_filter = ['lane_no', 'distance', 'max_archers']

admin.site.register(FieldConfiguration, FieldConfigurationAdmin)
