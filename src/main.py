
#이 코드는 PyQt5를 사용하여 식단 관리 프로그램의 사용자 인터페이스를 생성하는 Python 스크립트입니다. 
import sys # sys 모듈을 임포트합니다 (시스템 관련 파라미터와 함수에 접근)
from PyQt5.QtWidgets import * # PyQt5의 QtWidgets 모듈을 임포트합니다 (GUI 컴포넌트 제공)
from ui_manager import UIManager # ui_manager 모듈에서 UIManager 클래스를 임포트합니다
from event_handler import EventHandler # event_handler 모듈에서 EventHandler 클래스를 임포트합니다

class MyApp(QWidget): # MyApp 클래스 정의, PyQt5의 QWidget을 상속
    def __init__(self): # 생성자 메서드
        super().__init__() # 부모 클래스의 생성자 호출
        self.user_credentials = {} # 사용자 자격증명을 저장하기 위한 딕셔너리 초기화
        self.ui_manager = UIManager(self) # UIManager 인스턴스 생성
        self.event_handler = EventHandler(self) # EventHandler 인스턴스 생성
        self.initUI() # 사용자 인터페이스 초기화 메서드 호출

    def initUI(self): # 사용자 인터페이스 초기화 메서드
        self.setWindowTitle('식단관리프로그램') # 윈도우 제목 설정
        self.resize(1000, 500) # 윈도우 크기 설정
        self.ui_manager.center() # 윈도우를 화면 중앙에 위치시킴
        self.ui_manager.create_login_widgets() # 로그인 위젯 생성
        self.ui_manager.create_buttons() # 버튼 생성
        self.show() # 윈도우 표시

if __name__ == '__main__': # 이 스크립트가 직접 실행될 때만 아래 코드 실행
    app = QApplication(sys.argv) # QApplication 인스턴스 생성
    ex = MyApp() # MyApp 인스턴스 생성
    sys.exit(app.exec_()) # 이벤트 루프 시작 및 앱 종료 시 시스템 종료 코드 반환
