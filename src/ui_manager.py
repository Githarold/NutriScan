# 주요 기능: PyQt5를 사용하여 식단 관리 프로그램의 로그인 UI를 구성하는 UIManager 클래스
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class UIManager:
    def __init__(self, app):
        self.app = app # 메인 애플리케이션 인스턴스를 참조

    def create_login_widgets(self):
        # 폰트 및 스타일 설정
        font = QFont('Arial', 10) # 폰트 설정

        # ID 입력 위젯
        self.app.id_label = QLabel('ID:', self.app) # ID 라벨 생성
        self.app.id_label.setFont(font) # ID 라벨 폰트 설정
        self.app.id_input = QLineEdit(self.app) # ID 입력 필드 생성
        self.app.id_input.setFont(font) # ID 입력 필드 폰트 설정

        # PW 입력 위젯
        self.app.pw_label = QLabel('PW:', self.app) # 비밀번호 라벨 생성
        self.app.pw_label.setFont(font) # 비밀번호 라벨 폰트 설정
        self.app.pw_input = QLineEdit(self.app) # 비밀번호 입력 필드 생성
        self.app.pw_input.setFont(font) # 비밀번호 입력 필드 폰트 설정
        self.app.pw_input.setEchoMode(QLineEdit.Password) # 비밀번호 마스킹 설정

        # 레이아웃 설정
        id_layout = QHBoxLayout() # ID 입력 위젯을 위한 수평 레이아웃
        id_layout.addWidget(self.app.id_label) # ID 라벨 추가
        id_layout.addWidget(self.app.id_input) # ID 입력 필드 추가

        pw_layout = QHBoxLayout() # PW 입력 위젯을 위한 수평 레이아웃
        pw_layout.addWidget(self.app.pw_label) # PW 라벨 추가
        pw_layout.addWidget(self.app.pw_input) # PW 입력 필드 추가

        # 버튼 레이아웃
        self.create_buttons()

        # 버튼을 포함한 메인 레이아웃
        main_layout = QVBoxLayout() # 메인 수직 레이아웃
        main_layout.addLayout(id_layout) # ID 레이아웃 추가
        main_layout.addLayout(pw_layout) # PW 레이아웃 추가
        main_layout.addLayout(self.button_layout) # 버튼 레이아웃 추가

        # 메인 레이아웃을 앱의 레이아웃으로 설정
        self.app.setLayout(main_layout) # 메인 레이아웃을 앱에 설정

    def create_buttons(self):
        # 버튼 스타일 설정
        button_style = "QPushButton { font-size: 10pt; background-color: #4CAF50; color: white; }"

        # 회원가입 버튼
        self.app.signup_button = QPushButton('회원가입하기', self.app) # 회원가입 버튼 생성
        self.app.signup_button.setStyleSheet(button_style) # 스타일 적용
        self.app.signup_button.clicked.connect(self.app.event_handler.signup_clicked) # 클릭 이벤트 연결

        # 로그인 버튼
        self.app.signin_button = QPushButton('로그인하기', self.app) # 로그인 버튼 생성
        self.app.signin_button.setStyleSheet(button_style) # 스타일 적용
        self.app.signin_button.clicked.connect(self.app.event_handler.signin_clicked) # 클릭 이벤트 연결

        # 버튼 레이아웃
        self.button_layout = QHBoxLayout() # 버튼을 위한 수평 레이아웃
        self.button_layout.addWidget(self.app.signup_button) # 회원가입 버튼 추가
        self.button_layout.addWidget(self.app.signin_button) # 로그인 버튼 추가

    def center(self):
        qr = self.app.frameGeometry() # 현재 창의 위치와 크기를 가져옴
        cp = QDesktopWidget().availableGeometry().center() # 화면 중앙의 좌표를 계산
        qr.moveCenter(cp) # 창을 화면 중앙으로 이동
        self.app.move(qr.topLeft()) # 창을 화면 중앙에 위치시킴
