from .models import Client
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ClientListSerializer

# Create your views here.


class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientListSerializer(clients, many=True)
        return Response(serializer.data)


def index(request):
    return HttpResponse('<h1>Hello world</h1>')
