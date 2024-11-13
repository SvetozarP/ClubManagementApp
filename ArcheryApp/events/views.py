from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CombinedBookingSerializer

class CombinedBookingView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CombinedBookingSerializer()
        return Response(serializer.data)

def calendar_view(request):
    # Serialize the booking data to pass to the template
    serializer = CombinedBookingSerializer()
    data = serializer.data
    return render(request, 'events/calendar.html', {'data': data})