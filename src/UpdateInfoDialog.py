from PyQt5.QtWidgets import *

class UpdateInfoDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        # Initialize the dialog with user credentials and user ID
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        # Set the window title and size, and center the window on the screen
        self.setWindowTitle('체중, 키 및 나이 정보 업데이트')  
        self.setGeometry(100, 100, 300, 250)  
        self.center()  # Call function to center window

        layout = QVBoxLayout()

        # Age input field setup
        self.age_label = QLabel('나이:', self)
        self.age_input = QLineEdit(self)
        # Set existing age information
        current_age = self.user_credentials[self.user_id]['details'].get('age', '')
        self.age_input.setText(str(current_age))
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        # Weight input field setup
        self.weight_label = QLabel('체중 (kg):', self)
        self.weight_input = QLineEdit(self)
        # Set existing weight information
        current_weight = self.user_credentials[self.user_id]['details'].get('weight', '')
        self.weight_input.setText(str(current_weight))
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        # Height input field setup
        self.height_label = QLabel('키 (cm):', self)
        self.height_input = QLineEdit(self)
        # Set existing height information
        current_height = self.user_credentials[self.user_id]['details'].get('height', '')
        self.height_input.setText(str(current_height))
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # Update button setup
        self.update_button = QPushButton('업데이트', self)
        self.update_button.clicked.connect(self.update_info)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update_info(self):
        # Validate inputs and update user information
        errors = []  # List to store error messages

        # Validate age as a natural number
        age = self.age_input.text()
        if not age.isdigit() or int(age) <= 0:
            errors.append("나이는 자연수로 입력해야 합니다.")

        # Validate weight as a positive number
        weight = self.weight_input.text()
        try:
            if float(weight) <= 0:
                errors.append("체중은 양수로 입력해야 합니다.")
        except ValueError:
            errors.append("체중은 숫자로 입력해야 합니다.")

        # Validate height as a positive number
        height = self.height_input.text()
        try:
            if float(height) <= 0:
                errors.append("키는 양수로 입력해야 합니다.")
        except ValueError:
            errors.append("키는 숫자로 입력해야 합니다.")

        if errors:
            QMessageBox.warning(self, '입력 오류', "\n".join(errors))
            return

        # Update user information
        old_age = self.user_credentials[self.user_id]['details'].get('age', '없음')
        old_weight = self.user_credentials[self.user_id]['details'].get('weight', '없음')
        old_height = self.user_credentials[self.user_id]['details'].get('height', '없음')
        
        self.user_credentials[self.user_id]['details']['age'] = int(age)
        self.user_credentials[self.user_id]['details']['weight'] = float(weight)
        self.user_credentials[self.user_id]['details']['height'] = float(height)

        update_message = f'나이, 체중 및 키 정보가 업데이트되었습니다.\n\n' \
                         f'이전 나이: {old_age} 세\n' \
                         f'새 나이: {age} 세\n\n' \
                         f'이전 체중: {old_weight} kg\n' \
                         f'새 체중: {weight} kg\n\n' \
                         f'이전 키: {old_height} cm\n' \
                         f'새 키: {height} cm'
        QMessageBox.information(self, '업데이트 성공', update_message)
        self.accept()

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
