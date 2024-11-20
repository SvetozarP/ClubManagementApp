from django.urls import path

from ArcheryApp.web.views import IndexView, HistoryList, MembershipDetailsView, contact_us

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('history/', HistoryList.as_view(), name='club-history'),
    path('membershipinfo/', MembershipDetailsView.as_view(), name='club-membershipinfo'),

    path('contact/', contact_us, name='contact-us'),
]
