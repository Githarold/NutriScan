from PyQt5.QtWidgets import *
from datetime import datetime
from RecommendFood import Recommender


class FoodRecommendationDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("음식 추천")
        self.setGeometry(200, 200, 300, 200)
        self.center()  # Function call to center the window on the screen
        layout = QVBoxLayout()

        # Text label for recommendation
        self.recommendation_label = QLabel("오늘의 추천 음식", self)
        layout.addWidget(self.recommendation_label)

        # Label for user's total calorie intake
        user_name = (
            self.user_credentials.get(self.user_id, {})
            .get("details", {})
            .get("name", "Unknown User")
        )
        total_calories = round(self.calculate_total_calories())
        self.intake_label = QLabel(
            f"오늘 {user_name}님의 섭취량은 {total_calories} 칼로리입니다.", self
        )
        layout.addWidget(self.intake_label)

        # Label for remaining calorie intake
        remaining_intake = round(self.calculate_remaining_intake())
        self.remaining_intake_label = QLabel(
            f"{self.get_user_name()}님의 현재 남은 섭취량은 {remaining_intake}칼로리입니다.", self
        )
        layout.addWidget(self.remaining_intake_label)

        # Label for remaining nutrient intake
        remaining_nutrients = self.calculate_remaining_nutrient_intake()
        self.remaining_nutrition_intake_label = QLabel(
            f"남은 탄수화물: {round(remaining_nutrients['carbs'])}g, "
            f"단백질: {round(remaining_nutrients['protein'])}g, "
            f"지방: {round(remaining_nutrients['fats'])}g",
            self,
        )
        layout.addWidget(self.remaining_nutrition_intake_label)

        # Button for getting food recommendations
        self.get_recommendation_button = QPushButton("음식 추천 받기", self)
        self.get_recommendation_button.clicked.connect(
            self.on_recommendation_button_clicked
        )
        layout.addWidget(self.get_recommendation_button)

        self.setLayout(layout)

    def calculate_total_calories(self):
        # Calculate total calories consumed by the user on the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        user_diet = self.user_credentials.get(self.user_id, {}).get("diet", {})

        total_calories = 0
        for meal, foods in user_diet.get(current_date, {}).items():
            for food in foods:
                if isinstance(food, dict):
                    calories = food.get("nutrition", {}).get("칼로리", 0)
                    try:
                        total_calories += int(calories)
                    except ValueError:
                        pass  # Ignore invalid calorie values

        return total_calories

    def calculate_bmr(self):
        # Calculate the Basal Metabolic Rate (BMR) based on user's details
        user_details = self.user_credentials.get(self.user_id, {}).get("details", {})
        gender = user_details.get("gender", "N/A")
        try:
            age = float(user_details.get("age", 0))
            weight = float(user_details.get("weight", 0))
            height = float(user_details.get("height", 0))
        except ValueError:
            age = (
                weight
            ) = height = 0  # Use default values in case of conversion failure

        if gender == "남성":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == "여성":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            # Average BMR calculation for unspecified gender
            bmr = (
                (88.362 + 447.593) / 2
                + ((13.397 + 9.247) / 2 * weight)
                + ((4.799 + 3.098) / 2 * height)
                - ((5.677 + 4.330) / 2 * age)
            )
        return round(bmr, 2)

    def calculate_remaining_intake(self):
        # Calculate the remaining calorie intake for the user
        bmr = self.calculate_bmr()
        total_calories = self.calculate_total_calories()
        return max(bmr - total_calories, 0)  # Ensure the result is not negative

    def get_user_name(self):
        # Retrieve the user's name from credentials
        return (
            self.user_credentials.get(self.user_id, {})
            .get("details", {})
            .get("name", "Unknown User")
        )

    def on_recommendation_button_clicked(self):
        # Handle the event when the recommendation button is clicked
        remaining_nutrients = self.calculate_remaining_nutrient_intake()
        user_name = self.get_user_name()

        # Create an instance of Recommender class and get recommendations
        info_getter = Recommender(self.user_credentials, self.user_id)
        recommended_food = info_getter.get_info_gpt(remaining_nutrients)

        # Display the recommended food in a dialog
        QMessageBox.information(
            self, "음식 추천", f"{user_name}님을 위한 추천 음식: {recommended_food}"
        )

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

        return {
            "carbs": round(carbs_grams, 2),
            "protein": round(protein_grams, 2),
            "fats": round(fats_grams, 2),
        }

    def calculate_nutrient_intake(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        user_diet = self.user_credentials.get(self.user_id, {}).get("diet", {})

        nutrient_totals = {"carbs": 0, "protein": 0, "fats": 0}
        for meal, foods in user_diet.get(current_date, {}).items():
            for food in foods:
                if isinstance(food, dict):
                    nutrition = food.get("nutrition", {})
                    nutrient_totals["carbs"] += self.safe_convert_to_float(
                        nutrition.get("탄수화물", 0)
                    )
                    nutrient_totals["protein"] += self.safe_convert_to_float(
                        nutrition.get("단백질", 0)
                    )
                    nutrient_totals["fats"] += self.safe_convert_to_float(
                        nutrition.get("지방", 0)
                    )

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
            "carbs": max(recommended_intake["carbs"] - current_intake["carbs"], 0),
            "protein": max(
                recommended_intake["protein"] - current_intake["protein"], 0
            ),
            "fats": max(recommended_intake["fats"] - current_intake["fats"], 0),
        }
        return remaining_intake

    # Additional methods for calculating recommended nutrient intake, current nutrient intake, safe conversion to float, and remaining nutrient intake follow the same pattern as described above.

    def center(self):
        # Center the dialog on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
