from PyQt5.QtWidgets import QMessageBox
from UserDetailsDialog import UserDetailsDialog
from home import Home
from Database import Database

class EventHandler:
    def __init__(self, app):
        self.app = app
        self.db = Database()

    def signup_clicked(self):
        user_id = self.app.id_input.text()
        user_pw = self.app.pw_input.text()

        # check_user_exists 메소드로 사용자 ID의 존재 여부를 확인
        existing_user = self.app.db.check_user_exists(user_id)

        if existing_user:
            QMessageBox.warning(self.app, '회원가입 오류', '이미 존재하는 ID입니다.')
        elif user_id and user_pw:
            # add_new_user 메소드로 새 사용자를 데이터베이스에 추가
            if self.app.db.add_new_user(user_id, user_pw):
                QMessageBox.information(self.app, '회원가입', '사용자 정보를 입력해주세요.')
                self.open_user_details_dialog(user_id)
            else:
                QMessageBox.warning(self.app, '회원가입 오류', '데이터베이스 오류로 인해 회원가입에 실패했습니다.')
        else:
            QMessageBox.warning(self.app, '회원가입 오류', 'ID와 비밀번호를 모두 입력해주세요.')

    def signin_clicked(self):
        user_id = self.app.id_input.text()
        user_pw = self.app.pw_input.text()
        
        # 데이터베이스에서 사용자의 존재 여부와 비밀번호 일치 여부를 확인
        user_record = self.db.check_user_exists(user_id)
        
        if user_record and user_record['password'] == user_pw:
            # 로그인 성공 시 사용자의 상세 정보를 불러옵니다.
            user_data = self.db.fetch_user_data(user_id)
            # 사용자 상세 정보(user data + diet data) 보려면 바로 밑에 print 보기 
            # print(user_data)
            if user_data:
                # 가져온 사용자 정보를 user_credentials에 저장합니다.
                self.app.user_credentials = user_data
                QMessageBox.information(self.app, '로그인 성공', '로그인이 성공적으로 이루어졌습니다.')
                self.app.hide()  # 메인 다이얼로그 숨기기
                self.open_home_dialog(user_id)
            else:
                QMessageBox.warning(self.app, '로그인 오류', '사용자 정보를 가져오는데 실패했습니다.')
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
