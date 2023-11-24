from PyQt5.QtWidgets import QMessageBox
from UserDetailsDialog import UserDetailsDialog
from home import Home

class EventHandler:
    def __init__(self, app):
        self.app = app

    def signup_clicked(self):
        user_id = self.app.id_input.text()
        user_pw = self.app.pw_input.text()
        if user_id in self.app.user_credentials:
            QMessageBox.warning(self.app, '회원가입 오류', '이미 존재하는 ID입니다.')
        elif user_id and user_pw:
            self.app.user_credentials[user_id] = {'password': user_pw, 'details': {}}
            QMessageBox.information(self.app, '회원가입', '사용자 정보를 입력해주세요')
            self.open_user_details_dialog(user_id)
        else:
            QMessageBox.warning(self.app, '회원가입 오류', 'ID와 비밀번호를 모두 입력해주세요.')

    def signin_clicked(self):
        user_id = self.app.id_input.text()
        user_pw = self.app.pw_input.text()
        if self.app.user_credentials.get(user_id, {}).get('password') == user_pw:
            QMessageBox.information(self.app, '로그인 성공', '로그인이 성공적으로 이루어졌습니다.')
            self.app.hide()  # 메인 다이얼로그 숨기기
            self.open_home_dialog(user_id)
        else:
            QMessageBox.warning(self.app, '로그인 오류', 'ID 또는 비밀번호가 잘못되었습니다.')

    def open_home_dialog(self, user_id):
        dialog = Home(user_id, self.app.user_credentials)
        dialog.exec_()

    def open_user_details_dialog(self, user_id):
        dialog = UserDetailsDialog()
        if dialog.exec_():
            user_details = dialog.get_user_info()
            self.app.user_credentials[user_id]['details'] = user_details
