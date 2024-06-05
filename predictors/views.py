from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *
from accounts.models import User

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import json, logging

# 사용자 초기 선택 (작물, 지역, 날짜)
@method_decorator(csrf_exempt, name='dispatch')
class InitialSelectionView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        selected_crop = data.get('selectedCrop')
        selected_location = data.get('selectedLocation')
        selected_date = data.get('selectedDate')

        if selected_crop and selected_location and selected_date:
            # 사용자 정보 가져오기 (관리자가 직접 채워둔 사용자 정보를 사용. 로그인 기능의 부재로 인해 defaultUser 사용)
            user = User.objects.first()  # 첫 번째 사용자 정보를 가져옴

            user_select = UserSelect(
                selectedCrop=selected_crop,
                selectedLocation=selected_location,
                selectedDate=selected_date,
                user=user
            )
            user_select.save()

            serializer = UserSelectSerializer(user_select)
            return Response({'message': '지역, 작물, 날짜 선택 및 저장 성공!', 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incomplete data received'}, status=status.HTTP_400_BAD_REQUEST)
        
logger = logging.getLogger(__name__)

# 지역 수정
@method_decorator(csrf_exempt, name='dispatch')
class UpdateSelectedLocationView(APIView):
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            selected_location = data.get('selectedLocation')

            if selected_location:
                user_select = UserSelect.objects.latest('userSelectId')

                if user_select:
                    user_select.selectedLocation = selected_location
                    user_select.save()

                    serializer = UserSelectSerializer(user_select)
                    return Response({'message': '지역 수정 성공!', 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '사용자 선택 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': '수정할 지역 정보가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            error_message = f"잘못된 JSON 데이터 수신: {e}"
            logger.error(error_message)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = f"오류 발생: {e}"
            logger.error(error_message)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 작물 수정
@method_decorator(csrf_exempt, name='dispatch')
class UpdateSelectedCropView(APIView):
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            selected_crop = data.get('selectedCrop')

            if selected_crop:
                user_select = UserSelect.objects.latest('userSelectId')

                if user_select:
                    user_select.selectedCrop = selected_crop
                    user_select.save()

                    serializer = UserSelectSerializer(user_select)
                    return Response({'message': '작물 수정 성공!', 'data': serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '사용자 선택 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': '수정할 작물 정보가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError as e:
            error_message = f"잘못된 JSON 데이터 수신: {e}"
            logger.error(error_message)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = f"오류 발생: {e}"
            logger.error(error_message)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# 해충 정보 조회
@method_decorator(csrf_exempt, name='dispatch')
class PestInfoAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        pest_name = data.get('pestName')
        selected_crop = data.get('selectedCrop')

        # 선택한 작물과 해충에 대한 정보를 기반으로 해당 해충을 가져옴
        pest = get_object_or_404(Pest, pestName=pest_name)

        # 선택한 해충에 대한 관리 정보를 가져옴
        management_info = self.get_management_info(pest_name)

        # 해당 해충과 관리 정보를 시리얼라이저를 통해 응답함
        pest_serializer = PestSerializer(pest)

        # 해당 작물에 대한 농약 정보 가져오기
        crop_pesticides = CropPesticide.objects.filter(crop__cropName=selected_crop)

        # 해당 작물과 관련된 농약 중에서 pestName과 일치하는 것 찾기
        matching_pesticides = []
        for crop_pesticide in crop_pesticides:
            pesticide = crop_pesticide.pesticide
            pest_pesticides = PestPesticide.objects.filter(pest__pestName=pest_name, pesticide=pesticide)
            if pest_pesticides.exists():
                matching_pesticides.append(crop_pesticide)

        pest_info = pest_serializer.data

        unique_pesticides = set()
        pesticide_info = []
        for crop_pesticide in matching_pesticides:
            pesticide_id = crop_pesticide.pesticide.pesticideId
            if pesticide_id not in unique_pesticides:
                serializer1 = PesticideDetailSerializer(crop_pesticide)
                pesticide_info.append(serializer1.data)
                unique_pesticides.add(pesticide_id)
      
        response_data = {
            'pest': pest_info,
            'management': management_info,
            'pesticide_info': pesticide_info,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    # 선택한 해충에 대한 관리 정보를 가져옴
    def get_management_info(self, pest_name):
        management = get_object_or_404(Management, pest__pestName=pest_name)

        management1 = management.management1
        management_list = management1.split('/') if management1 else []
        return management_list