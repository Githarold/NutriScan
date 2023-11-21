# 필요한 모듈들을 불러옵니다
from PyQt5.QtWidgets import *
from datetime import datetime
from UpdateInfoDialog import UpdateInfoDialog
from FoodTextUploadDialog import FoodTextUploadDialog
from FoodImageUploadDialog import FoodImageUploadDialog
from DietInfoDialog import DietInfoDialog
from BMRinfoDialog import BMRInfoDialog
from ExcelExporter import ExcelExporter



# Home 클래스
class Home(QDialog):
    def __init__(self, user_id, user_credentials):
        super().__init__()
        self.user_id = user_id
        self.user_credentials = user_credentials
        self.initUI()

    def initUI(self):
        user_name = self.user_credentials.get(self.user_id, {}).get('details', {}).get('name', 'Unknown User')
        self.setWindowTitle(f'{user_name}의 Home')  
        self.setGeometry(100, 100, 400, 300)  
        layout = QVBoxLayout()  



        # '음식 텍스트 업로드' 버튼
        self.upload_food_text_button = QPushButton('음식 텍스트 업로드', self)
        self.upload_food_text_button.clicked.connect(self.upload_food_text)
        layout.addWidget(self.upload_food_text_button)

        # '음식 사진 업로드' 버튼
        self.upload_food_image_button = QPushButton('음식 사진 업로드', self)
        self.upload_food_image_button.clicked.connect(self.upload_food_image)
        layout.addWidget(self.upload_food_image_button)

        # 식단 정보 확인 버튼
        self.diet_info_button = QPushButton('식단 정보 확인', self)
        self.diet_info_button.clicked.connect(self.show_diet_info)
        layout.addWidget(self.diet_info_button)

        # 체중 및 키 정보 업데이트 버튼
        self.update_info_button = QPushButton('체중 및 키 정보 업데이트', self)
        self.update_info_button.clicked.connect(self.update_info)
        layout.addWidget(self.update_info_button)

        # 기초대사량 확인 버튼
        self.nutrition_info_button = QPushButton('기초대사량 확인', self)
        self.nutrition_info_button.clicked.connect(self.show_nutrition_info)
        layout.addWidget(self.nutrition_info_button)

        # '엑셀로 내보내기' 버튼
        self.export_excel_button = QPushButton('사용자 정보 엑셀로 내보내기', self)
        self.export_excel_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_excel_button)

        self.setLayout(layout)

    def upload_food_text(self):
        dialog = FoodTextUploadDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def upload_food_image(self):
        dialog = FoodImageUploadDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def show_diet_info(self):
        diet_data = self.user_credentials.get(self.user_id, {}).get('diet', {})
        dialog = DietInfoDialog(diet_data)
        dialog.exec_()

    def update_info(self):
        dialog = UpdateInfoDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def show_nutrition_info(self):
        dialog = BMRInfoDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def export_to_excel(self):
        # ExcelExporter 다이얼로그를 생성하고 실행합니다.
        exporter_dialog = ExcelExporter(self.user_credentials)
        exporter_dialog.exec_()