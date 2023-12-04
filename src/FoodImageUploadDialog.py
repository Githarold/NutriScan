from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMessageBox, QComboBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from datetime import datetime
import requests
import webbrowser
from GetFoodNutrient import Parser

class FoodImageUploadDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('음식 사진 업로드')  
        self.setGeometry(100, 100, 300, 250)
        layout = QVBoxLayout()

        self.url_button = QPushButton('이미지 업로드 사이트', self)
        self.url_button.clicked.connect(self.open_image_upload_site)
        layout.addWidget(self.url_button)

        # 식사 시간 선택을 위한 드롭다운 메뉴
        self.meal_time_combo = QComboBox(self)
        self.meal_time_combo.addItems(['아침', '점심', '저녁'])
        layout.addWidget(self.meal_time_combo)

        self.submit_button = QPushButton('제출하기', self)
        self.submit_button.clicked.connect(self.submit_image)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def open_image_upload_site(self):
        webbrowser.open("http://110.34.114.31:5000")

    def submit_image(self):
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")

        # 사용자가 입력한 음식 이름 가져오기
        food_name = self.get_food_name_from_server()

        # 영양소 정보를 가져오기 위해 Parser 클래스 사용
        parser = Parser()
        nutritional_info = parser.get_info_openapi(food_name)

        if nutritional_info["error"]:
            QMessageBox.warning(self, '오류', nutritional_info["message"])
            return

        # 유저 식단 정보에 음식 이름과 영양소 정보 추가
        user_diet = self.user_credentials[self.user_id].setdefault('diet', {})
        daily_diet = user_diet.setdefault(current_date, {'아침': [], '점심': [], '저녁': []})
        food_info = {
            'name': food_name,
            'nutrition': nutritional_info["nutritional_info"]
        }
        daily_diet[meal_time].append(food_info)

        QMessageBox.information(self, '음식 정보 추가', f'{meal_time} 식단에 "{food_name}"이(가) 추가되었습니다.')
        self.accept()

    def get_food_name_from_server(self):
        session = requests.Session()
        response = session.get("http://110.34.114.31:5000/check")
        if response.ok:
            return response.text
        else:
            return "Unknown"  # 서버로부터 응답이 없을 경우
