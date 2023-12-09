from PyQt5.QtWidgets import *


class ManualNutritionInputDialog(QDialog):
    def __init__(self, food_name):
        # Initialize the dialog with a specific food name
        super().__init__()
        self.food_name = food_name
        self.initUI()

    def initUI(self):
        # Set the window title and size, and center the window on the screen
        self.setWindowTitle('영양 정보 입력')  
        self.setGeometry(100, 100, 300, 200)  
        self.center()  # 화면 중앙에 위치시키는 함수 호출

        layout = QVBoxLayout()

        # Display a message prompting the user to input nutrition information for the food
        message_label = QLabel(f'"{self.food_name}"을(를) 찾지 못했습니다.\n"{self.food_name}"의 영양소 정보를 입력해주세요.')
        layout.addWidget(message_label)

        # Create and add input fields for various nutrients
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

        # Add input fields for sugar and sodium
        self.sugar_input = QLineEdit(self)
        layout.addWidget(QLabel('당류(g):'))
        layout.addWidget(self.sugar_input)

        self.sodium_input = QLineEdit(self)
        layout.addWidget(QLabel('나트륨(mg):'))
        layout.addWidget(self.sodium_input)

        submit_button = QPushButton('제출', self)
        submit_button.clicked.connect(self.accept)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def accept(self):
        # Validate the inputs and close the dialog if inputs are valid
        errors = []  # List to store error messages

        # Mapping of nutrient fields to their respective input widgets
        nutrition_fields = {
            '칼로리(kcal)': self.calories_input,
            '탄수화물(g)': self.carbs_input,
            '지방(g)': self.fat_input,
            '단백질(g)': self.protein_input,
            '당류(g)': self.sugar_input,
            '나트륨(mg)': self.sodium_input
        }

        for key, edit in nutrition_fields.items():
            value = edit.text()
            try:
                # Attempt to convert the input value to a float
                nutrition_value = float(value)
                # Check if the input value is non-negative
                if nutrition_value < 0:
                    errors.append(f'{key}는 0 이상이어야 합니다.')
            except ValueError:
                # Add an error message if the input is not a number
                errors.append(f'{key}는 숫자로 입력해야 합니다.')

        if errors:
            # Display all error messages if there are any
            QMessageBox.warning(self, '입력 오류', "\n".join(errors))
            return
        else:
            super().accept()

    def get_nutrition_info(self):
        # Return the entered nutrition information as a dictionary
        return {
            'calories': self.calories_input.text(),
            'carbs': self.carbs_input.text(),
            'fat': self.fat_input.text(),
            'protein': self.protein_input.text(),
            'sugar': self.sugar_input.text(),  # 당류
            'sodium': self.sodium_input.text()  # 나트륨
        }

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
