from PyQt5.QtWidgets import *
import pandas as pd

class ExcelExporter(QDialog):
    def __init__(self, user_credentials):
        super().__init__()
        self.user_credentials = user_credentials
        self.initUI()

    def initUI(self):
        self.setWindowTitle('엑셀로 내보내기')  
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()  

        export_button = QPushButton('내보내기', self)
        export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(export_button)

        self.setLayout(layout)

    def export_to_excel(self):
        # 사용자 정보와 식단 정보를 포함한 DataFrame 생성
        data = []
        for user_id, info in self.user_credentials.items():
            user_data = info.get('details', {}).copy()
            user_data['id'] = user_id

            # 식단 정보 처리
            diet_info = info.get('diet', {})
            if diet_info:
                for date, meals in diet_info.items():
                    for meal_time, meal_list in meals.items():
                        for meal in meal_list:
                            meal_data = user_data.copy()
                            meal_data.update({
                                'date': date,
                                'meal_time': meal_time,
                                'food_name': meal.get('name', ''),
                                'calories': meal.get('nutrition', {}).get('칼로리', ''),
                                'carbs': meal.get('nutrition', {}).get('탄수화물', ''),
                                'protein': meal.get('nutrition', {}).get('단백질', ''),
                                'fat': meal.get('nutrition', {}).get('지방', ''),
                                'image_url': meal.get('image_url', '')
                            })
                            data.append(meal_data)
            else:
                # 식단 정보가 없는 경우, 기본 사용자 정보만 추가
                user_data.update({
                    'date': '',
                    'meal_time': '',
                    'food_name': '',
                    'calories': '',
                    'carbs': '',
                    'protein': '',
                    'fat': '',
                    'image_url': ''
                })
                data.append(user_data)

        df = pd.DataFrame(data)

        # 엑셀 파일로 저장
        filename = 'user_credentials.xlsx'
        df.to_excel(filename, index=False)
        QMessageBox.information(self, '내보내기 완료', f'사용자 정보가 "{filename}" 파일로 저장되었습니다.')