from PyQt5.QtWidgets import *


class UIManager:
    # Constructor for UIManager class
    def __init__(self, app):
        self.app = app  # Reference to the main application

    # Method to create login widgets
    def create_login_widgets(self):
        # Widget for ID input
        self.app.id_label = QLabel("ID:", self.app)
        self.app.id_input = QLineEdit(self.app)

        # Widget for password input
        self.app.pw_label = QLabel("PW:", self.app)
        self.app.pw_input = QLineEdit(self.app)
        self.app.pw_input.setEchoMode(QLineEdit.Password)

        # Layout for ID input
        id_layout = QHBoxLayout()
        id_layout.addWidget(self.app.id_label)
        id_layout.addWidget(self.app.id_input)

        # Layout for password input
        pw_layout = QHBoxLayout()
        pw_layout.addWidget(self.app.pw_label)
        pw_layout.addWidget(self.app.pw_input)

        # Create buttons for the UI
        self.create_buttons()

        # Main layout including the buttons
        main_layout = QVBoxLayout()
        main_layout.addLayout(id_layout)
        main_layout.addLayout(pw_layout)
        main_layout.addLayout(self.button_layout)

        # Set the main layout as the app's layout
        self.app.setLayout(main_layout)

    # Method to create buttons
    def create_buttons(self):
        # Signup button
        self.app.signup_button = QPushButton("회원가입하기", self.app)
        self.app.signup_button.clicked.connect(self.app.Login.signup_clicked)

        # Signin button
        self.app.signin_button = QPushButton("로그인하기", self.app)
        self.app.signin_button.clicked.connect(self.app.Login.signin_clicked)

        # Layout for buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.app.signup_button)
        self.button_layout.addWidget(self.app.signin_button)

     # Method to center the application window
    def center(self):
        qr = self.app.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.app.move(qr.topLeft())
