from django.contrib import admin
from .models import *

# Crop 모델에 대한 어드민 클래스
class CropAdmin(admin.ModelAdmin):
    list_display = ['cropId', 'cropName']

admin.site.register(Crop, CropAdmin)

# Pest 모델에 대한 어드민 클래스
class PestAdmin(admin.ModelAdmin):
    list_display = ['pestId', 'pestName', 'pestImage', 'pestInfo', 'pestStepImage1', 'pestStepImage2', 'pestStepImage3', 'pesticideExcel']

admin.site.register(Pest, PestAdmin)

# Pesticide 모델에 대한 어드민 클래스
class PesticideAdmin(admin.ModelAdmin):
    list_display = ['pesticideId', 'pesticideName', 'companyName']

admin.site.register(Pesticide, PesticideAdmin)

# RiskForecast 모델에 대한 어드민 클래스
class RiskForecastAdmin(admin.ModelAdmin):
    list_display = ['riskForecastId', 'selectedCrop', 'selectedLocation', 'percentages', 'riskLevels']

admin.site.register(RiskForecast, RiskForecastAdmin)

# CropPesticide 모델에 대한 어드민 클래스
class CropPesticideAdmin(admin.ModelAdmin):
    list_display = ['cropPesticideId', 'crop', 'pesticide', 'safeUsagePeriod', 'safeUsageFrequency']

admin.site.register(CropPesticide, CropPesticideAdmin)

# PestPesticide 모델에 대한 어드민 클래스
class PestPesticideAdmin(admin.ModelAdmin):
    list_display = ['pestPesticideId', 'pest', 'pesticide']

admin.site.register(PestPesticide, PestPesticideAdmin)

# Management 모델에 대한 어드민 클래스
class ManagementAdmin(admin.ModelAdmin):
    list_display = ['managementId', 'pest', 'management1', 'management2']

admin.site.register(Management, ManagementAdmin)

# Location 모델에 대한 어드민 클래스
class LocationAdmin(admin.ModelAdmin):
    list_display = ['locationId', 'location']

admin.site.register(Location, LocationAdmin)

# UserSelect 모델에 대한 어드민 클래스
class UserSelectAdmin(admin.ModelAdmin):
    list_display = ['userSelectId', 'user', 'selectedCrop', 'selectedLocation', 'selectedDate']
admin.site.register(UserSelect, UserSelectAdmin)