from PyQt5.QtWidgets import *

class UIManager:
    def __init__(self, app):
        self.app = app

    def create_login_widgets(self):
        # ID 입력 위젯
        self.app.id_label = QLabel('ID:', self.app)
        self.app.id_input = QLineEdit(self.app)

        # PW 입력 위젯
        self.app.pw_label = QLabel('PW:', self.app)
        self.app.pw_input = QLineEdit(self.app)
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
        # 회원가입 버튼
        self.app.signup_button = QPushButton('회원가입하기', self.app)
        self.app.signup_button.clicked.connect(self.app.Login.signup_clicked)

        # 로그인 버튼
        self.app.signin_button = QPushButton('로그인하기', self.app)
        self.app.signin_button.clicked.connect(self.app.Login.signin_clicked)

        # 버튼 레이아웃
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.app.signup_button)
        self.button_layout.addWidget(self.app.signin_button)

    def center(self):
        qr = self.app.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.app.move(qr.topLeft())
