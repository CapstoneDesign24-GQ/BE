from rest_framework import serializers
from predictors.models import RiskForecast

class RiskForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskForecast
        fields = '__all__'