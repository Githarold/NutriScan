from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class UIManager:
    def __init__(self, app):
        self.app = app

    def create_login_widgets(self):
        # 폰트 및 스타일 설정
        font = QFont('Arial', 10)

        # ID 입력 위젯
        self.app.id_label = QLabel('ID:', self.app)
        self.app.id_label.setFont(font)
        self.app.id_input = QLineEdit(self.app)
        self.app.id_input.setFont(font)

        # PW 입력 위젯
        self.app.pw_label = QLabel('PW:', self.app)
        self.app.pw_label.setFont(font)
        self.app.pw_input = QLineEdit(self.app)
        self.app.pw_input.setFont(font)
        self.app.pw_input.setEchoMode(QLineEdit.Password)

        # 레이아웃 설정
        id_layout = QHBoxLayout()
        id_layout.addWidget(self.app.id_label)
        id_layout.addWidget(self.app.id_input)

        pw_layout = QHBoxLayout()
        pw_layout.addWidget(self.app.pw_label)
        pw_layout.addWidget(self.app.pw_input)

        # 버튼 레이아웃
        self.create_buttons()

        # 버튼을 포함한 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addLayout(id_layout)
        main_layout.addLayout(pw_layout)
        main_layout.addLayout(self.button_layout)

        # 메인 레이아웃을 앱의 레이아웃으로 설정
        self.app.setLayout(main_layout)

    def create_buttons(self):
        # 버튼 스타일 설정
        button_style = "QPushButton { font-size: 10pt; background-color: #4CAF50; color: white; }"

        # 회원가입 버튼
        self.app.signup_button = QPushButton('회원가입하기', self.app)
        self.app.signup_button.setStyleSheet(button_style)
        self.app.signup_button.clicked.connect(self.app.event_handler.signup_clicked)

        # 로그인 버튼
        self.app.signin_button = QPushButton('로그인하기', self.app)
        self.app.signin_button.setStyleSheet(button_style)
        self.app.signin_button.clicked.connect(self.app.event_handler.signin_clicked)

        # 버튼 레이아웃
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.app.signup_button)
        self.button_layout.addWidget(self.app.signin_button)

    def center(self):
        qr = self.app.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.app.move(qr.topLeft())
