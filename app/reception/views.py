from .models import Reception
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReceptionListSerializer

# Create your views here.


class ReceptionListView(APIView):
    def get(self, request):
        orders = Reception.objects.all()
        serializer = ReceptionListSerializer(orders, many=True)
        return Response(serializer.data)