from PyQt5.QtWidgets import *

class FoodDetailEditDialog (QDialog):
    def __init__(self, food):
        super().__init__()
        self.food = food
        self.initUI()

    def initUI(self):
        self.setWindowTitle('음식 세부 정보 편집')
        self.setGeometry(100, 100, 300, 200)
        self.center()  # 화면 중앙에 위치시키는 함수 호출
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
            try:
                # 입력값을 float로 변환을 시도합니다.
                nutrition_value = float(value)
                # 입력된 값이 0 이하인 경우 경고 메시지를 표시합니다.
                if nutrition_value < 0:
                    QMessageBox.warning(self, '입력 오류', f'{key}는 0이상의 숫자여야 합니다.')
                    return
            except ValueError:
                # 변환에 실패할 경우 경고 메시지를 표시합니다.
                QMessageBox.warning(self, '입력 오류', f'{key}는 숫자로 입력해야 합니다.')
                return

            # 변환에 성공한 경우, nutrition 사전에 값을 저장합니다.
            nutrition[key] = nutrition_value

        self.food['nutrition'] = nutrition
        self.accept()

    def get_updated_food(self):
        # 편집된 음식 정보를 반환하는 메서드
        return self.food  # 여기서 self.food는 편집된 음식 정보를 담고 있어야 합니다.

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())