from main.service import DefaultPagination
from .models import Company
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CompanyListSerializer, CompanyDetailSerializer
from django.shortcuts import get_object_or_404

# Create your views here.


class CompanyListView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        paginator = DefaultPagination()
        serializer = CompanyListSerializer(paginator.paginate_queryset(companies, request), many=True)
        return paginator.get_paginated_response(serializer.data)


class CompanyDetailView(APIView):
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanyDetailSerializer(company)
        return Response(serializer.data)