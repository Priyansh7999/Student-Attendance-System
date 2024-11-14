from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame, QHBoxLayout, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QLinearGradient, QPalette, QColor
import sqlite3
from .student import StudentWindow
from insert_data import InsertDataWindow  # Import the InsertData window

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(1500, 1500)
        
        # Set gradient background
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0.0, QColor(63, 81, 181))
        gradient.setColorAt(1.0, QColor(25, 118, 210))
        
        palette = self.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create a container frame with border
        container = QFrame()
        container.setFrameShape(QFrame.Box)
        container.setFixedWidth(600)
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border: 2px solid white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignCenter)
        
        # Create widgets
        title = QLabel("Login")
        title.setStyleSheet("color: white; font-size: 30px; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(400)
        self.username.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                background: white;
                margin: 10px;
            }
        """)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(400)
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                background: white;
                margin: 10px;
            }
        """)
        
        login_btn = QPushButton("Login")
        login_btn.setFixedWidth(400)
        login_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #4CAF50;
                color: white;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        login_btn.clicked.connect(self.login)
        
        # Add widgets to container layout
        container_layout.addWidget(title)
        container_layout.addWidget(self.username)
        container_layout.addWidget(self.password)
        container_layout.addWidget(login_btn)
        
        # Add "Registry Member" button below login button
        registry_member_btn = QPushButton("Registry Member")
        registry_member_btn.setFixedWidth(400)
        registry_member_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #4CAF50;
                color: white;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background: darkred;
            }
        """)
        registry_member_btn.clicked.connect(self.registry_member_login)
        
        # Add "Registry Member" button to container layout
        container_layout.addWidget(registry_member_btn)
        
        # Add container to main layout
        main_layout.addWidget(container)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        
        conn = sqlite3.connect('database/login.db')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT * FROM users 
                         WHERE username = ? AND password = ?''', 
                      (username, password))
        
        if cursor.fetchone():
            self.student_window = StudentWindow()
            self.student_window.show()
            self.username.clear()
            self.password.clear()
            # self.close()
        else:
            QMessageBox.critical(self, 'Error', 'No User Found!', 
                                QMessageBox.Ok)
            
        conn.close()

    def registry_member_login(self):
        username = self.username.text()
        password = self.password.text()
        
        # Check if the username and password are correct
        conn = sqlite3.connect('database/login.db')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT * FROM users 
                         WHERE username = ? AND password = ?''', 
                      (username, password))
        
        if cursor.fetchone():
            # Prompt for the registry member access password
            registry_password, ok = QInputDialog.getText(self, "Registry Member Access", 
                                                         "Enter Registry Member Password:", QLineEdit.Password)
            if ok and registry_password == "JUETGUNA":
                self.open_insert_data()
            else:
                QMessageBox.critical(self, 'Error', 'Wrong registry member password!', QMessageBox.Ok)
        else:
            QMessageBox.critical(self, 'Error', 'Invalid username or password!', QMessageBox.Ok)
        
        conn.close()

    def open_insert_data(self):
        # Open the InsertData window for the registry member
        self.insert_data_window = InsertDataWindow()
        self.insert_data_window.show()
