from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from datetime import datetime
import requests
import webbrowser
from GetFoodNutrient import Parser
from ManualNutritionInputDialog1 import ManualNutritionInputDialog


# Class for the food image upload dialog
class FoodImageUploadDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials  # User authentication information
        self.user_id = user_id  # User ID
        self.initUI()

    def initUI(self):
        # Initialize the user interface for the dialog
        self.setWindowTitle("음식 사진 업로드")  # Title of the dialog
        self.setGeometry(100, 100, 300, 250)  # Set geometry of the dialog
        self.center()  # Center the dialog on the screen
        layout = QVBoxLayout()  # Use vertical box layout

        # Button to open the image upload site
        self.url_button = QPushButton("이미지 업로드 사이트", self)
        self.url_button.clicked.connect(self.open_image_upload_site)
        layout.addWidget(self.url_button)

        # Combo box for selecting meal time
        self.meal_time_combo = QComboBox(self)
        self.meal_time_combo.addItems(["아침", "점심", "저녁"])  # Morning, Afternoon, Evening
        layout.addWidget(self.meal_time_combo)

        # Button for submitting the image
        self.submit_button = QPushButton("제출하기", self)
        self.submit_button.clicked.connect(self.submit_image)
        layout.addWidget(self.submit_button)

        # Button for manual nutrition input
        self.manual_input_button = QPushButton("직접 입력하기", self)
        self.manual_input_button.clicked.connect(
            self.open_manual_nutrition_input_dialog
        )
        layout.addWidget(self.manual_input_button)

        self.setLayout(layout)  # Set the layout for the dialog

    def open_image_upload_site(self):
        # Function to open the image upload site in a web browser
        # webbrowser.open("http://110.34.114.31:5000")
        try:
            webbrowser.open("http://110.34.114.31:5000")
        except Exception as e:
            QMessageBox.critical(self, "연결 실패", "웹페이지에 연결할 수 없습니다.\n" + str(e))

    def submit_image(self):
        meal_time = self.meal_time_combo.currentText()  # 선택된 식사 시간
        current_date = datetime.now().strftime("%Y-%m-%d")  # 현재 날짜
        info_added = False  # 추가된 정보가 있는지 추적

        try:
            food_names = self.get_food_name_from_server()  # 서버에서 음식 이름 가져오기

            if not food_names or all(not name.strip() for name in food_names):
                QMessageBox.warning(self, "오류", "음식이 인식되지 않았습니다.")
                return

            for food_name in food_names:
                if not food_name.strip():
                    continue  # 빈 이름 건너뛰기

                nutritional_info = self.query_nutritional_info(food_name)  # 영양 정보 조회

                if nutritional_info.get("error"):
                    if self.open_manual_nutrition_input_dialog(food_name):
                        info_added = True  # 수동 입력 성공 시
                    else:
                        continue  # 수동 입력 취소 시 다음 음식으로 넘어감
                else:
                    self.save_nutrition_info(food_name, nutritional_info["nutritional_info"])  # 영양 정보 저장
                    info_added = True

            if info_added:
                QMessageBox.information(self, "음식 정보 추가", f"{meal_time} 식단에 입력된 음식들이 추가되었습니다.")
                self.accept()  # 대화 상자 닫기

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "연결 실패", "웹 서버에 연결할 수 없습니다.\n" + str(e))
            if self.open_manual_nutrition_input_dialog():
                QMessageBox.information(self, "음식 정보 추가", f"{meal_time} 식단에 입력된 음식들이 추가되었습니다.")
                self.accept()  # 대화 상자 닫기

    
    def get_food_name_from_server(self):
            try:
                session = requests.Session()
                response = session.get("http://110.34.114.31:5000/check", timeout=5)  # 5초 타임아웃 설정
                if response.ok:
                    return response.text.split(" ")
                else:
                    return ["Unknown"]
            except requests.exceptions.Timeout:
                # 타임아웃 발생 시
                QMessageBox.critical(self, "연결 실패", "서버로부터 응답이 없습니다. 네트워크 연결을 확인해주세요.")
                return ["Unknown"]
            except requests.exceptions.RequestException as e:
                # 기타 요청 예외 발생 시
                QMessageBox.critical(self, "연결 실패", "웹 서버에 연결할 수 없습니다.\n" + str(e))
                return ["Unknown"]

    def open_manual_nutrition_input_dialog(self, pre_filled_food_name=None):
        # Open a dialog for manual input of nutrition information
        food_name, ok = QInputDialog.getText(self, "음식 이름 입력", "음식 이름을 입력하세요:", text=pre_filled_food_name or "")
        if ok and food_name:
            nutritional_info = self.query_nutritional_info(food_name)
            if not nutritional_info.get("error"):
                self.save_nutrition_info(food_name, nutritional_info["nutritional_info"])
            else:
               # Open a dialog for manual input if there's an error in fetching data
                dialog = ManualNutritionInputDialog(food_name)
                if dialog.exec_():
                    nutrition_info = dialog.get_nutrition_info()
                    self.save_nutrition_info(food_name, {
                        "칼로리": float(nutrition_info["calories"]),
                        "탄수화물": float(nutrition_info["carbs"]),
                        "지방": float(nutrition_info["fat"]),
                        "단백질": float(nutrition_info["protein"]),
                        "당류": float(nutrition_info["sugar"]),
                        "나트륨": float(nutrition_info["sodium"]),
                    })
                    return True
        return False
    

    def save_nutrition_info(self, food_name, nutrition_info):
        # Save the nutritional information of a food item
        meal_time = self.meal_time_combo.currentText()  # Get the selected meal time
        current_date = datetime.now().strftime("%Y-%m-%d")  # Get the current date
        # Retrieve or initialize the user's diet information
        user_diet = self.user_credentials[self.user_id].setdefault("diet", {})
        daily_diet = user_diet.setdefault(current_date, {"아침": [], "점심": [], "저녁": []})
        # Prepare the food information
        food_info = {"name": food_name, "nutrition": nutrition_info}
        daily_diet[meal_time].append(food_info)  # Add the food information to the diet
        # Show a message box with the added nutrition information
        QMessageBox.information(
            self, "영양 정보 추가", f'{meal_time} 식단에 "{food_name}"의 영양 정보가 추가되었습니다.'
        )
        self.save_food_name_to_user_credentials(
            food_name
        )  # Update user credentials with the food name

    def save_food_name_to_user_credentials(self, food_name):
        # Save the food name to the user's credentials
        user_foods = self.user_credentials[self.user_id].setdefault("foods", [])
        # Add the food name to the list if it's not already there
        if food_name not in user_foods:
            user_foods.append(food_name)

    def query_nutritional_info(self, food_name):
        # Query nutritional information for a given food name
        parser = Parser()  # Create a Parser object
        return parser.get_info_openapi(
            food_name
        )  # Use the parser to fetch nutritional info from an API

    def center(self):
        # Center the dialog on the screen
        qr = self.frameGeometry()  # Get the geometry of the dialog
        cp = (
            QDesktopWidget().availableGeometry().center()
        )  # Get the center point of the desktop
        qr.moveCenter(cp)  # Move the dialog's center to the desktop's center
        self.move(
            qr.topLeft()
        )  # Move the dialog to the top-left of the centered geometry