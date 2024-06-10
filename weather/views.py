from predictors.models import *

import requests, logging, joblib, time
import pandas as pd
import numpy as np

from django.conf import settings
from django.http import JsonResponse, HttpResponseServerError
from django.utils.dateformat import DateFormat

from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from urllib.parse import unquote

# 데이터 처리
def extract_weather_data(json_data):
    required_categories = ['TMP', 'REH', 'VEC', 'WSD', 'PCP']
    extracted_data = []

    if 'response' in json_data and 'body' in json_data['response'] and 'items' in json_data['response']['body']:
        items = json_data['response']['body']['items']['item']
        
        for item in items:
            if item['category'] in required_categories and item['fcstTime'] == '0600':
                extracted_data.append({
                    "category": item['category'],
                    "fcstValue": item['fcstValue']
                })
    
    return extracted_data

# 데이터 형식 처리
def process_weather_data(data):
    categories = ['TMP', 'REH', 'VEC', 'WSD', 'PCP']

    # 초기값 설정
    processed_data = {category: 999 for category in categories}

    for item in data:
        category = item['category']
        value = item['fcstValue']

        # PCP 값 변환
        if category == 'PCP':
            value = 0 if value == '강수없음' or value == 0 else 1

        # 값 형변환
        float_value = float(value)
        int_value = int(float_value)

        # 중복된 값이 없거나 중복된 값이 있어도 나중에 들어온 값으로 덮어쓰기
        processed_data[category] = int_value

    # 요구된 카테고리가 없는 경우에도 기본값으로 추가
    for category in ['TMP', 'REH', 'VEC', 'WSD', 'PCP']:
        if category not in processed_data:
            processed_data[category] = 999  # 기본값은 999으로 설정 -> 오류 시 999

    # 데이터를 리스트 형태로 변환
    converted_data = {key: [value] for key, value in processed_data.items()}

    # converted_data를 DataFrame으로 변환
    input_data = pd.DataFrame(converted_data)

    # 인코딩 함수 정의
    def encode_vec(value):
        if (0 <= value < 22.5) or (337 <= value <= 360):
            return 6
        elif 22.5 <= value < 67.5:
            return 4
        elif 67.5 <= value < 112.5:
            return 3
        elif 112.5 <= value < 157.5:
            return 0
        elif 157.5 <= value < 202.5:
            return 2
        elif 202.5 <= value < 247.5:
            return 1
        elif 247.5 <= value < 292.5:
            return 7
        elif 292.5 <= value < 337.5:
            return 5
        else:
            return None  # 범위를 벗어나는 경우

    # 'VEC' 컬럼 인코딩
    input_data['VEC'] = input_data['VEC'].apply(encode_vec)

    # 컬럼명 변경
    input_data.columns = ['Temperature(℃)', 'Humidity(%)', 'Wind direction', 'Wind speed(ms)', 'Rain condition']
    return input_data

logger = logging.getLogger(__name__)
    
def calculate_risk_level(percentage):
    '''if percentage < 25:
        return '괜찮'
    elif 25 <= percentage < 50:
        return '조심'
    elif 50 <= percentage < 75:
        return '주의'
    else:
        return '위험'''
    mean = 70.9191
    std_dev = 24.367
    
    if percentage >= mean + std_dev:
        return "위험"
    elif mean <= percentage < mean + std_dev:
        return "주의"
    elif mean - std_dev <= percentage < mean:
        return "조심"
    else:
        return "안전"

