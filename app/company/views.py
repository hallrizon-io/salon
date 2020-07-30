from .models import Company
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CompanyListSerializer

# Create your views here.


class CompanyListView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)