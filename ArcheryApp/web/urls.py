from django.urls import path

from ArcheryApp.web.views import IndexView, HistoryList, MembershipDetailsView, EventsListView, NewsListView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('history/', HistoryList.as_view(), name='club-history'),
    path('membershipinfo/', MembershipDetailsView.as_view(), name='club-membershipinfo'),
    path('events/', EventsListView.as_view(), name='club-events'),
    path('news/', NewsListView.as_view(), name='club-news'),
]
