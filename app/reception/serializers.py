from rest_framework import serializers
from .models import Reception


class ReceptionListSerializer(serializers.ModelSerializer):
    # company = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    # master = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
             # + ' ' + serializers.SlugRelatedField(slug_field='surname', read_only=True, many=True)
    # client = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta():
        model = Reception
        exclude = ('id', )