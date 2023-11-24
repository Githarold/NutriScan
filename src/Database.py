import pymysql

class Database:

    # 데이터베이스 연결 설정 
    # 연결 매개변수(호스트, 사용자 이름, 비밀번호, 데이터베이스 이름)를 사용하여 데이터베이스에 연결
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          db=db,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def database_init(cls):
        return cls(host="database-1.cqviy5dwn8yf.us-east-2.rds.amazonaws.com",
                    user="admin",
                    password="pposim2023",
                    db="PPOSIM")


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
    def fetch_data(self, query):
        try:
            self.cursor.execute(query)
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


# ##############################3
# ############ FOR TEST ##############
# db = Database(host="database-1.cqviy5dwn8yf.us-east-2.rds.amazonaws.com", user="admin", password="pposim2023", db="PPOSIM")

# # 테스트용 테이블 생성
# create_table_query = """
# CREATE TABLE IF NOT EXISTS test_users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50),
#     email VARCHAR(100)
# );
# """
# db.execute_query(create_table_query)

# # 테스트용 데이터 삽입
# insert_query = "INSERT INTO test_users (username, email) VALUES (%s, %s)"
# data = ("testuser", "testuser@example.com")
# db.insert_data(insert_query, data)
# print("1")

# # 데이터 조회
# select_query = "SELECT * FROM test_users"
# results = db.fetch_data(select_query)
# for result in results:
#     print(result)
# print("2")

# # 테스트용 테이블 삭제 
# drop_table_query = "DROP TABLE test_users;"
# db.execute_query(drop_table_query)
# print("3")

# # 테이블 삭제 확인
# check_table_query = "SHOW TABLES LIKE 'test_users';"
# result = db.fetch_data(check_table_query)
# if result:
#     print("The table was not deleted.")
# else:
#     print("The table has been successfully deleted.")
# print("4")

# # 연결 종료
# db.close()
# #####################################



##################################33
# 사용 예
# 예시) db = Database(host="your_host", user="your_username", password="your_password", db="your_dbname")
# db = Database(host="database-1.cqviy5dwn8yf.us-east-2.rds.amazonaws.com", user="admin", password="pposim2023", db="PPOSIM")

# # 데이터 조회
# query = "SELECT * FROM your_table"
# results = db.fetch_data(query)
# print(results)

# # 데이터 삽입
# insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
# db.insert_data(insert_query, ("value1", "value2"))

# # 데이터 업데이트
# update_query = "UPDATE your_table SET column1 = %s WHERE id = %s"
# db.update_data(update_query, ("new_value", 1))

# # 데이터 삭제
# delete_query = "DELETE FROM your_table WHERE id = %s"
# db.delete_data(delete_query, 1)

# # 연결 종료
# db.close()
##################################


# 함수 설명 
################################
# fetch_data 메소드에서 query는 데이터를 조회하기 위한 SQL SELECT 문입니다.

# 예: "SELECT * FROM users" – 여기서 users는 데이터베이스의 테이블 이름입니다. *는 모든 컬럼을 선택하라는 의미입니다.

# insert_data 메소드에서 query는 데이터를 삽입하기 위한 SQL INSERT 문입니다.

# 예: "INSERT INTO users (name, email) VALUES (%s, %s)" – 여기서 users는 테이블 이름이고, name과 email은 컬럼 이름입니다. %s는 파라미터로 전달될 값을 위한 플레이스홀더입니다.

# update_data 메소드에서 query는 데이터를 업데이트하기 위한 SQL UPDATE 문입니다.

# 예: "UPDATE users SET name = %s WHERE id = %s" – 여기서 name은 업데이트할 컬럼이고, id는 어떤 레코드를 업데이트할지 결정하는 조건입니다.

# delete_data 메소드에서 query는 데이터를 삭제하기 위한 SQL DELETE 문입니다.

# 예: "DELETE FROM users WHERE id = %s" – 여기서 id는 삭제할 레코드를 식별하는 조건입니다.
################