# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Company
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CompanyListSerializer, CompanyDetailSerializer
from django.shortcuts import get_object_or_404


class CompanyListView(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)


class CompanyDetailView(APIView):
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanyDetailSerializer(company)
        return Response(serializer.data)