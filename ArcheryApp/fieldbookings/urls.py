from django.urls import path, include

from ArcheryApp.fieldbookings.views import CreateFieldBookingsView, ListBookingsView, create_event, \
    FieldBookingDetailView, EditBookingView, DeleteBookingView

urlpatterns = [
    path('', CreateFieldBookingsView.as_view(), name='create-booking'),
    path('list/', ListBookingsView.as_view(), name='list-bookings'),
    path('create/<str:date>', create_event, name='create_date_booking'),
    path('<int:pk>/', include([
        path('detail/', FieldBookingDetailView.as_view(), name='booking-detail'),
        path('edit/', EditBookingView.as_view(), name='edit-field-booking'),
        path('delete/', DeleteBookingView.as_view(), name='cancel-field-booking'),
    ]))
]
