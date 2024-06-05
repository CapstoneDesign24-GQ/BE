from django.db import models
from accounts.models import User

# Create your models here.

class Crop(models.Model):
    cropId = models.AutoField(primary_key=True)
    cropName = models.CharField(max_length=100, unique=False)

class Pest(models.Model):
    pestId = models.AutoField(primary_key=True)
    pestName = models.CharField(max_length=100)
    pestImage = models.CharField(max_length=100)
    pestInfo = models.TextField()
    pestStepImage1 = models.CharField(max_length=100)
    pestStepImage2 = models.CharField(max_length=100, null=True)
    pestStepImage3 = models.CharField(max_length=100, null=True)
    pesticideExcel = models.CharField(max_length=100, null=True)

class Pesticide(models.Model):
    pesticideId = models.AutoField(primary_key=True)
    pesticideName = models.CharField(max_length=100)
    companyName = models.CharField(max_length=100)

class UserSelect(models.Model):
    userSelectId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selectedCrop = models.CharField(max_length=100, unique=False)
    selectedLocation = models.CharField(max_length=100, unique=False)
    selectedDate = models.DateField()

    class Meta:
        get_latest_by = 'userSelectId'

class RiskForecast(models.Model):
    riskForecastId = models.AutoField(primary_key=True)
    selectedCrop = models.ForeignKey(UserSelect, on_delete=models.CASCADE, related_name='selected_crop_forecasts', null=True) 
    selectedLocation = models.ForeignKey(UserSelect, on_delete=models.CASCADE, related_name='selected_location_forecasts', null=True)
    percentages = models.JSONField()
    riskLevels = models.JSONField()

class CropPesticide(models.Model):
    cropPesticideId = models.AutoField(primary_key=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)
    safeUsagePeriod = models.CharField(max_length=100)
    safeUsageFrequency = models.CharField(max_length=100)

class PestPesticide(models.Model):
    pestPesticideId = models.AutoField(primary_key=True)
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE)
    pesticide = models.ForeignKey(Pesticide, on_delete=models.CASCADE)

class Management(models.Model):
    managementId = models.AutoField(primary_key=True)
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE)
    management1 = models.TextField()
    management2 = models.TextField(blank=True)
    
class Location(models.Model):
    locationId = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
