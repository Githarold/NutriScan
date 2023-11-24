from PyQt5.QtWidgets import *
import json
from datetime import datetime

class FoodRecommendationDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('음식 추천')  
        self.setGeometry(200, 200, 300, 200)  
        layout = QVBoxLayout()  

        # 텍스트 라벨
        self.recommendation_label = QLabel('오늘의 추천 음식', self)
        layout.addWidget(self.recommendation_label)

        # 사용자 섭취량 라벨
        user_name = self.user_credentials.get(self.user_id, {}).get('details', {}).get('name', 'Unknown User')
        total_calories = self.calculate_total_calories()
        self.intake_label = QLabel(f"오늘 {user_name}님의 섭취량은 {total_calories} 칼로리입니다.", self)
        layout.addWidget(self.intake_label)

        # '남은 섭취량' 라벨 추가
        remaining_intake = self.calculate_remaining_intake()
        self.remaining_intake_label = QLabel(f"{self.get_user_name()}님의 현재 남은 섭취량은 {remaining_intake}칼로리입니다.", self)
        layout.addWidget(self.remaining_intake_label)
        
        # '영양소별 남은 섭취량' 라벨 추가
        remaining_nutrients = self.calculate_remaining_nutrient_intake()
        self.remaining_nutrition_intake_label = QLabel(
            f"남은 탄수화물: {remaining_nutrients['carbs']}g, "
            f"단백질: {remaining_nutrients['protein']}g, "
            f"지방: {remaining_nutrients['fats']}g", self)
        layout.addWidget(self.remaining_nutrition_intake_label)


        # '음식 추천 받기' 버튼
        self.get_recommendation_button = QPushButton('음식 추천 받기', self)
        self.get_recommendation_button.clicked.connect(self.on_recommendation_button_clicked)
        layout.addWidget(self.get_recommendation_button)

        self.setLayout(layout)

    def calculate_total_calories(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        user_diet = self.user_credentials.get(self.user_id, {}).get('diet', {})

        total_calories = 0
        for meal, foods in user_diet.get(current_date, {}).items():
            for food in foods:
                if isinstance(food, dict):
                    calories = food.get('nutrition', {}).get('칼로리', 0)
                    try:
                        total_calories += int(calories)
                    except ValueError:
                        pass  # 정수가 아닌 칼로리 값 처리

        return total_calories

    def calculate_bmr(self):
        user_details = self.user_credentials.get(self.user_id, {}).get('details', {})
        gender = user_details.get('gender', 'N/A')
        try:
            age = float(user_details.get('age', 0))
            weight = float(user_details.get('weight', 0))
            height = float(user_details.get('height', 0))
        except ValueError:
            age = weight = height = 0  # 변환 실패 시 기본값 처리

        if gender == '남성':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == '여성':
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            bmr = (88.362 + 447.593) / 2 + ((13.397 + 9.247) / 2 * weight) + ((4.799 + 3.098) / 2 * height) - ((5.677 + 4.330) / 2 * age)
        return round(bmr, 2)

    def calculate_remaining_intake(self):
        bmr = self.calculate_bmr()
        total_calories = self.calculate_total_calories()
        return max(bmr - total_calories, 0)  # 음수가 되지 않도록 처리

    def get_user_name(self):
        return self.user_credentials.get(self.user_id, {}).get('details', {}).get('name', 'Unknown User')

    def on_recommendation_button_clicked(self):
        remaining_intake = self.calculate_remaining_intake()
        user_name = self.get_user_name()

        # 남은 섭취량 데이터를 JSON 파일로 저장
        remaining_intake_data = {
            'user_name': user_name,
            'remaining_intake': remaining_intake
        }
        file_name = f"{user_name}_remaining_intake.json"
        with open(file_name, 'w') as file:
            json.dump(remaining_intake_data, file, indent=4)

        # 콘솔에 남은 섭취량 출력
        print(f"{user_name}님의 현재 남은 섭취량: {remaining_intake}칼로리")

        # 사용자에게 파일 저장 알림
        QMessageBox.information(self, '음식 추천', f'{user_name}님의 남은 섭취량이 {file_name}에 저장되었습니다.')

    def calculate_recommended_intake(self):
        bmr = self.calculate_bmr()
        # 탄수화물 50%, 단백질 30%, 지방 20%로 분배
        carbs_cal = bmr * 0.5
        protein_cal = bmr * 0.3
        fats_cal = bmr * 0.2

        # 칼로리를 그램으로 변환 (탄수화물과 단백질 1g당 4칼로리, 지방 1g당 9칼로리)
        carbs_grams = carbs_cal / 4
        protein_grams = protein_cal / 4
        fats_grams = fats_cal / 9

        return {'carbs': round(carbs_grams, 2), 'protein': round(protein_grams, 2), 'fats': round(fats_grams, 2)}

    def calculate_nutrient_intake(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        user_diet = self.user_credentials.get(self.user_id, {}).get('diet', {})

        nutrient_totals = {'carbs': 0, 'protein': 0, 'fats': 0}
        for meal, foods in user_diet.get(current_date, {}).items():
            for food in foods:
                if isinstance(food, dict):
                    nutrition = food.get('nutrition', {})
                    nutrient_totals['carbs'] += self.safe_convert_to_float(nutrition.get('탄수화물', 0))
                    nutrient_totals['protein'] += self.safe_convert_to_float(nutrition.get('단백질', 0))
                    nutrient_totals['fats'] += self.safe_convert_to_float(nutrition.get('지방', 0))

        return nutrient_totals

    def safe_convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return 0.0

    def calculate_remaining_nutrient_intake(self):
        recommended_intake = self.calculate_recommended_intake()
        current_intake = self.calculate_nutrient_intake()

        remaining_intake = {
            'carbs': max(recommended_intake['carbs'] - current_intake['carbs'], 0),
            'protein': max(recommended_intake['protein'] - current_intake['protein'], 0),
            'fats': max(recommended_intake['fats'] - current_intake['fats'], 0)
        }
        return remaining_intake