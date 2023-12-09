from PyQt5.QtWidgets import *
from datetime import datetime

from ManualNutritionInputDialog import ManualNutritionInputDialog
from GetFoodNutrient import Parser





class FoodTextUploadDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()
        self.info_getter = Parser()  # Initialize the Parser instance

    def initUI(self):
        self.setWindowTitle("음식 텍스트 업로드")  # Title: 'Food Text Upload'
        self.setGeometry(100, 100, 300, 200)
        self.center()  # Function call to center the window on the screen
        layout = QVBoxLayout()

        # Label and input for food name
        self.food_label = QLabel("음식 이름:", self)
        self.food_input = QLineEdit(self)
        layout.addWidget(self.food_label)
        layout.addWidget(self.food_input)

        # Label and dropdown for selecting meal time
        self.meal_time_label = QLabel("식사 시간:", self)
        self.meal_time_combo = QComboBox(self)
        self.meal_time_combo.addItems(
            ["아침", "점심", "저녁"]
        )  # Items: 'Breakfast', 'Lunch', 'Dinner'
        layout.addWidget(self.meal_time_label)
        layout.addWidget(self.meal_time_combo)

        # Button for submitting food text
        self.submit_button = QPushButton("음식 텍스트 업로드", self)
        self.submit_button.clicked.connect(self.submit_food)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_food(self):
        # Get food name and meal time from user input
        food_name = self.food_input.text()
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")

        if not food_name:
            QMessageBox.warning(
                self, "입력 오류", "음식 이름을 입력해주세요."
            )  # 'Input Error: Please enter the food name'
            return

        # Retrieve nutritional information using OpenAPI
        nutritional_info = self.query_nutritional_info(food_name)
        if nutritional_info.get("error"):
            # If info not found in OpenAPI, open manual input dialog
            manual_input_dialog = ManualNutritionInputDialog(food_name)
            if manual_input_dialog.exec_():
                food_info = {
                    "칼로리": manual_input_dialog.calories_input.text(),
                    "탄수화물": manual_input_dialog.carbs_input.text(),
                    "지방": manual_input_dialog.fat_input.text(),
                    "단백질": manual_input_dialog.protein_input.text(),
                    "당류": manual_input_dialog.sugar_input.text(),
                    "나트륨": manual_input_dialog.sodium_input.text(),
                }
            else:
                return  # Exit if user cancels input
        else:
            # If info is found in OpenAPI
            food_info = nutritional_info["nutritional_info"]

        # Update user's diet information
        user_diet = self.user_credentials[self.user_id].setdefault("diet", {})
        daily_diet = user_diet.setdefault(current_date, {"아침": [], "점심": [], "저녁": []})
        food_entry = {"name": food_name, "nutrition": food_info}
        daily_diet[meal_time].append(food_entry)

        QMessageBox.information(
            self, "음식 업로드", f'{meal_time} 식단에 "{food_name}"이(가) 추가되었습니다.'
        )  # 'Food Uploaded'
        self.accept()

    def query_nutritional_info(self, food_name):
        # Retrieve nutritional information using the Parser class
        return self.info_getter.get_info_openapi(food_name)

    def center(self):
        # Center the dialog on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
