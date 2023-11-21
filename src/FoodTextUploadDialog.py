from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from datetime import datetime
import pandas as pd
from ManualNutritionInputDialog import ManualNutritionInputDialog

def search_food_nutrition(file_path, food_name):
    # 엑셀 파일을 DataFrame으로 읽기
    df = pd.read_excel(file_path)

    # 음식 이름으로 검색
    result = df[df['음식 이름'] == food_name]
    if not result.empty:
        return result.iloc[0].to_dict()
    else:
        return None

class FoodTextUploadDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('음식 텍스트 업로드')  
        self.setGeometry(100, 100, 300, 200)  
        layout = QVBoxLayout()  

        self.food_label = QLabel('음식 이름:', self)
        self.food_input = QLineEdit(self)
        layout.addWidget(self.food_label)
        layout.addWidget(self.food_input)

        self.meal_time_label = QLabel('식사 시간:', self)
        self.meal_time_combo = QComboBox(self)
        self.meal_time_combo.addItems(['아침', '점심', '저녁'])
        layout.addWidget(self.meal_time_label)
        layout.addWidget(self.meal_time_combo)

        self.submit_button = QPushButton('음식 텍스트 업로드', self)
        self.submit_button.clicked.connect(self.submit_food)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_food(self):
        food_name = self.food_input.text()
        meal_time = self.meal_time_combo.currentText()
        current_date = datetime.now().strftime("%Y-%m-%d")

        if not food_name:
            QMessageBox.warning(self, '입력 오류', '음식 이름을 입력해주세요.')
            return

        # 음식 정보 검색
        food_info = search_food_nutrition('/Users/you-seungwon/Desktop/sbjb2/nutritioninfo.xlsx', food_name)
        if not food_info:
            # 영양 정보 수동 입력 대화상자 열기
            manual_input_dialog = ManualNutritionInputDialog(food_name)
            if manual_input_dialog.exec_():
                food_info = {
                    '칼로리': manual_input_dialog.calories_input.text(),
                    '탄수화물': manual_input_dialog.carbs_input.text(),
                    '지방': manual_input_dialog.fat_input.text(),
                    '단백질': manual_input_dialog.protein_input.text()
                }
            else:
                return  # 사용자가 입력을 취소함

        # 유저 식단 정보 업데이트
        user_diet = self.user_credentials[self.user_id].setdefault('diet', {})
        daily_diet = user_diet.setdefault(current_date, {'아침': [], '점심': [], '저녁': []})
        food_entry = {
            'name': food_name,
            'nutrition': food_info
        }
        daily_diet[meal_time].append(food_entry)

        QMessageBox.information(self, '음식 업로드', f'{meal_time} 식단에 "{food_name}"이(가) 추가되었습니다.')
        self.accept()
