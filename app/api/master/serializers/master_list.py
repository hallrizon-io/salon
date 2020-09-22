from rest_framework import serializers
from api.master.models import Master
from api.master.serializers.work_type_list import WorkTypesListSerializer
from api.profile.serializers import ProfileDetailSerializer


class RatingsField(serializers.ListField):
    def to_representation(self, data):
        ratings_field = []

        for item in data.ratings:
            item.pop('master')
            item['company_id'] = item.pop('company')
            item['service_id'] = item.pop('service')
            ratings_field.append(item)
        return ratings_field


class CompanyField(serializers.ListField):
    def to_representation(self, data):
        company_field = []
        for company in data.company.all():
            company_field.append({
                'id': company.id,
                'name': company.name,
                'address': company.address,
                'opening_hours': company.opening_hours,
                'closing_hours': company.closing_hours,
                'image': company.image.name if company.image.name else None,
                'is_active': company.is_active
            })

        return company_field


class MasterListSerializer(serializers.ModelSerializer):
    company = CompanyField(source='*')
    work_types = WorkTypesListSerializer(many=True)
    profile = ProfileDetailSerializer()
    ratings = RatingsField(source='*')

    class Meta:
        model = Master
        fields = ('id', 'profile', 'company', 'work_types', 'ratings')
