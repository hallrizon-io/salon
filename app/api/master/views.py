# Create your views here.
from datetime import datetime, timedelta, date

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.formats import date_format
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.exceptions import ValidationError

from api.company.models import Company
from api.company.serializers import CreateCompanySerializer
from api.profile.models import Profile
from api.profile.serializers import CreateProfileSerializer
from api.reception.models import Reception
from api.reception.serializers import BookedHoursSerializer
from main.service import DefaultPagination
from .models import Master
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MasterListSerializer, WorkTypeListSerializer


class MasterListView(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request, *args, **kwargs):
        masters = Master.objects.all()
        paginator = DefaultPagination()
        serializer = MasterListSerializer(paginator.paginate_queryset(masters, request), many=True)
        return paginator.get_paginated_response(serializer.data)


class CreateMasterView(APIView):
    def post(self, request, *args, **kwargs):
        profile_serializer = CreateProfileSerializer(
            user_type=Profile.UserType.MASTER, data=request.data.get('profile')
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

                master = Master.objects.create_master(
                    profile=profile_serializer.save(),
                    company=company,
                    work_types=work_types_serializer.save()
                )

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
