import json
import pymysql
from Database import Database

# JSON 데이터를 파싱합니다.
json_data = {
    '123': {
        'password': '123',
        'details': {
            'name': 'dddd',
            'gender': '남성',
            'age': '12',
            'weight': '123',
            'height': '123',
            'allergies': ''
        },
        'diet': {
            '2023-11-24': {
                '아침': [
                    {
                        'name': '제육',
                        'nutrition': {
                            '음식 이름': '제육',
                            '칼로리': 1,
                            '탄수화물': 2,
                            '지방': 3,
                            '단백질': 4,
                            '당류': 10,
                            '나트륨': 4
                        }
                    }
                ],
                '점심': [
                    {
                        'name': '포도',
                        'nutrition': {
                            '음식 이름': '포도',
                            '칼로리': 5,
                            '탄수화물': 6,
                            '지방': 7,
                            '단백질': 8,
                            '당류': 1,
                            '나트륨': 2
                        }
                    }
                ],
                '저녁': []
            }
        }
    }
}

# 데이터베이스 객체 생성
db = Database(host='your_host', user='your_username', password='your_password', db='your_db_name')

# 사용자 정보를 users 테이블에 삽입합니다.
for user_id, data in json_data.items():
    user_info = data['details']
    password = data['password']
    user_query = f"""
    INSERT INTO users (user_id, password, name, gender, age, weight, height, allergies) VALUES
    ('{user_id}', '{password}', '{user_info['name']}', '{user_info['gender']}', {user_info['age']}, {user_info['weight']}, {user_info['height']}, '{user_info['allergies']}');
    """
    db.execute_query(user_query)

    # 식단 정보를 diet 테이블에 삽입합니다.
    diet_info = data['diet']
    for date, meals in diet_info.items():
        for meal_type, foods in meals.items():
            for food in foods:
                nutrition = food['nutrition']
                diet_query = f"""
                INSERT INTO diet (user_id, date, meal_type, food_name, calories, carbs, fat, protein, sugar, sodium) VALUES
                ('{user_id}', '{date}', '{meal_type}', '{nutrition['음식 이름']}', {nutrition['칼로리']}, {nutrition['탄수화물']}, {nutrition['지방']}, {nutrition['단백질']}, {nutrition['당류']}, {nutrition['나트륨']});
                """
                db.execute_query(diet_query)
