from PyQt5.QtWidgets import *

class BMRInfoDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('기초대사량 정보')  
        self.setGeometry(100, 100, 300, 200)  
        layout = QVBoxLayout()  

        # BMR 정보 표시 레이블
        self.bmr_label = QLabel(self)
        layout.addWidget(self.bmr_label)

        self.calculate_and_display_bmr()
        self.setLayout(layout)

    def calculate_and_display_bmr(self):
        user_details = self.user_credentials.get(self.user_id, {}).get('details', {})
        age = int(user_details.get('age', 0))
        weight = float(user_details.get('weight', 0))
        height = float(user_details.get('height', 0))
        gender = user_details.get('gender', '남성')

        if age == 0 or weight == 0 or height == 0:
            self.bmr_label.setText('나이, 체중, 키 정보가 필요합니다.')
            return

        bmr = self.calculate_bmr(gender, age, weight, height)
        self.bmr_label.setText(f'기초대사량: {bmr} kcal')

    def calculate_bmr(self, gender, age, weight, height):
        if gender == '남성':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == '여성':
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            bmr = (88.362 + 447.593) / 2 + ((13.397 + 9.247) / 2 * weight) + ((4.799 + 3.098) / 2 * height) - ((5.677 + 4.330) / 2 * age)
        return round(bmr, 2)
