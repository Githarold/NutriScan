from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from datetime import datetime
import requests
import webbrowser
from GetFoodNutrient import Parser
from ManualNutritionInputDialog1 import ManualNutritionInputDialog


class FoodImageUploadDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("음식 사진 업로드")  # Title: 'Upload Food Image'
        self.setGeometry(100, 100, 300, 250)
        self.center()  # Function call to center the window on the screen
        layout = QVBoxLayout()

        # Button to open the image upload site
        self.url_button = QPushButton("이미지 업로드 사이트", self)
        self.url_button.clicked.connect(self.open_image_upload_site)
        layout.addWidget(self.url_button)

        # Dropdown menu for selecting meal time
        self.meal_time_combo = QComboBox(self)
        self.meal_time_combo.addItems(
            ["아침", "점심", "저녁"]
        )  # Items: 'Breakfast', 'Lunch', 'Dinner'
        layout.addWidget(self.meal_time_combo)

        # Button to submit the image
        self.submit_button = QPushButton("제출하기", self)  # 'Submit'
        self.submit_button.clicked.connect(self.submit_image)
        layout.addWidget(self.submit_button)

        # Button for manual nutrition input
        self.manual_input_button = QPushButton("직접 입력하기", self)  # 'Enter Manually'
        self.manual_input_button.clicked.connect(
            self.open_manual_nutrition_input_dialog
        )
        layout.addWidget(self.manual_input_button)

        self.setLayout(layout)

    def open_image_upload_site(self):
        # Open the image upload website in a web browser
        webbrowser.open("http://10.0.33.229:5000")

    def submit_image(self):
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Retrieves the food name entered by the user from the server
        try:
            food_name = self.get_food_name_from_server()
        except requests.exceptions.ConnectionError:
            # If server connection fails, provide an option for manual entry
            self.open_manual_nutrition_input_dialog()
            return

        # Use the Parser class to fetch nutritional information
        parser = Parser()
        nutritional_info = parser.get_info_openapi(food_name)

        if nutritional_info["error"]:
            # If nutritional information is not found, open the manual input dialog
            self.open_manual_nutrition_input_dialog(food_name)
            return

        # Add food name and nutrition info to user's diet data
        user_diet = self.user_credentials[self.user_id].setdefault("diet", {})
        daily_diet = user_diet.setdefault(current_date, {"아침": [], "점심": [], "저녁": []})
        food_info = {
            "name": food_name,
            "nutrition": nutritional_info["nutritional_info"],
        }
        daily_diet[meal_time].append(food_info)

        QMessageBox.information(
            self, "음식 정보 추가", f'{meal_time} 식단에 "{food_name}"이(가) 추가되었습니다.'
        )  # 'Food Information Added'
        self.accept()

    def get_food_name_from_server(self):
        # Create a session to make a request to the server
        session = requests.Session()
        response = session.get("http://10.0.33.229:5000/check")
        if response.ok:
            # Return the food name as a list, splitting by space
            return response.text.split(" ")
        else:
            # Return a default value if no response from the server
            return ["Unknown"]

    # Additional methods (submit_image, open_manual_nutrition_input_dialog, save_nutrition_info, save_food_name_to_user_credentials, query_nutritional_info) follow the same pattern as described above

    def center(self):
        # Method to center the dialog on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
