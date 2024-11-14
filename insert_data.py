import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QPalette, QColor
from insertDB.insert_user import InsertUserWindow
from insertDB.insert_student import InsertStudentWindow
from insertDB.update_user import UpdateUserWindow
from insertDB.update_student import UpdateStudentWindow
from encode import encode_known_faces  # Import the encode_faces function from encode.py

class InsertDataWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Management Panel")
        self.setFixedSize(1500, 1500)
        
        # Set gradient background
        gradient = QLinearGradient(0, 0, 0, 300)
        gradient.setColorAt(0.0, QColor(63, 81, 181))
        gradient.setColorAt(1.0, QColor(25, 118, 210))
        
        palette = self.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Add title
        title = QLabel("Data Management Panel")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        
        # Create buttons for insertion
        insert_user_btn = QPushButton("Insert New User")
        insert_user_btn.setStyleSheet(self.get_button_style("#4CAF50", "#45f149"))
        insert_user_btn.clicked.connect(self.open_user_window)
        
        insert_student_btn = QPushButton("Insert New Student")
        insert_student_btn.setStyleSheet(self.get_button_style("#2196F3", "#1910E2"))
        insert_student_btn.clicked.connect(self.open_student_window)
        
        # Create buttons for updating
        update_user_btn = QPushButton("Update User")
        update_user_btn.setStyleSheet(self.get_button_style("#FFC107", "#FFB300"))
        update_user_btn.clicked.connect(self.open_update_user_window)
        
        update_student_btn = QPushButton("Update Student")
        update_student_btn.setStyleSheet(self.get_button_style("#FF5722", "#E64A19"))
        update_student_btn.clicked.connect(self.open_update_student_window)

        # Create "Encode Face" button
        encode_face_btn = QPushButton("Encode Face")
        encode_face_btn.setStyleSheet(self.get_button_style("#673AB7", "#512DA8"))
        encode_face_btn.clicked.connect(self.encode_faces)

        back_button = QPushButton("Back")
        back_button.setStyleSheet(self.get_button_style("#F44336", "#D32F2F"))
        back_button.move(100, 10)
        back_button.clicked.connect(self.on_back_button_clicked)
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(insert_user_btn)
        layout.addWidget(insert_student_btn)
        layout.addWidget(update_user_btn)
        layout.addWidget(update_student_btn)
        layout.addWidget(encode_face_btn)
        layout.addWidget(back_button)
        
    def get_button_style(self, color, hover_color):
        return f"""
            QPushButton {{
                padding: 15px;
                background: {color};
                color: white;
                border-radius: 5px;
                margin: 10px;
                font-size: 30px;
                min-width: 200px;
            }}
            QPushButton:hover {{
                background: {hover_color};
            }}
        """

    def open_user_window(self):
        self.user_window = InsertUserWindow()
        self.user_window.show()
    
    def open_student_window(self):
        self.student_window = InsertStudentWindow()
        self.student_window.show()
    
    def open_update_user_window(self):
        self.update_user_window = UpdateUserWindow()
        self.update_user_window.show()
    
    def open_update_student_window(self):
        self.update_student_window = UpdateStudentWindow()
        self.update_student_window.show()

    def encode_faces(self):
        # Call the encode_faces function from encode.py
        encode_known_faces()
        # Display a message or update the GUI to show the result of face encoding

    def on_back_button_clicked(self):
        # Close the current window
        self.close()

def main():
    app = QApplication(sys.argv)
    window = InsertDataWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()