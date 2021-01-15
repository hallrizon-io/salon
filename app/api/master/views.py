# Create your views here.
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.formats import date_format
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.reception.models import Reception
from api.reception.serializers import BookedHoursSerializer

from main.services import DefaultPagination

from .managers import MasterViewManager
from .models.master import Master
from .models.worktype import WorkType
from .serializers.master_list import MasterListSerializer, WorkTypesListSerializer

from rest_framework import viewsets, generics


class MasterListView(APIView):

    def get(self, request, *args, **kwargs):
        masters = Master.objects.all()
        paginator = DefaultPagination()
        serializer = MasterListSerializer(paginator.paginate_queryset(masters, request), many=True)
        return paginator.get_paginated_response(serializer.data)


class CreateMasterView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        master_view_manager = MasterViewManager(request)
        status_code = status.HTTP_201_CREATED
        try:
            master = master_view_manager.processing()
            response = {
                'id': master.id,
                'date_joined': date_format(master.profile.date_joined, 'DATETIME_FORMAT')
            }
        except ValidationError as error:
            response = error.detail
            status_code = error.status_code

        return Response(response, status=status_code)


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
            Q(status=Reception.Status.BOOKED) | Q(status=Reception.Status.ACCEPTED),
            Q(start_timestamp__gte=from_date.timestamp()) & Q(start_timestamp__lt=to_date.timestamp())
        )

        paginator = DefaultPagination()
        serializer = BookedHoursSerializer(paginator.paginate_queryset(receptions, request), many=True)

        return paginator.get_paginated_response(serializer.data)


class WorkTypesViewSet(viewsets.GenericViewSet,
                       viewsets.mixins.CreateModelMixin,
                       viewsets.mixins.ListModelMixin,
                       ):
    serializer_class = WorkTypesListSerializer
    queryset = WorkType.objects.all()
