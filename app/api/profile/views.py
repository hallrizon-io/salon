from rest_framework import status
from rest_framework.serializers import ValidationError

from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileListSerializer, CreateProfileSerializer
from objects.ip import IP


# Create your views here.


class ProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        clients = Profile.objects.all()
        serializer = ProfileListSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        response = {}
        serializer = CreateProfileSerializer(Profile.UserType.CLIENT, data=request.data)
        client_ip = IP.get_client_ip(request)
        status_code = status.HTTP_200_OK
        try:
            serializer.is_valid(raise_exception=True)
            profile = serializer.save()
            response['id'] = profile.id
            response['date_joined'] = profile.date_joined.strftime('%Y-%m-%d %H:%M:%S')
            response['user_location'] = IP.get_location_by_ip(client_ip)
        except ValidationError as error:
            response = serializer.errors
            status_code = error.status_code

        return Response(response, status=status_code)