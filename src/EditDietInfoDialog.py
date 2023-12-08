from PyQt5.QtWidgets import *
from FoodDetailEditDialog import FoodDetailEditDialog


class EditDietInfoDialog(QDialog):
    def __init__(self, diet_data):
        super().__init__()
        self.diet_data = diet_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('식단 정보 수정')
        self.setGeometry(150, 150, 350, 350)
        self.center()  # 화면 중앙에 위치시키는 함수 호출
        layout = QVBoxLayout()

        self.date_combo = QComboBox(self)
        self.date_combo.addItems(sorted(self.diet_data.keys(), reverse=True))
        self.date_combo.currentIndexChanged.connect(self.update_food_list)
        layout.addWidget(self.date_combo)

        # 음식 선택을 위한 QComboBox
        self.food_combo = QComboBox(self)
        layout.addWidget(self.food_combo)

        self.edit_food_button = QPushButton('음식 편집', self)
        self.edit_food_button.clicked.connect(self.edit_food)
        layout.addWidget(self.edit_food_button)

        self.delete_food_button = QPushButton('음식 삭제', self)
        self.delete_food_button.clicked.connect(self.delete_food)
        layout.addWidget(self.delete_food_button)

        self.save_button = QPushButton('변경 사항 저장', self)
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
        self.update_food_list()

    def update_food_list(self):
        self.food_combo.clear()
        selected_date = self.date_combo.currentText()
        daily_diet = self.diet_data.get(selected_date, {})
        for meal_time, meal_list in daily_diet.items():
            for meal in meal_list:
                if isinstance(meal, dict) and 'name' in meal:
                    self.food_combo.addItem(meal['name'])

    def delete_food(self):
        selected_food_name = self.food_combo.currentText()
        if selected_food_name:
            reply = QMessageBox.question(self, '음식 삭제 확인', f"'{selected_food_name}' 음식을 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                selected_date = self.date_combo.currentText()
                for meal_time in self.diet_data[selected_date]:
                    self.diet_data[selected_date][meal_time] = [meal for meal in self.diet_data[selected_date][meal_time] if meal.get('name') != selected_food_name]
                self.update_food_list()
    
    def save_changes(self):
        reply = QMessageBox.question(self, '변경 사항 저장 확인', '변경 사항을 저장하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.accept()

    def get_diet_data(self):
        return self.diet_data

    def edit_food(self):
        selected_food_name = self.food_combo.currentText()
        if selected_food_name:
            selected_date = self.date_combo.currentText()
            for meal_time, meal_list in self.diet_data[selected_date].items():
                for meal in meal_list:
                    if meal.get('name') == selected_food_name:
                        self.edit_food_details(meal, selected_date, meal_time)

    def edit_food_details(self, food, selected_date, meal_time):
        dialog = FoodDetailEditDialog(food)
        if dialog.exec_():
            updated_food = dialog.get_updated_food()
            reply = QMessageBox.question(self, '음식 수정 확인', '수정 사항을 저장하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                for i, meal in enumerate(self.diet_data[selected_date][meal_time]):
                    if meal.get('name') == food['name']:
                        self.diet_data[selected_date][meal_time][i] = updated_food
                        break
                self.update_food_list()

    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
