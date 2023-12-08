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

# Home class definition
class Home(QDialog):
    # Constructor for the Home class
    def __init__(self, user_id, user_credentials):
        super().__init__()
        self.user_id = user_id
        self.user_credentials = user_credentials
        self.initUI()
        self.db = Database()

    def initUI(self):
        # Initializes the UI components of the Home dialog
        user_name = (
            self.user_credentials.get(self.user_id, {})
            .get("details", {})
            .get("name", "Unknown User")
        )
        self.setWindowTitle(f"{user_name}의 Home")
        self.setGeometry(100, 100, 400, 300)
        self.center()  # Call function to center the dialog on screen
        layout = QVBoxLayout()

        # Button for uploading food text
        self.upload_food_text_button = QPushButton("음식 텍스트 업로드", self)
        self.upload_food_text_button.clicked.connect(self.upload_food_text)
        layout.addWidget(self.upload_food_text_button)

        # Button for uploading food images
        self.upload_food_image_button = QPushButton("음식 사진 업로드", self)
        self.upload_food_image_button.clicked.connect(self.upload_food_image)
        layout.addWidget(self.upload_food_image_button)

        # Button to view diet information
        self.diet_info_button = QPushButton("식단 정보 확인", self)
        self.diet_info_button.clicked.connect(self.show_diet_info)
        layout.addWidget(self.diet_info_button)

        # Button to update weight, height, and age information
        self.update_info_button = QPushButton("체중, 키 및 나이 정보 업데이트", self)
        self.update_info_button.clicked.connect(self.update_info)
        layout.addWidget(self.update_info_button)

        # Button to check Basal Metabolic Rate (BMR) information
        self.nutrition_info_button = QPushButton("기초대사량 확인", self)
        self.nutrition_info_button.clicked.connect(self.show_nutrition_info)
        layout.addWidget(self.nutrition_info_button)

        # Button to export user information to Excel
        self.export_excel_button = QPushButton("사용자 정보 엑셀로 내보내기", self)
        self.export_excel_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_excel_button)

        # Button to receive food recommendations
        self.recommend_food_button = QPushButton("음식 추천 받기", self)
        self.recommend_food_button.clicked.connect(self.open_food_recommendation_dialog)
        layout.addWidget(self.recommend_food_button)

        # Button to exit the system
        self.exit_system_button = QPushButton("시스템 종료하기", self)
        self.exit_system_button.clicked.connect(self.export_credentials_and_exit)
        layout.addWidget(self.exit_system_button)

        self.setLayout(layout)

    def upload_food_text(self):
        # Function to handle food text upload
        dialog = FoodTextUploadDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def upload_food_image(self):
        # Function to handle food image upload
        dialog = FoodImageUploadDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def show_diet_info(self):
        # Function to display diet information
        diet_data = self.user_credentials.get(self.user_id, {}).get("diet", {})
        dialog = DietInfoDialog(diet_data, self.user_id)
        dialog.exec_()

    def update_info(self):
        # Function to update user's weight, height, and age information
        dialog = UpdateInfoDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def show_nutrition_info(self):
        # Function to display BMR information
        dialog = BMRInfoDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def export_to_excel(self):
        # Function to export data to an Excel file
        # Create and execute ExcelExporter dialog
        exporter_dialog = ExcelExporter(self.user_credentials)
        exporter_dialog.exec_()

    def open_food_recommendation_dialog(self):
        # Function to open food recommendation dialog
        dialog = FoodRecommendationDialog(self.user_credentials, self.user_id)
        dialog.exec_()

    def export_credentials_and_exit(self):
        # Function to export user credentials and exit
        self.export_user_credentials()
        self.close()  # Close the dialog

    def export_user_credentials(self):
        # Function to export user credentials
        # Create Database object
        db = Database()
        # Save user_credentials to database
        db.save_user_credentials(self.user_credentials)
        # Close database connection
        db.close()
        QMessageBox.information(self, "정보 내보내기", "사용자 정보가 데이터베이스에 저장되었습니다.")

    def center(self):
        # Function to center the dialog on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
