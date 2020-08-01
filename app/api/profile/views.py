from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileListSerializer


# Create your views here.


class ProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        clients = Profile.objects.all()
        serializer = ProfileListSerializer(clients, many=True)
        return Response(serializer.data)
