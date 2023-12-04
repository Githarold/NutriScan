import sys
from PyQt5.QtWidgets import *
from UIManager import UIManager
from Login import Login
from Database import Database

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.user_credentials = {}
        self.UIManager = UIManager(self)
        self.Login = Login(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('식단관리프로그램')
        self.resize(400, 300)
        self.UIManager.center()
        self.UIManager.create_login_widgets()
        self.UIManager.create_buttons()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
