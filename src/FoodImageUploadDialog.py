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

        self.manual_input_button = QPushButton('직접 입력하기', self)
        self.manual_input_button.clicked.connect(self.open_manual_nutrition_input_dialog)
        layout.addWidget(self.manual_input_button)


        self.setLayout(layout)

    def open_image_upload_site(self):
        #webbrowser.open("http://110.34.114.31:5000")
        webbrowser.open("http://10.0.33.229:5000")
    def submit_image(self):
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # 사용자가 입력한 음식 이름 가져오기
            food_name = self.get_food_name_from_server()
        except requests.exceptions.ConnectionError:
            # 서버 연결 실패 시 직접 입력 옵션 제공
            self.open_manual_nutrition_input_dialog()
            return

        # 영양소 정보를 가져오기 위해 Parser 클래스 사용
        parser = Parser()
        nutritional_info = parser.get_info_openapi(food_name)

        if nutritional_info["error"]:
            # 영양소 정보를 찾지 못했을 경우 직접 입력 다이얼로그 열기
            self.open_manual_nutrition_input_dialog(food_name)
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
        response = session.get("http://10.0.33.229:5000/check")
        if response.ok:
            # 음식 이름을 띄어쓰기로 구분하여 리스트로 반환
            return response.text.split(' ')
        else:
            return ["Unknown"]  # 서버로부터 응답이 없을 경우 기본값 반환

    def submit_image(self):
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")
        food_names = self.get_food_name_from_server()

        for food_name in food_names:
            if not food_name.strip():
                continue  # 빈 이름 무시

            nutritional_info = self.query_nutritional_info(food_name)
            if nutritional_info.get('error'):
                # 영양소 정보를 찾지 못했을 경우 직접 입력 다이얼로그 열기
                if not self.open_manual_nutrition_input_dialog(food_name):
                    continue  # 사용자가 입력을 취소함
            else:
                # OpenAPI에서 정보를 찾은 경우
                self.save_nutrition_info(food_name, nutritional_info["nutritional_info"])

        QMessageBox.information(self, '음식 정보 추가', f'{meal_time} 식단에 입력된 음식들이 추가되었습니다.')
        self.accept()

    def open_manual_nutrition_input_dialog(self, food_name):
        dialog = ManualNutritionInputDialog(food_name)
        if dialog.exec_():
            nutrition_info = dialog.get_nutrition_info()
            self.save_nutrition_info(food_name, {
                '칼로리': float(nutrition_info['calories']),
                '탄수화물': float(nutrition_info['carbs']),
                '지방': float(nutrition_info['fat']),
                '단백질': float(nutrition_info['protein']),
                '당류': float(nutrition_info['sugar']),
                '나트륨': float(nutrition_info['sodium'])
            })
            return True
        return False

    def save_nutrition_info(self, food_name, nutrition_info):
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")
        user_diet = self.user_credentials[self.user_id].setdefault('diet', {})
        daily_diet = user_diet.setdefault(current_date, {'아침': [], '점심': [], '저녁': []})
        food_info = {
            'name': food_name,
            'nutrition': nutrition_info
        }
        daily_diet[meal_time].append(food_info)

        QMessageBox.information(self, '영양 정보 추가', f'{meal_time} 식단에 "{food_name}"의 영양 정보가 추가되었습니다.')

    def query_nutritional_info(self, food_name):
        # Parser 클래스를 사용하여 OpenAPI로부터 영양 정보 조회
        parser = Parser()
        return parser.get_info_openapi(food_name)