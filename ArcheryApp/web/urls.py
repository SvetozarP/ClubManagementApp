from django.urls import path

from ArcheryApp.web.views import IndexView, HistoryList, MembershipDetailsView, EventsListView, NewsListView, \
    contact_us, PastNewsView, PastEventsView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('history/', HistoryList.as_view(), name='club-history'),
    path('membershipinfo/', MembershipDetailsView.as_view(), name='club-membershipinfo'),
    path('events/', EventsListView.as_view(), name='club-events'),
    path('news/', NewsListView.as_view(), name='club-news'),
    path('contact/', contact_us, name='contact_us'),
    path('past-news/', PastNewsView.as_view(), name='club-past-news'),
    path('past-events/', PastEventsView.as_view(), name='club-past-events'),
]
