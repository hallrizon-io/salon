from .models import Master
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MasterListSerializer

# Create your views here.


class MasterListView(APIView):
    def get(self, request):
        masters = Master.objects.all()
        serializer = MasterListSerializer(masters, many=True)
        return Response(serializer.data)