from PyQt5.QtWidgets import *


class FoodDetailEditDialog(QDialog):
    def __init__(self, food):
        super().__init__()
        self.food = food
        self.initUI()

    def initUI(self):
        self.setWindowTitle("음식 세부 정보 편집")  # Title: 'Edit Food Details'
        self.setGeometry(100, 100, 300, 200)
        self.center()  # Function call to center the window on the screen
        layout = QFormLayout()

        # Line edit for food name
        self.name_edit = QLineEdit(self.food.get("name", ""))
        layout.addRow("음식 이름:", self.name_edit)  # 'Food Name:'

        # Dictionary to store nutrition value line edits
        self.nutrition_edits = {}
        for key in ["칼로리", "탄수화물", "지방", "단백질", "당류", "나트륨"]:  # Nutrition components
            edit = QLineEdit(str(self.food.get("nutrition", {}).get(key, "")))
            self.nutrition_edits[key] = edit
            layout.addRow(
                f"{key}:", edit
            )  # Adding line edit for each nutrition component

        # Save button
        self.save_button = QPushButton("저장", self)  # 'Save'
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_changes(self):
        self.food["name"] = self.name_edit.text()
        nutrition = self.food.get("nutrition", {})
        for key, edit in self.nutrition_edits.items():
            value = edit.text()
            try:
                # Attempt to convert input value to float
                nutrition_value = float(value)
                # Display warning message if input value is less than 0
                if nutrition_value < 0:
                    QMessageBox.warning(
                        self, "입력 오류", f"{key}는 0이상의 숫자여야 합니다."
                    )  # 'Input Error: [key] must be a non-negative number'
                    return
            except ValueError:
                # Display warning message if conversion fails
                QMessageBox.warning(
                    self, "입력 오류", f"{key}는 숫자로 입력해야 합니다."
                )  # 'Input Error: [key] must be a number'
                return

            # If conversion is successful, save the value in the nutrition dictionary
            nutrition[key] = nutrition_value

        self.food["nutrition"] = nutrition
        self.accept()

    def get_updated_food(self):
        # Method to return the edited food information
        return self.food  # self.food should contain the edited food information

    def center(self):
        # Method to center the dialog on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
