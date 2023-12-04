from PyQt5.QtWidgets import *


class ManualNutritionInputDialog(QDialog):
    def __init__(self, food_name):
        super().__init__()
        self.food_name = food_name
        self.initUI()

    def initUI(self):
        self.setWindowTitle('영양 정보 입력')  
        self.setGeometry(100, 100, 300, 200)  
        self.center()  # 화면 중앙에 위치시키는 함수 호출
        layout = QVBoxLayout()  

        message_label = QLabel(f'"{self.food_name}"을(를) 찾지 못했습니다.\n"{self.food_name}"의 영양소 정보를 입력해주세요.')
        layout.addWidget(message_label)

        self.calories_input = QLineEdit(self)
        layout.addWidget(QLabel('칼로리(kcal):'))
        layout.addWidget(self.calories_input)

        self.carbs_input = QLineEdit(self)
        layout.addWidget(QLabel('탄수화물(g):'))
        layout.addWidget(self.carbs_input)

        self.fat_input = QLineEdit(self)
        layout.addWidget(QLabel('지방(g):'))
        layout.addWidget(self.fat_input)

        self.protein_input = QLineEdit(self)
        layout.addWidget(QLabel('단백질(g):'))
        layout.addWidget(self.protein_input)

        # 당류 입력 필드 추가
        self.sugar_input = QLineEdit(self)
        layout.addWidget(QLabel('당류(g):'))
        layout.addWidget(self.sugar_input)

        # 나트륨 입력 필드 추가
        self.sodium_input = QLineEdit(self)
        layout.addWidget(QLabel('나트륨(g):'))
        layout.addWidget(self.sodium_input)

        submit_button = QPushButton('제출', self)
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def is_number(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def accept(self):
        # 입력된 모든 값이 숫자인지 확인
        if not all(self.is_number(value.text()) for value in [self.calories_input, self.carbs_input, self.fat_input, self.protein_input, self.sugar_input, self.sodium_input]):
            QMessageBox.warning(self, '입력 오류', '영양소 정보는 숫자로 입력해야 합니다.')
            return
        super().accept()

    def get_nutrition_info(self):
        return {
            'calories': self.calories_input.text(),
            'carbs': self.carbs_input.text(),
            'fat': self.fat_input.text(),
            'protein': self.protein_input.text(),
            'sugar': self.sugar_input.text(),  # 당류
            'sodium': self.sodium_input.text()  # 나트륨
        }
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())