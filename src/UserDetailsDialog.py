from PyQt5.QtWidgets import *

class UserDetailsDialog(QDialog):
    def __init__(self):
        # Initialize the user details dialog
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the user interface for the dialog
        self.setWindowTitle('사용자 상세 정보')
        self.setGeometry(100, 100, 300, 200)
        self.center()  # Center the window on the screen

        layout = QVBoxLayout()

        # Set up name input field
        self.name_label = QLabel('이름:', self)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Set up gender selection field
        self.gender_label = QLabel('성별:', self)
        self.gender_input = QComboBox(self)
        self.gender_input.addItems(['남성', '여성', '기타'])
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_input)

        # Set up age input field
        self.age_label = QLabel('나이:', self)
        self.age_input = QLineEdit(self)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        # Set up weight input field
        self.weight_label = QLabel('체중(kg):', self)
        self.weight_input = QLineEdit(self)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        # Set up height input field
        self.height_label = QLabel('키(cm):', self)
        self.height_input = QLineEdit(self)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # Set up allergy information input field
        self.allergy_label = QLabel('알레르기 정보:', self)
        self.allergy_input = QLineEdit(self)
        layout.addWidget(self.allergy_label)
        layout.addWidget(self.allergy_input)

        # Set up submit button
        self.submit_button = QPushButton('제출하기', self)
        self.submit_button.clicked.connect(self.submit_info)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_info(self):
        # Validate inputs and save user information
        errors = []  # List to store error messages

        # Validate age as a positive integer
        if not self.age_input.text().isdigit() or int(self.age_input.text()) <= 0:
            errors.append("나이는 자연수로 입력해야 합니다.")

        # Validate weight and height as positive numbers
        for label, edit in [("체중(kg)", self.weight_input), ("키(cm)", self.height_input)]:
            try:
                value = float(edit.text())
                if value <= 0:
                    errors.append(f"{label}는 양수로 입력해야 합니다.")
            except ValueError:
                errors.append(f"{label}는 숫자로 입력해야 합니다.")

        if errors:
            # Display all error messages if there are any
            QMessageBox.warning(self, "입력 오류", "\n".join(errors))
            return

        # Save user information if all inputs are valid
        self.user_info = {
            'name': self.name_input.text(),
            'gender': self.gender_input.currentText(),
            'age': int(self.age_input.text()),
            'weight': float(self.weight_input.text()),
            'height': float(self.height_input.text()),
            'allergies': self.allergy_input.text()
        }
        QMessageBox.information(self, '회원가입', '회원가입이 완료되었습니다.')
        self.accept()

    def get_user_info(self):
        # Return the saved user information
        return self.user_info

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
