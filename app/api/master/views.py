# Create your views here.
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from rest_framework import status

from ..reception.models import Reception
from ..reception.serializers import BookedHoursSerializer
from .models import Master
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MasterListSerializer


class MasterListView(APIView):
    def get(self, request):
        masters = Master.objects.all()
        serializer = MasterListSerializer(masters, many=True)
        return Response(serializer.data)


class MasterBookedHoursView(APIView):
    def get(self, request, pk):
        try:
            get_object_or_404(Master, pk=pk)

            today = date.today().isoformat()
            from_date = datetime.fromisoformat(request.query_params.get('date', today))
            to_date = from_date + timedelta(days=1)

            master_booked_records = Reception.objects.filter(
                master=pk, status=Reception.Status.ACCEPTED,
                time__range=(from_date, to_date)
            )
            serializer = BookedHoursSerializer(master_booked_records, many=True)
            response = Response(serializer.data)
        except:
            response = Response({'detail': 'Incorrect Date'}, status=status.HTTP_400_BAD_REQUEST)
        return response
