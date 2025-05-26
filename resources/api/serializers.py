from rest_framework import serializers
from ..models import resources as ResourceModel

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceModel
        fields = '__all__'
        read_only_fields = ('id', 'uploaded_at', 'uploaded_by') 