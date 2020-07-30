from rest_framework import serializers
from .models import Master


class MasterListSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Master
        exclude = ('id',)