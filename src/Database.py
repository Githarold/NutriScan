import pymysql


class Database:
    def __init__(self):
        # Establishes a connection to the database with the specified parameters.
        self.connection = pymysql.connect(
            host="database-1.cqviy5dwn8yf.us-east-2.rds.amazonaws.com",
            user="admin",
            password="pposim2023",
            db="PPOSIM",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        # Executes a given query with optional parameters and handles exceptions.
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    def fetch_data(self, query, params=None):
        # Fetches data from the database based on the given query and parameters.
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def insert_data(self, query, data):
        # Inserts data into the database based on the given query and data.
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    def update_data(self, query, data):
        # Updates existing data in the database based on the given query and data.
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    def close(self):
        # Closes the database connection.
        self.cursor.close()
        self.connection.close()

    def check_user_exists(self, user_id):
        # Checks if a user exists in the database based on the user ID.
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result

    def add_new_user(self, user_id, password):
        # Define the SQL query to insert a new user into the 'users' table.
        query = "INSERT INTO users (user_id, password) VALUES (%s, %s)"
        try:
            # Execute the SQL query with the provided user_id and password.
            self.cursor.execute(query, (user_id, password))
            # Commit the transaction to the database.
            self.connection.commit()
            return True  # Return True to indicate success.
        except pymysql.MySQLError as e:
            # Print the error if the SQL operation fails.
            print(f"An error occurred: {e}")
            # Rollback the transaction in case of error.
            self.connection.rollback()
            return False  # Return False to indicate failure.

    def fetch_user_data(self, user_id):
        # Fetches specific data for a user based on the user ID.
        user_info_query = "SELECT * FROM users WHERE user_id = %s"
        user_info = self.fetch_data(user_info_query, (user_id,))

        if not user_info:
            return {user_id: {}}

        # Formats the fetched user data.
        user_data = {
            "password": user_info[0]["password"],
            "details": {
                "name": user_info[0]["name"],
                "gender": user_info[0]["gender"],
                "age": user_info[0]["age"],
                "weight": user_info[0]["weight"],
                "height": user_info[0]["height"],
                "allergies": user_info[0]["allergies"],
            },
            "diet": {},
        }

        diet_query = "SELECT * FROM diet WHERE user_id = %s"
        diet_data = self.fetch_data(diet_query, (user_id,))

        for item in diet_data:
            date = item["date"].strftime("%Y-%m-%d")
            meal_time = item["meal_time"]
            food_name = item["food_name"]
            nutrition = {
                "음식 이름": food_name,
                "칼로리": item["calories"],
                "탄수화물": item["carbs"],
                "지방": item["fat"],
                "단백질": item["protein"],
                "당류": item["sugar"],
                "나트륨": item["sodium"],
            }

            if date not in user_data["diet"]:
                user_data["diet"][date] = {"아침": [], "점심": [], "저녁": []}

            user_data["diet"][date][meal_time].append(
                {"name": food_name, "nutrition": nutrition}
            )

        return {user_id: user_data}

    def update_user_details(self, user_id, user_details):
        # Updates the details of an existing user in the database.
        query = """
        UPDATE users SET name=%s, gender=%s, age=%s, weight=%s, height=%s, allergies=%s
        WHERE user_id=%s
        """
        data = (
            user_details["name"],
            user_details["gender"],
            user_details["age"],
            user_details["weight"],
            user_details["height"],
            user_details["allergies"],
            user_id,
        )
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return False

    def save_user_credentials(self, user_credentials):
        # Saves multiple user credentials in the database.
        for user_id, credentials in user_credentials.items():
            user_details = credentials.get("details", {})
            name = user_details.get("name", "")
            gender = user_details.get("gender", "")
            age = user_details.get("age", 0)
            weight = user_details.get("weight", 0)
            height = user_details.get("height", 0)
            allergies = user_details.get("allergies", "")

            if self.check_user_exists(user_id):
                # Updates existing user details.
                update_query = """
                UPDATE users SET name=%s, gender=%s, age=%s, weight=%s, height=%s, allergies=%s
                WHERE user_id=%s
                """
                self.update_data(
                    update_query,
                    (name, gender, age, weight, height, allergies, user_id),
                )
            else:
                # Inserts new user data.
                insert_query = """
                INSERT INTO users (user_id, password, name, gender, age, weight, height, allergies) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                password = credentials.get("password", "")
                self.insert_data(
                    insert_query,
                    (user_id, password, name, gender, age, weight, height, allergies),
                )

            delete_diet_query = "DELETE FROM diet WHERE user_id = %s"
            self.execute_query(delete_diet_query, (user_id,))

            for date, meals in credentials.get("diet", {}).items():
                for meal_time, foods in meals.items():
                    for food in foods:
                        # Inserts diet data for each food item.
                        insert_query = """
                        INSERT INTO diet (user_id, date, meal_time, food_name, calories, carbs, fat, protein, sugar, sodium)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        nutrition = food["nutrition"]
                        diet_data = (
                            user_id,
                            date,
                            meal_time,
                            food["name"],
                            nutrition["칼로리"],
                            nutrition["탄수화물"],
                            nutrition["지방"],
                            nutrition["단백질"],
                            nutrition["당류"],
                            nutrition["나트륨"],
                        )
                        self.insert_data(insert_query, diet_data)
