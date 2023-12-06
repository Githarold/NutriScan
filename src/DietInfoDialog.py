from PyQt5.QtWidgets import *
from EditDietInfoDialog import EditDietInfoDialog

class DietInfoDialog(QDialog):
    def __init__(self, diet_data, user_id):
        super().__init__()
        self.diet_data = diet_data
        self.user_id = user_id  # 사용자 ID를 저장
        self.initUI()


    def initUI(self):
        self.setWindowTitle('식단 정보 확인')
        self.setGeometry(100, 100, 300, 300)
        self.center()  # 화면 중앙에 위치시키는 함수 호출
        layout = QVBoxLayout()

        # 날짜 선택 콤보 박스
        self.date_combo = QComboBox(self)
        # 날짜를 내림차순으로 정렬
        sorted_dates = sorted(self.diet_data.keys(), reverse=True)
        self.date_combo.addItems(sorted_dates)
        self.date_combo.currentIndexChanged.connect(self.display_diet_info)
        layout.addWidget(self.date_combo)

        # 식단 정보 라벨
        self.diet_info_label = QLabel(self)
        layout.addWidget(self.diet_info_label)

        # 초기 식단 정보 표시
        self.display_diet_info(0)

        self.edit_button = QPushButton('식단 정보 수정', self)
        self.edit_button.clicked.connect(self.open_edit_dialog)
        layout.addWidget(self.edit_button)
        self.setLayout(layout)

        # 콤보 박스의 초기 선택을 가장 최근 날짜로 설정
        if sorted_dates:
            self.date_combo.setCurrentIndex(0)

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
                    # 단위 'kcal' 및 'g' 추가
                    diet_info += (f"  - {food_name} (칼로리: {nutrition.get('칼로리', 'N/A')} kcal, "
                                  f"탄수화물: {nutrition.get('탄수화물', 'N/A')} g, "
                                  f"지방: {nutrition.get('지방', 'N/A')} g, "
                                  f"단백질: {nutrition.get('단백질', 'N/A')} g, "
                                  f"당류: {nutrition.get('당류', 'N/A')} g, "
                                  f"나트륨: {nutrition.get('나트륨', 'N/A')} mg")
                    diet_info += "\n"
                else:
                    # 문자열 형태인 경우 (영양 정보 없음)
                    diet_info += f"  - {food}\n"
        self.diet_info_label.setText(diet_info)

    def open_edit_dialog(self):
        edit_dialog = EditDietInfoDialog(self.diet_data)
        if edit_dialog.exec_():
            self.diet_data = edit_dialog.get_diet_data()  # 변경 사항을 받아옴
            self.display_diet_info(self.date_combo.currentIndex())  # 식단 정보 업데이트

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())