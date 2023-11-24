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
        users = self.fetch_data("SELECT * FROM users")
        users_dict = {user['user_id']: user for user in users}
        return users_dict