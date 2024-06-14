from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from scrape_restaurant_data import scrape_restaurant_data
import os
import time

app = Flask(__name__)
CORS(app)

# 캐시 설정
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# 스크래핑한 데이터 저장
restaurants = scrape_restaurant_data()

@app.route('/chat', methods=['POST'])
@cache.cached(timeout=60, query_string=True)
def chat():
    start_time = time.time()
    data = request.json
    user_message = data.get('message')
    
    bot_response = handle_message(user_message)
    
    end_time = time.time()
    print(f"Request processing time: {end_time - start_time} seconds")
    
    return jsonify({'response': bot_response})

def handle_message(message):
    start_time = time.time()
    if "예약" in message:
        response = handle_reservation(message)
    elif "추천" in message:
        response = recommend_restaurant(message)
    elif "취소" in message:
        response = cancel_reservation(message)
    else:
        response = "죄송합니다, 이해하지 못했습니다."
    end_time = time.time()
    print(f"handle_message processing time: {end_time - start_time} seconds")
    return response

def handle_reservation(message):
    start_time = time.time()
    if "지역" in message:
        region = message.split("지역")[1].strip()
        available_restaurants = [r for r in restaurants if region in r['location']]
        if available_restaurants:
            response = f"{region}에서 예약 가능한 음식점은 다음과 같습니다: {', '.join([r['name'] for r in available_restaurants])}"
        else:
            response = f"{region}에서 예약 가능한 음식점을 찾을 수 없습니다."
    else:
        response = "원하시는 지역을 말씀해 주세요."
    end_time = time.time()
    print(f"handle_reservation processing time: {end_time - start_time} seconds")
    return response

def recommend_restaurant(message):
    start_time = time.time()
    if "한식" in message:
        recommended = [r['name'] for r in restaurants if '한식' in r['category']]
        response = f"추천 한식당: {', '.join(recommended)}"
    elif "중식" in message:
        recommended = [r['name'] for r in restaurants if '중식' in r['category']]
        response = f"추천 중식당: {', '.join(recommended)}"
    elif "일식" in message:
        recommended = [r['name'] for r in restaurants if '일식' in r['category']]
        response = f"추천 일식당: {', '.join(recommended)}"
    else:
        response = "어떤 종류의 음식을 찾고 계신가요? 예: 한식, 중식, 일식"
    end_time = time.time()
    print(f"recommend_restaurant processing time: {end_time - start_time} seconds")
    return response

def cancel_reservation(message):
    start_time = time.time()
    if "예약 번호" in message:
        reservation_number = message.split("예약 번호")[1].strip()
        for reservation in reservations:
            if reservation['number'] == reservation_number:
                reservations.remove(reservation)
                response = f"예약 번호 {reservation_number}의 예약이 취소되었습니다."
                break
        else:
            response = f"예약 번호 {reservation_number}을 찾을 수 없습니다."
    else:
        response = "예약 번호를 입력해 주세요."
    end_time = time.time()
    print(f"cancel_reservation processing time: {end_time - start_time} seconds")
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Starting app on port {port}")
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
