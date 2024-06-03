from django.urls import path
from .views import *

urlpatterns = [
    path('get/weatherdata/', get_weather_data, name='get-weather-data'),
    path('api/get/maininfo/', get_main_info, name='maininfo'),
]