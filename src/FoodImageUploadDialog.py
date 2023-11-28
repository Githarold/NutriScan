from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from datetime import datetime

class FoodImageUploadDialog(QDialog):
    def __init__(self, user_credentials, user_id):
        super().__init__()
        self.user_credentials = user_credentials
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('음식 사진 업로드')  
        self.setGeometry(100, 100, 300, 250)  # 창 크기 조정
        layout = QVBoxLayout()  

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('여기에 이미지 url을 붙여넣기 해주세요')
        layout.addWidget(self.url_input)

        self.url_button = QPushButton('이미지 url 변환사이트', self)
        self.url_button.clicked.connect(self.open_image_url_site)
        layout.addWidget(self.url_button)

        # 식사 시간 선택을 위한 드롭다운 메뉴
        self.meal_time_combo = QComboBox(self)
        self.meal_time_combo.addItems(['아침', '점심', '저녁'])
        layout.addWidget(self.meal_time_combo)

        self.submit_button = QPushButton('제출하기', self)
        self.submit_button.clicked.connect(self.submit_image)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def open_image_url_site(self):
        QDesktopServices.openUrl(QUrl("https://ko.imgbb.com"))

    def submit_image(self):
        image_url = self.url_input.text()
        meal_time = self.meal_time_combo.currentText()
        if not image_url:
            QMessageBox.warning(self, '입력 오류', '이미지 URL을 입력해주세요.')
            return

        # 현재 날짜를 얻어오기
        current_date = datetime.now().strftime("%Y-%m-%d")

        # 유저 식단 정보에 이미지 URL 추가
        user_diet = self.user_credentials[self.user_id].setdefault('diet', {})
        daily_diet = user_diet.setdefault(current_date, {'아침': [], '점심': [], '저녁': []})
        daily_diet[meal_time].append({'image_url': image_url})

        QMessageBox.information(self, '이미지 업로드', f'이미지 URL이 {meal_time} 식단에 추가되었습니다.')
        self.accept()
