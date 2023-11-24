import sys
from PyQt5.QtWidgets import *
from ui_manager import UIManager
from event_handler import EventHandler

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user_credentials = {}
        self.ui_manager = UIManager(self)
        self.event_handler = EventHandler(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('식단관리프로그램')
        self.resize(400, 300)
        self.ui_manager.center()
        self.ui_manager.create_login_widgets()
        self.ui_manager.create_buttons()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
