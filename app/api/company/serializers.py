from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Company
from api.master.serializers.master_detail import MasterDetailSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'rating', 'opening_hours',
                  'closing_hours', 'image', 'enter_code', 'is_active')


class CompanyDetailSerializer(serializers.ModelSerializer):
    masters = MasterDetailSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'address', 'opening_hours', 'closing_hours')
        extra_kwargs = {
            'name': {'allow_blank': False, 'required': False},
            'address': {'allow_blank': False, 'required': False},
            'opening_hours': {'required': False},
            'closing_hours': {'required': False},
        }

    def validate(self, attrs):
        request = dict(attrs)
        request.update(self.context)

        if request.get('new_company', False):
            required_fields = self.fields.keys()
        else:
            required_fields = ['enter_code']

        for field in required_fields:
            if field not in request.keys():
                raise ValidationError({field: 'This field is required.'})
            elif not request[field]:
                raise ValidationError({field: 'This field may not be blank.'})

        if 'enter_code' in required_fields and not Company.objects.filter(enter_code=request.get('enter_code')).exists():
            raise ValidationError({'enter_code': 'Not found company by current enter_code'})

        return request
