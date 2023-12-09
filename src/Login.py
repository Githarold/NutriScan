from PyQt5.QtWidgets import *
from UserDetailsDialog import UserDetailsDialog
from HomeDialog import Home
from Database import Database


class Login:
    # Constructor for the Login class
    def __init__(self, app):
        self.app = app
        self.db = Database()

    def signup_clicked(self):
        # Function called when the signup button is clicked
        user_id = self.app.id_input.text()
        user_pw = self.app.pw_input.text()

        # Check if the user ID already exists using the check_user_exists method
        existing_user = self.app.db.check_user_exists(user_id)

        if existing_user:
            QMessageBox.warning(self.app, "회원가입 오류", "이미 존재하는 ID입니다.")
        elif user_id and user_pw:
            # Add new user to the database using the add_new_user method
            if self.app.db.add_new_user(user_id, user_pw):
                QMessageBox.information(self.app, "회원가입", "사용자 정보를 입력해주세요.")
                self.open_user_details_dialog(user_id)
            else:
                QMessageBox.warning(self.app, "회원가입 오류", "데이터베이스 오류로 인해 회원가입에 실패했습니다.")
        else:
            QMessageBox.warning(self.app, "회원가입 오류", "ID와 비밀번호를 모두 입력해주세요.")

    def signin_clicked(self):
        # Function called when the signin button is clicked
        user_id = self.app.id_input.text()
        user_pw = self.app.pw_input.text()

        # Check the existence and password match of the user in the database
        user_record = self.db.check_user_exists(user_id)

        if user_record and user_record["password"] == user_pw:
            # On successful login, fetch user details
            user_data = self.db.fetch_user_data(user_id)
            # Uncomment the below line to see user data (user data + diet data)
            if user_data:
                # Save the fetched user data in user_credentials
                self.app.user_credentials = user_data
                QMessageBox.information(self.app, "로그인 성공", "로그인이 성공적으로 이루어졌습니다.")
                self.app.hide()  # Hide the main dialog
                self.open_home_dialog(user_id)
            else:
                QMessageBox.warning(self.app, "로그인 오류", "사용자 정보를 가져오는데 실패했습니다.")
        else:
            QMessageBox.warning(self.app, "로그인 오류", "ID 또는 비밀번호가 잘못되었습니다.")

    def open_home_dialog(self, user_id):
        # Function to open the Home dialog
        dialog = Home(user_id, self.app.user_credentials)
        dialog.exec_()

    def open_user_details_dialog(self, user_id):
        # Function to open the User Details dialog
        dialog = UserDetailsDialog()
        if dialog.exec_():
            user_details = dialog.get_user_info()
            # Save the details to the database using the update_user_details method of Database class
            if self.db.update_user_details(user_id, user_details):
                QMessageBox.information(
                    self.app, "회원 정보 등록 완료", "사용자 세부 정보가 업데이트되었습니다."
                )
            else:
                QMessageBox.critical(self.app, "회원 정보 등록 실패", "데이터베이스 오류가 발생했습니다.")
