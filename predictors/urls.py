from django.urls import path
from .views import *

urlpatterns = [
    path('api/select/', InitialSelectionView.as_view(), name='initial-selection'),
    path('api/update/crop/', UpdateSelectedCropView.as_view(), name='update-selected-crop'),
    path('api/update/location/', UpdateSelectedLocationView.as_view(), name='update-selected-location'),
    path('api/get/pestinfo/', PestInfoAPIView.as_view(), name='pest_info'),
]