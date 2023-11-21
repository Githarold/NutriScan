from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox

class DietInfoDialog(QDialog):
    def __init__(self, diet_data):
        super().__init__()
        self.diet_data = diet_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('식단 정보 확인')
        self.setGeometry(100, 100, 300, 300)
        layout = QVBoxLayout()

        # 날짜 선택 콤보 박스
        self.date_combo = QComboBox(self)
        self.date_combo.addItems(sorted(self.diet_data.keys()))
        self.date_combo.currentIndexChanged.connect(self.display_diet_info)
        layout.addWidget(self.date_combo)

        # 식단 정보 라벨
        self.diet_info_label = QLabel(self)
        layout.addWidget(self.diet_info_label)

        # 초기 식단 정보 표시
        self.display_diet_info(0)
        self.setLayout(layout)

    def display_diet_info(self, index):
        date = self.date_combo.itemText(index)
        daily_diet = self.diet_data.get(date, {})
        diet_info = f"날짜: {date}\n"
        for meal, foods in daily_diet.items():
            diet_info += f"{meal}:\n"
            for food in foods:
                if isinstance(food, dict):
                    # 사전 형태인 경우 (영양 정보 포함)
                    food_name = food.get('name', 'N/A')
                    nutrition = food.get('nutrition', {})
                    diet_info += (f"  - {food_name} (칼로리: {nutrition.get('칼로리', 'N/A')}, "
                                  f"탄수화물: {nutrition.get('탄수화물', 'N/A')}, "
                                  f"지방: {nutrition.get('지방', 'N/A')}, "
                                  f"단백질: {nutrition.get('단백질', 'N/A')})\n")
                else:
                    # 문자열 형태인 경우 (영양 정보 없음)
                    diet_info += f"  - {food}\n"
            self.diet_info_label.setText(diet_info)
