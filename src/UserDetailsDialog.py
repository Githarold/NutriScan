# 주요 기능: 사용자 상세 정보(이름, 성별, 나이, 체중, 키, 알레르기 정보)를 입력받는 대화상자 구현
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox

class UserDetailsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI() # 사용자 인터페이스 초기화

    def initUI(self):
        self.setWindowTitle('사용자 상세 정보') # 창 제목 설정
        self.setGeometry(100, 100, 300, 200) # 창 위치 및 크기 설정

        layout = QVBoxLayout() # 수직 레이아웃

        # 이름 입력 위젯
        self.name_label = QLabel('이름:', self)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # 성별 선택 위젯
        self.gender_label = QLabel('성별:', self)
        self.gender_input = QComboBox(self)
        self.gender_input.addItems(['남성', '여성', '기타'])
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_input)

        # 나이 입력 위젯
        self.age_label = QLabel('나이:', self)
        self.age_input = QLineEdit(self)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

        # 체중 입력 위젯
        self.weight_label = QLabel('체중(kg):', self)
        self.weight_input = QLineEdit(self)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        # 키 입력 위젯
        self.height_label = QLabel('키(cm):', self)
        self.height_input = QLineEdit(self)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # 알레르기 정보 입력 위젯
        self.allergy_label = QLabel('알레르기 정보:', self)
        self.allergy_input = QLineEdit(self)
        layout.addWidget(self.allergy_label)
        layout.addWidget(self.allergy_input)

        # 확인 버튼
        self.submit_button = QPushButton('확인', self)
        self.submit_button.clicked.connect(self.submit_info) # 클릭 이벤트 연결
        layout.addWidget(self.submit_button)

        self.setLayout(layout) # 레이아웃 설정

    def submit_info(self):
        # 숫자로 변환 가능한지 확인하는 함수
        def is_number(s):
            try:
                float(s) # 숫자로 변환 시도
                return True
            except ValueError:
                return False

        # 입력된 나이, 체중, 키가 숫자인지 확인
        if not (is_number(self.age_input.text()) and 
                is_number(self.weight_input.text()) and 
                is_number(self.height_input.text())):
            QMessageBox.warning(self, "입력 오류", "나이, 체중, 키는 숫자로 입력해야 합니다.")
            return

        # 모든 입력이 유효한 경우, 사용자 정보 저장
        self.user_info = {
            'name': self.name_input.text(),
            'gender': self.gender_input.currentText(),
            'age': self.age_input.text(),
            'weight': self.weight_input.text(),
            'height': self.height_input.text(),
            'allergies': self.allergy_input.text()
        }
        self.accept() # 다이얼로그를 성공적으로 닫음

    def get_user_info(self):
        return self.user_info # 저장된 사용자 정보 반환
