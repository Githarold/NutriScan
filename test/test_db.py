import json
import pymysql
from Database import Database
import json

# JSON 데이터를 파싱합니다.
json_data = {
    'happydog': {
        'password': '123',
        'details': {
            'name': '조행복',
            'gender': '남성',
            'age': '12',
            'weight': '123',
            'height': '1234',
            'allergies': '초콜릿알레르기'
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

DB = Database()

# create_users_table_query = """
# CREATE TABLE IF NOT EXISTS users (
#     user_id VARCHAR(255) PRIMARY KEY,
#     password VARCHAR(255),
#     name VARCHAR(255),
#     gender VARCHAR(50),
#     age INT,
#     weight INT,
#     height INT,
#     allergies TEXT
# );
# """
# DB.execute_query(create_users_table_query)

# # diet 테이블 생성
# create_diet_table_query = """
# CREATE TABLE IF NOT EXISTS diet (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id VARCHAR(255),
#     date DATE,
#     meal_time VARCHAR(50),
#     food_name VARCHAR(255),
#     calories INT,
#     carbs INT,
#     fat INT,
#     protein INT,
#     sugar INT,
#     sodium INT,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );
# """
# DB.execute_query(create_diet_table_query)

# # # 사용자 정보를 users 테이블에 삽입합니다.
# for user_id, user_data in json_data.items():
#     details = user_data['details']
#     insert_user_query = "INSERT INTO users (user_id, password, name, gender, age, weight, height, allergies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#     user_values = (user_id, user_data['password'], details['name'], details['gender'], details['age'], details['weight'], details['height'], details['allergies'])
#     DB.insert_data(insert_user_query, user_values)
    
#     # 식단 정보를 diet 테이블에 삽입합니다.
#     for date, meals in user_data['diet'].items():
#         for meal_time, dishes in meals.items():
#             for dish in dishes:
#                 nutrition = dish['nutrition']
#                 insert_diet_query = "INSERT INTO diet (user_id, date, meal_time, food_name, calories, carbs, fat, protein, sugar, sodium) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#                 diet_values = (user_id, date, meal_time, nutrition['음식 이름'], nutrition['칼로리'], nutrition['탄수화물'], nutrition['지방'], nutrition['단백질'], nutrition['당류'], nutrition['나트륨'])
#                 DB.insert_data(insert_diet_query, diet_values)

# users 테이블에서 모든 사용자 정보 조회
users_query = "SELECT * FROM users"
users_data = DB.fetch_data(users_query)
print(users_data)

user_id_to_check = 'happydog'  # 예시로 사용할 사용자 ID
diet_query = "SELECT * FROM diet WHERE user_id = %s"
diet_data = DB.fetch_data(diet_query, (user_id_to_check,))

print(diet_data)
# 연결 종료
DB.close()