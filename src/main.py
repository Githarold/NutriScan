import sys
from PyQt5.QtWidgets import *
from UIManager import UIManager
from Login import Login
from Database import Database


class MyApp(QWidget):
    # Constructor of the MyApp class
    def __init__(self):
        super().__init__()
        self.db = Database()  # Initialize the Database object
        self.user_credentials = {}  # Dictionary to store user credentials
        self.UIManager = UIManager(
            self
        )  # Initialize UIManager with the current instance
        self.Login = Login(self)  # Initialize Login with the current instance
        self.initUI()  # Initialize the UI elements

    # Method to initialize the user interface
    def initUI(self):
        self.setWindowTitle("식단관리프로그램")  # Set the window title
        self.resize(400, 300)  # Set the window size
        self.UIManager.center()  # Center the window on the screen
        self.UIManager.create_login_widgets()  # Create widgets for the login interface

        self.show()  # Show the window


# Check if the script is run directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
