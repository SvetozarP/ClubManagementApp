from django.contrib import admin

from ArcheryApp.fieldbookings.models import FieldBookings


# Register your models here.
@admin.register(FieldBookings)
class FieldBookingsAdmin(admin.ModelAdmin):
    pass