from PyQt5.QtWidgets import *

class UserDetailsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('사용자 상세 정보')
        self.setGeometry(100, 100, 300, 200)
        self.center()  # 화면 중앙에 위치시키는 함수 호출
        layout = QVBoxLayout()

        self.name_label = QLabel('이름:', self)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.gender_label = QLabel('성별:', self)
        self.gender_input = QComboBox(self)
        self.gender_input.addItems(['남성', '여성', '기타'])
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_input)

        self.age_label = QLabel('나이:', self)
        self.age_input = QLineEdit(self)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        self.weight_label = QLabel('체중(kg):', self)
        self.weight_input = QLineEdit(self)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        self.height_label = QLabel('키(cm):', self)
        self.height_input = QLineEdit(self)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        self.allergy_label = QLabel('알레르기 정보:', self)
        self.allergy_input = QLineEdit(self)
        layout.addWidget(self.allergy_label)
        layout.addWidget(self.allergy_input)

        self.submit_button = QPushButton('제출하기', self)
        self.submit_button.clicked.connect(self.submit_info)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_info(self):
        # 숫자로 변환 가능한지 확인하는 함수
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        # 입력된 나이, 체중, 키가 숫자인지 확인
        if not (is_number(self.age_input.text()) and 
                is_number(self.weight_input.text()) and 
                is_number(self.height_input.text())):
            QMessageBox.warning(self, "입력 오류", "나이, 체중, 키는 숫자로 입력해야 합니다.")
            return

        # 나이가 정수이고 0 이상인지, 몸무게와 키가 0 이상인지 확인
        if not (self.age_input.text().isdigit() and int(self.age_input.text()) > 0 and
                float(self.weight_input.text()) > 0 and 
                float(self.height_input.text()) > 0):
            QMessageBox.warning(self, "입력 오류", "나이는 자연수, 체중과 키는 양수로 입력해야 합니다.")
            return

        # 모든 입력이 유효한 경우, 사용자 정보 저장
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
        return self.user_info

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())