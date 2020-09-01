from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Reception
from .serializers import ReceptionListSerializer, CreateReceptionSerializer


class ReceptionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        receptions = Reception.objects.all()
        serializer = ReceptionListSerializer(receptions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        reception_serializer = CreateReceptionSerializer(data=request.data)
        status_code = status.HTTP_201_CREATED
        try:
            reception_serializer.is_valid(raise_exception=True)

            reception = reception_serializer.save()

            response = {
                'id': reception.id,
                'service_name': reception.service.name,
                'master': reception.master.profile.full_name,
                'start_time': reception.start_datetime,
                'end_time': reception.end_datetime
            }
        except ValidationError as error:
            response = error.detail
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status_code)
