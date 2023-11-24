from PyQt5.QtWidgets import *

class FoodDetailEditDialog (QDialog):
    def __init__(self, food):
        super().__init__()
        self.food = food
        self.initUI()

    def initUI(self):
        self.setWindowTitle('음식 세부 정보 편집')
        self.setGeometry(100, 100, 300, 200)
        layout = QFormLayout()

        self.name_edit = QLineEdit(self.food.get('name', ''))
        layout.addRow('음식 이름:', self.name_edit)

        self.nutrition_edits = {}
        for key in ['칼로리', '탄수화물', '지방', '단백질', '당류', '나트륨']:
            edit = QLineEdit(str(self.food.get('nutrition', {}).get(key, '')))
            self.nutrition_edits[key] = edit
            layout.addRow(f'{key}:', edit)

        self.save_button = QPushButton('저장', self)
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_changes(self):
        self.food['name'] = self.name_edit.text()
        nutrition = self.food.get('nutrition', {})
        for key, edit in self.nutrition_edits.items():
            value = edit.text()
            if not value.isdigit():
                QMessageBox.warning(self, '입력 오류', f'{key}는 숫자로 입력해야 합니다.')
                return
            nutrition[key] = int(value)
        self.food['nutrition'] = nutrition
        self.accept()

    def get_updated_food(self):
        # 편집된 음식 정보를 반환하는 메서드
        return self.food  # 여기서 self.food는 편집된 음식 정보를 담고 있어야 합니다.