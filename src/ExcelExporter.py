from PyQt5.QtWidgets import *
import pandas as pd


class ExcelExporter(QDialog):
    def __init__(self, user_credentials):
        super().__init__()
        self.user_credentials = user_credentials    # Store the user credentials
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle('엑셀로 내보내기')  
        self.setGeometry(100, 100, 300, 100)
        self.center()  # Function call to center the window on the screen
        layout = QVBoxLayout()

        # Button for exporting data to Excel
        export_button = QPushButton('내보내기', self)
        export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(export_button)

        self.setLayout(layout)

    def export_to_excel(self):
        # Create DataFrame with user information and diet information
        data = []
        for user_id, info in self.user_credentials.items():
            user_data = info.get('details', {}).copy()
            user_data['id'] = user_id

           # Process diet information
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
                                'sugar': meal.get('nutrition', {}).get('당류', ''),
                                'sodium': meal.get('nutrition', {}).get('나트륨', '')
                            })
                            data.append(meal_data)
            else:
                # If there is no diet information, add only the basic user information
                user_data.update({
                    'date': '',
                    'meal_time': '',
                    'food_name': '',
                    'calories': '',
                    'carbs': '',
                    'protein': '',
                    'fat': '',
                    'sugar': '',
                    'sodium': ''
                })
                data.append(user_data)

        df = pd.DataFrame(data)

        # Save the DataFrame as an Excel file
        filename = 'user_credentials.xlsx'
        df.to_excel(filename, index=False)
        QMessageBox.information(self, '내보내기 완료', f'사용자 정보가 "{filename}" 파일로 저장되었습니다.')
        print(self.user_credentials)

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
