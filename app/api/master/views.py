# Create your views here.
from datetime import datetime, timedelta, date

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.formats import date_format
from rest_framework import status
from rest_framework.exceptions import ValidationError

from ..company.models import Company
from ..company.serializers import CreateCompanySerializer
from ..profile.models import Profile
from ..profile.serializers import CreateProfileSerializer
from ..reception.models import Reception
from ..reception.serializers import BookedHoursSerializer
from .models import Master
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MasterListSerializer, WorkTypeListSerializer


class MasterAPIView(APIView):
    def get(self, request, *args, **kwargs):
        masters = Master.objects.all()
        serializer = MasterListSerializer(masters, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        profile_serializer = CreateProfileSerializer(
            Profile.UserType.MASTER, data=request.data.get('profile')
        )
        work_types_serializer = WorkTypeListSerializer(data=request.data)
        company_serializer = CreateCompanySerializer(data=request.data.get('company'))
        try:
            profile_serializer.is_valid(raise_exception=True)
            work_types_serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                if request.data.get('new_company', False):
                    company_serializer.is_valid(raise_exception=True)
                    company = company_serializer.save()
                else:
                    company = get_object_or_404(
                        Company, enter_code=request.data.get('company').get('enter_code')
                    )

                profile = profile_serializer.save()
                master = Master.objects.create(profile=profile)

                work_types = work_types_serializer.save()

                master.company.add(company)
                master.work_types.add(*work_types)

            response = {
                'id': master.id,
                'date_joined': date_format(master.profile.date_joined, 'DATETIME_FORMAT')
            }
        except ValidationError as error:
            response = error.detail

        return Response(response)


class MasterBookedHoursView(APIView):
    def get(self, request, pk):
        master = get_object_or_404(Master, pk=pk)
        today = date.today().isoformat()
        try:
            from_date = datetime.fromisoformat(request.query_params.get('date', today))
        except:
            return Response({'detail': 'Incorrect Date'}, status=status.HTTP_400_BAD_REQUEST)

        to_date = from_date + timedelta(days=1)

        receptions = master.receptions.filter(
            status=Reception.Status.ACCEPTED,
            time__range=(from_date, to_date)
        )

        serializer = BookedHoursSerializer(receptions, many=True)

        return Response(serializer.data)
