import pymysql

class Database:

    def __init__(self):
        self.connection = pymysql.connect(host="database-1.cqviy5dwn8yf.us-east-2.rds.amazonaws.com",
                                          user="admin",
                                          password="pposim2023",
                                          db="PPOSIM",
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    # 쿼리 실행
    # SQL 쿼리를 실행하는 함수를 정의
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    # 데이터 조회
    # 데이터베이스에서 데이터를 조회하고 결과를 반환하는 함수를 정의
    def fetch_data(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    # 데이터 삽입 
    # 데이터베이스에 새로운 레코드를 삽입하는 함수를 정의
    def insert_data(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    # 데이터 업데이트 
    # 데이터베이스의 기존 레코드를 업데이트하는 함수를 정의
    def update_data(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    # 데이터 삭제
    # 데이터베이스에서 레코드를 삭제하는 함수를 정의
    def delete_data(self, query, id):
        try:
            self.cursor.execute(query, (id,))
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    # 연결 종료
    # 데이터베이스 연결을 안전하게 종료하는 함수를 정의  
    def close(self):
        self.cursor.close()
        self.connection.close()

    # 모든 사용자 정보 조회 
    # return value : dictionary
    def fetch_all_users(self):
        query = "SELECT * FROM users"
        users = self.fetch_data(query)
        users_dict = {user['user_id']: user for user in users}
        return users_dict
    
    # 특정 사용자 존재 유무 확인
    # return value : list (존재 : list, 없음 : None)
    def check_user_exists(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result
    
    # 회원가입한 유저 DB에 추가
    # return value : bool (성공 : True, 실패 : False)
    def add_new_user(self, user_id, password):
            query = "INSERT INTO users (user_id, password) VALUES (%s, %s)"
            try:
                self.cursor.execute(query, (user_id, password))
                self.connection.commit()
                return True  # 사용자 추가 성공
            except pymysql.MySQLError as e:
                print(f"An error occurred: {e}")
                self.connection.rollback()
                return False  # 사용자 추가 실패
    
    # 로그인한 유저 모든 데이터 load
    # return value : list (user data + diet data)
    def fetch_user_data(self, user_id):
        # 사용자 정보 조회
        user_info_query = "SELECT * FROM users WHERE user_id = %s"
        user_info = self.fetch_data(user_info_query, (user_id,))
        
        # 사용자 정보가 없는 경우 빈 딕셔너리 반환
        if not user_info:
            return {user_id: {}}
        
        # 조회된 사용자 정보 딕셔너리 생성
        user_data = {
            'password': user_info[0]['password'],
            'details': {
                'name': user_info[0]['name'],
                'gender': user_info[0]['gender'],
                'age': user_info[0]['age'],
                'weight': user_info[0]['weight'],
                'height': user_info[0]['height'],
                'allergies': user_info[0]['allergies']
            },
            'diet': {}
        }

        # 식단 정보 조회
        diet_query = "SELECT * FROM diet WHERE user_id = %s"
        diet_data = self.fetch_data(diet_query, (user_id,))

        # 식단 정보를 사용자 정보 딕셔너리에 추가
        for item in diet_data:
            date = item['date'].strftime('%Y-%m-%d')  # datetime 객체를 문자열로 변환
            meal_time = item['meal_time']
            food_name = item['food_name']
            nutrition = {
                '음식 이름': food_name,
                '칼로리': item['calories'],
                '탄수화물': item['carbs'],
                '지방': item['fat'],
                '단백질': item['protein'],
                '당류': item['sugar'],
                '나트륨': item['sodium']
            }
            
            # 날짜 키가 없으면 초기화
            if date not in user_data['diet']:
                user_data['diet'][date] = {'아침': [], '점심': [], '저녁': []}
            
            # 해당 식사 시간에 음식 정보 추가
            user_data['diet'][date][meal_time].append({
                'name': food_name,
                'nutrition': nutrition
            })

        return {user_id: user_data}  # 사용자 ID를 최상위 키로 사용하여 반환
