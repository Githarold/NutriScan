from PyQt5.QtWidgets import *

class UpdateInfoDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('체중 및 키 정보 업데이트')  
        self.setGeometry(100, 100, 300, 200)  

        layout = QVBoxLayout()  

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
            weight = self.weight_input.text()
            height = self.height_input.text()

            # 체중과 키가 숫자로 변환 가능한지 확인
            try:
                weight = float(weight)
                height = float(height)
            except ValueError:
                QMessageBox.warning(self, '입력 오류', '체중과 키는 숫자로 입력해야 합니다.')
                return

            # 사용자 정보 업데이트
            old_weight = self.user_credentials[self.user_id]['details'].get('weight', '없음')
            old_height = self.user_credentials[self.user_id]['details'].get('height', '없음')

            self.user_credentials[self.user_id]['details']['weight'] = weight
            self.user_credentials[self.user_id]['details']['height'] = height

            update_message = f'체중 및 키 정보가 업데이트되었습니다.\n\n' \
                            f'이전 체중: {old_weight} kg\n' \
                            f'새 체중: {weight} kg\n\n' \
                            f'이전 키: {old_height} cm\n' \
                            f'새 키: {height} cm'
            QMessageBox.information(self, '업데이트 성공', update_message)
            self.accept()