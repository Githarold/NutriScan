from PyQt5.QtWidgets import *

class UpdateInfoDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('체중, 키 및 나이 정보 업데이트')  
        self.setGeometry(100, 100, 300, 250)  # 창 크기를 조정합니다.
        self.center()  # 화면 중앙에 위치시키는 함수 호출
        layout = QVBoxLayout()  

        # 나이 입력 필드
        self.age_label = QLabel('나이:', self)
        self.age_input = QLineEdit(self)
        # 기존 나이 정보 설정
        current_age = self.user_credentials[self.user_id]['details'].get('age', '')
        self.age_input.setText(str(current_age))
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        # 체중 입력 필드
        self.weight_label = QLabel('체중(kg):', self)
        self.weight_input = QLineEdit(self)
        # 기존 체중 정보 설정
        current_weight = self.user_credentials[self.user_id]['details'].get('weight', '')
        self.weight_input.setText(str(current_weight))
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        # 키 입력 필드
        self.height_label = QLabel('키(cm):', self)
        self.height_input = QLineEdit(self)
        # 기존 키 정보 설정
        current_height = self.user_credentials[self.user_id]['details'].get('height', '')
        self.height_input.setText(str(current_height))
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # 업데이트 버튼
        self.update_button = QPushButton('업데이트', self)
        self.update_button.clicked.connect(self.update_info)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update_info(self):
        errors = []  # 오류 메시지를 저장할 리스트

        # 나이가 자연수인지 확인
        age = self.age_input.text()
        if not age.isdigit() or int(age) <= 0:
            errors.append("나이는 자연수로 입력해야 합니다.")

        # 체중과 키가 양수인지 확인
        try:
            weight = float(self.weight_input.text())
            if weight <= 0:
                errors.append("체중은 양수로 입력해야 합니다.")
        except ValueError:
            errors.append("체중은 숫자로 입력해야 합니다.")

        try:
            height = float(self.height_input.text())
            if height <= 0:
                errors.append("키는 양수로 입력해야 합니다.")
        except ValueError:
            errors.append("키는 숫자로 입력해야 합니다.")

        if errors:
            QMessageBox.warning(self, '입력 오류', "\n".join(errors))
            return

        # 사용자 정보 업데이트
        old_age = self.user_credentials[self.user_id]['details'].get('age', '없음')
        old_weight = self.user_credentials[self.user_id]['details'].get('weight', '없음')
        old_height = self.user_credentials[self.user_id]['details'].get('height', '없음')

        self.user_credentials[self.user_id]['details']['age'] = int(age)
        self.user_credentials[self.user_id]['details']['weight'] = weight
        self.user_credentials[self.user_id]['details']['height'] = height

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
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
