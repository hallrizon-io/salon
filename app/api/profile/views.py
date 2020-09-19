# Create your views here.
from django.utils.formats import date_format
from rest_framework import status
from rest_framework.serializers import ValidationError
from main.services import DefaultPagination
from .models import Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProfileListSerializer, CreateProfileSerializer
from objects.ip import IP


class ProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        clients = Profile.objects.all()
        paginator = DefaultPagination()
        serializer = ProfileListSerializer(paginator.paginate_queryset(clients, request), many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        response = {}
        serializer = CreateProfileSerializer(Profile.UserType.CLIENT, data=request.data)
        client_ip = IP.get_client_ip(request)
        status_code = status.HTTP_201_CREATED
        try:
            serializer.is_valid(raise_exception=True)
            profile = serializer.save()
            response['id'] = profile.id
            response['date_joined'] = date_format(profile.date_joined, 'DATETIME_FORMAT')
            response['user_location'] = IP.get_location_by_ip(client_ip)
        except ValidationError as error:
            response = serializer.errors
            status_code = error.status_code

        return Response(response, status=status_code)
