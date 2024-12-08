from django.urls import path

from ArcheryApp.web.views import IndexView, HistoryList, MembershipDetailsView, contact_us, ContactRequestDetailsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'), # Main landing page
    path('history/', HistoryList.as_view(), name='club-history'), # CLub history page
    path('membershipinfo/', MembershipDetailsView.as_view(), name='club-membershipinfo'), # Membership info page

    path('contact/', contact_us, name='contact-us'), # Contact us page
    path('contact/<int:pk>', ContactRequestDetailsView.as_view(), name='contact-us-detail') # Detail view for contact requests - is_staff
]
