from PyQt5.QtWidgets import *
from EditDietInfoDialog import EditDietInfoDialog


class DietInfoDialog(QDialog):
    def __init__(self, diet_data, user_id):
        super().__init__()
        self.diet_data = diet_data  # Store the diet data
        self.user_id = user_id      # Store the user ID
        self.initUI()


    def initUI(self):
        # Set the window title and size
        self.setWindowTitle('식단 정보 확인')
        self.setGeometry(100, 100, 300, 300)
        self.center()  # Call function to center the window on the screen
        layout = QVBoxLayout()

        # Date selection combo box
        self.date_combo = QComboBox(self)
        
        # Sort dates in descending order
        sorted_dates = sorted(self.diet_data.keys(), reverse=True)
        self.date_combo.addItems(sorted_dates)
        self.date_combo.currentIndexChanged.connect(self.display_diet_info)
        layout.addWidget(self.date_combo)

        # Label to display diet information
        self.diet_info_label = QLabel(self)
        layout.addWidget(self.diet_info_label)

        # Display initial diet information
        self.display_diet_info(0)

        # Button to edit diet information
        self.edit_button = QPushButton('식단 정보 수정', self)
        self.edit_button.clicked.connect(self.open_edit_dialog)
        layout.addWidget(self.edit_button)
        self.setLayout(layout)

        # Set the initial selection of the combo box to the most recent date
        if sorted_dates:
            self.date_combo.setCurrentIndex(0)

    def display_diet_info(self, index):
        # Display the diet information for the selected date
        date = self.date_combo.itemText(index)
        daily_diet = self.diet_data.get(date, {})
        diet_info = f"날짜: {date}\n"
        
        for meal, foods in daily_diet.items():
            diet_info += f"{meal}:\n"
            for food in foods:
                if isinstance(food, dict):
                    # In case the food item is a dictionary (includes nutrition information)
                    food_name = food.get('name', 'N/A')
                    nutrition = food.get('nutrition', {})
                    
                    # Add units 'kcal' and 'g'
                    diet_info += (f"  - {food_name} (칼로리: {nutrition.get('칼로리', 'N/A')} kcal, "
                                  f"탄수화물: {nutrition.get('탄수화물', 'N/A')} g, "
                                  f"지방: {nutrition.get('지방', 'N/A')} g, "
                                  f"단백질: {nutrition.get('단백질', 'N/A')} g, "
                                  f"당류: {nutrition.get('당류', 'N/A')} g, "
                                  f"나트륨: {nutrition.get('나트륨', 'N/A')} mg")
                    diet_info += "\n"
                    
                else:
                    # In case the food item is a string (no nutrition information)
                    diet_info += f"  - {food}\n"
        self.diet_info_label.setText(diet_info)

    def open_edit_dialog(self):
        # Open the dialog to edit diet information
        edit_dialog = EditDietInfoDialog(self.diet_data)
        
        if edit_dialog.exec_():
            # Update diet data and display the updated information
            self.diet_data = edit_dialog.get_diet_data()
            self.display_diet_info(self.date_combo.currentIndex())

    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