def get_main_info(request):
    try:
        # 가장 최근에 저장된 사용자 선택 정보 가져오기
        latest_user_select = UserSelect.objects.latest('userSelectId')

        # 선택된 작물, 지역, 날짜
        selected_crop = latest_user_select.selectedCrop
        selected_location = latest_user_select.selectedLocation
        selected_date = latest_user_select.selectedDate

        today_date = datetime.now().date()

        # 날짜 형식 변환
        date = DateFormat(today_date).format('Ymd')

        # 기상 데이터 가져오기
        weather_response = get_weather_data(request)
        if weather_response.status_code != 200:
            return Response({"error": "Failed to fetch data from NWS API"}, status=500)

        weather_data = weather_response.data

        # 예측 모델 로드
        model_path = 'weather/resource/test3_model.pkl' # 이전 모델
        # model_path = 'weather/resource/xgb_optimized_f1.pkl'
        model = joblib.load(model_path)

        # processed_data = process_weather_data(weather_data)
        # processed_data_array = processed_data.to_numpy()
        processed_data_array = pd.DataFrame.from_dict(weather_data).to_numpy()


        # 발생 확률 예측
        y_prob = model.predict_proba(processed_data_array)
        percentage_list = [round(item[0][1] * 100) for item in y_prob]

        # 해충 이름 목록
        insect_names = [
            '담배거세미나방',
            '미국선녀벌레',
            '썩덩나무노린재',
            '작은뿌리파리',
            '톱다리개미허리노린재',
            '흰점도둑나방'
        ]

        # 해충 이름을 키로 사용한 딕셔너리 생성
        percentage = {insect_names[i]: percentage_list[i] for i in range(len(insect_names))}

        # 리스크 레벨 계산
        riskLevel = {insect_names[i]: calculate_risk_level(percentage_list[i]) for i in range(len(insect_names))}

        response_data = {
            'selected_crop': selected_crop,
            'selected_location': selected_location,
            'selected_date': today_date,
            'percentages': percentage,
            'riskLevels': riskLevel
        }

        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        return HttpResponseServerError(f"Error occurred: {str(e)}")
    
# 로그 설정
logger = logging.getLogger(__name__)

def fetch_weather_data(url, params, retries=40, delay=1):
    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except ValueError:
                logger.error(f"JSON 응답을 파싱하는데 실패했습니다: {response.text}")
        else:
            logger.error(f"NWS API에서 데이터를 가져오는데 실패했습니다. 상태 코드: {response.status_code}")
        time.sleep(delay)
    return None


@api_view(['GET'])
def get_weather_data(request):
    # 사용자 날짜 및 시간으로 설정
    latest_user_select = UserSelect.objects.latest('userSelectId')
    selected_date = latest_user_select.selectedDate

    # 오늘 날짜 및 시간으로 설정 
    today_date = datetime.now().date()

    # 날짜 형식 변환
    date = DateFormat(today_date).format('Ymd')
  
    # 기본 지역 설정
    location_name = '충청도'

    # 지역에 따른 좌표 설정
    region_coords = {
        '충청도': {'nx': '76', 'ny': '114'},
        '경상도': {'nx': '98', 'ny': '76'},
        '경기도': {'nx': '60', 'ny': '120'},
        '강원도': {'nx': '85', 'ny': '126'},
        '제주도': {'nx': '48', 'ny': '36'},
        '전라도': {'nx': '48', 'ny': '59'}
    }

    coords = region_coords.get(location_name, {'nx': '76', 'ny': '114'})

    try:
        eapi_key = settings.NWS_API_KEY
        api_key = unquote(eapi_key, 'UTF-8')
        if not api_key:
            raise ValueError("API key is empty")
    except AttributeError:
        logger.error("NWS_API_KEY가 설정에 없습니다.")
        return Response({"error": "API key not found"}, status=500)
    except ValueError as e:
        logger.error(e)
        return Response({"error": str(e)}, status=500)

    categories = ['TMP', 'REH', 'VEC', 'WSD', 'PCP']

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    model_test_data = {category: [] for category in categories}

    params = {
        'serviceKey': api_key,
        'numOfRows': '290',
        'pageNo': '1',
        'dataType': 'JSON',
        'base_date': date,
        'base_time': '0500', 
        'nx': coords['nx'],
        'ny': coords['ny']
    }

    logger.debug(f"요청 URL: {url}")
    logger.debug(f"요청 파라미터: {params}")
    logger.debug(f"API 키: {api_key}")

    data = fetch_weather_data(url, params)

    if not data:
        return Response({"error": "Failed to fetch data from NWS API after multiple attempts"}, status=500)
    
    # 서비스 오류 확인
    if 'response' in data and 'header' in data['response']:
        header = data['response']['header']
        if header['resultCode'] != '00':
            logger.error(f"NWS API에서 오류를 반환했습니다: {header['resultMsg']} (코드: {header['resultCode']})")
            return Response({
                "error": "NWS API returned an error",
                "resultCode": header['resultCode'],
                "resultMsg": header['resultMsg']
            }, status=500)

    extract_data = extract_weather_data(data)
    processed_data = process_weather_data(extract_data)
    # result_data = model_test(processed_data)
    return Response(processed_data.to_dict(), status=200)