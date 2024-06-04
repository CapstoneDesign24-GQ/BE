from rest_framework import serializers
from .models import *

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class PestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pest
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pest_info = representation.get('pestInfo')

        if isinstance(pest_info, str):
            representation['pestInfo'] = pest_info.split(',')
        else:
            representation['pestInfo'] = []

        return representation

class RiskForecastSerializer(serializers.ModelSerializer):
    pestName = serializers.SerializerMethodField()

    class Meta:
        model = RiskForecast
        fields = '__all__'

    def get_pestName(self, obj):
        return obj.pest.pestName if obj.pest else None

class UserSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSelect
        fields = '__all__'

class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = ['management1', 'management2']

class PesticideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesticide
        fields = ['companyName', 'pesticideName', 'safeUsagePeriod', 'safeUsageFrequency', 'pesticideExcel']
