from django.urls import path

from ArcheryApp.web.views import IndexView, HistoryList, MembershipDetailsView, contact_us, ContactRequestDetailsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('history/', HistoryList.as_view(), name='club-history'),
    path('membershipinfo/', MembershipDetailsView.as_view(), name='club-membershipinfo'),

    path('contact/', contact_us, name='contact-us'),
    path('contact/<int:pk>', ContactRequestDetailsView.as_view(), name='contact-us-detail')
]
