# 필요한 모듈들을 불러옵니다
from PyQt5.QtWidgets import *
import os
from datetime import datetime
from UpdateInfoDialog import UpdateInfoDialog
from FoodTextUploadDialog import FoodTextUploadDialog
from FoodImageUploadDialog import FoodImageUploadDialog
from DietInfoDialog import DietInfoDialog
from BMRinfoDialog import BMRInfoDialog
from ExcelExporter import ExcelExporter
from FoodRecommendationDialog import FoodRecommendationDialog
from Database import Database
import json

# Home 클래스
class Home(QDialog):
    def __init__(self, user_id, user_credentials):
        super().__init__()
        self.user_id = user_id
        self.user_credentials = user_credentials
        self.initUI()
        self.db = Database()

    def initUI(self):
        user_name = self.user_credentials.get(self.user_id, {}).get('details', {}).get('name', 'Unknown User')
        self.setWindowTitle(f'{user_name}의 Home')  
        self.setGeometry(100, 100, 400, 300) 
        self.center()  # 화면 중앙에 위치시키는 함수 호출 
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

        # '음식 추천 받기' 버튼
        self.recommend_food_button = QPushButton('음식 추천 받기', self)
        self.recommend_food_button.clicked.connect(self.open_food_recommendation_dialog)
        layout.addWidget(self.recommend_food_button)

        # '시스템 종료하기' 버튼
        self.exit_system_button = QPushButton('시스템 종료하기', self)
        self.exit_system_button.clicked.connect(self.export_credentials_and_exit)
        layout.addWidget(self.exit_system_button)

        self.setLayout(layout)

    def upload_food_text(self):
        dialog = FoodTextUploadDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def upload_food_image(self):
        dialog = FoodImageUploadDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def show_diet_info(self):
        diet_data = self.user_credentials.get(self.user_id, {}).get('diet', {})
        dialog = DietInfoDialog(diet_data, self.user_id)
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

    def open_food_recommendation_dialog(self):
        dialog = FoodRecommendationDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def export_credentials_and_exit(self):
        self.export_user_credentials()
        self.close()  # 다이얼로그 닫기

    def export_user_credentials(self):
        # 데이터베이스 객체 생성
        db = Database()
        # user_credentials 데이터베이스에 저장
        db.save_user_credentials(self.user_credentials)
        # 데이터베이스 연결 종료
        db.close()
        QMessageBox.information(self, '정보 내보내기', '사용자 정보가 데이터베이스에 저장되었습니다.')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())