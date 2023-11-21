# 주요 기능: PyQt5를 사용하여 식단 관리 프로그램의 이벤트 처리를 담당하는 EventHandler 클래스
from PyQt5.QtWidgets import QMessageBox
from UserDetailsDialog import UserDetailsDialog
from home import Home

class EventHandler:
    def __init__(self, app):
        self.app = app # 메인 애플리케이션 인스턴스 참조

    def signup_clicked(self):
        user_id = self.app.id_input.text() # ID 입력 필드의 텍스트 추출
        user_pw = self.app.pw_input.text() # 비밀번호 입력 필드의 텍스트 추출
        # 이미 존재하는 ID인 경우 경고 메시지 표시
        if user_id in self.app.user_credentials:
            QMessageBox.warning(self.app, '회원가입 오류', '이미 존재하는 ID입니다.')
        # ID와 비밀번호가 모두 입력된 경우
        elif user_id and user_pw:
            # 사용자 자격증명에 사용자 추가
            self.app.user_credentials[user_id] = {'password': user_pw, 'details': {}}
            # 회원가입 성공 메시지 표시
            QMessageBox.information(self.app, '회원가입 성공', '회원가입이 완료되었습니다.')
            # 사용자 상세 정보 다이얼로그 열기
            self.open_user_details_dialog(user_id)
        else:
            # ID와 비밀번호가 누락된 경우 경고 메시지 표시
            QMessageBox.warning(self.app, '회원가입 오류', 'ID와 비밀번호를 모두 입력해주세요.')

    def signin_clicked(self):
        user_id = self.app.id_input.text() # ID 입력 필드의 텍스트 추출
        user_pw = self.app.pw_input.text() # 비밀번호 입력 필드의 텍스트 추출
        # 사용자 자격증명 확인
        if self.app.user_credentials.get(user_id, {}).get('password') == user_pw:
            # 로그인 성공 메시지 표시
            QMessageBox.information(self.app, '로그인 성공', '로그인이 성공적으로 이루어졌습니다.')
            # 홈 다이얼로그 열기
            self.open_home_dialog(user_id)
        else:
            # ID 또는 비밀번호 오류 시 경고 메시지 표시
            QMessageBox.warning(self.app, '로그인 오류', 'ID 또는 비밀번호가 잘못되었습니다.')

    def open_home_dialog(self, user_id):
        dialog = Home(user_id, self.app.user_credentials) # 홈 다이얼로그 생성
        dialog.exec_() # 다이얼로그 실행

    def open_user_details_dialog(self, user_id):
        dialog = UserDetailsDialog() # 사용자 상세 정보 다이얼로그 생성
        if dialog.exec_(): # 다이얼로그 실행
            user_details = dialog.get_user_info() # 사용자 상세 정보 추출
            # 사용자 자격증명에 상세 정보 추가
            self.app.user_credentials[user_id]['details'] = user_details
