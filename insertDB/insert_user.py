from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                            QLineEdit, QPushButton, QMessageBox)
import sqlite3

class InsertUserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert User")
        self.setFixedSize(500, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Username field with label
        username_label = QLabel("Enter Username:")
        self.username = QLineEdit()
        
        # Password field with label
        password_label = QLabel("Enter Password:")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        
        # Employee ID field with label
        employee_id_label = QLabel("Enter Employee ID:")
        self.employee_id = QLineEdit()
        
        insert_btn = QPushButton("Insert User")
        insert_btn.clicked.connect(self.insert_user)
        
        # Add widgets to layout
        layout.addWidget(username_label)
        layout.addWidget(self.username)
        layout.addWidget(password_label)
        layout.addWidget(self.password)
        layout.addWidget(employee_id_label)
        layout.addWidget(self.employee_id)
        layout.addWidget(insert_btn)

    def check_if_exists(self, conn, employee_id):
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE employee_id = ?", (employee_id,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def insert_user(self):
        if not self.username.text() or not self.password.text() or not self.employee_id.text():
            QMessageBox.warning(self, 'Warning',
                              'Please fill in all fields!',
                              QMessageBox.Ok)
            return
        
        conn = None
        try:
            conn = sqlite3.connect('database/login.db')
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (username TEXT UNIQUE,
                             password TEXT,
                             employee_id TEXT PRIMARY KEY)''')
            
            # Check if employee_id already exists
            if self.check_if_exists(conn, self.employee_id.text()):
                QMessageBox.critical(self, 'Error',
                                   'Employee ID already exists!',
                                   QMessageBox.Ok)
                return
            
            # Insert new user
            cursor.execute('''INSERT INTO users (username, password, employee_id)
                            VALUES (?, ?, ?)''',
                          (self.username.text(), self.password.text(),
                           self.employee_id.text()))
            
            conn.commit()
            
            QMessageBox.information(self, 'Success',
                                  'User data has been added to database!',
                                  QMessageBox.Ok)
            
            # Clear the fields
            self.username.clear()
            self.password.clear()
            self.employee_id.clear()
            
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                QMessageBox.critical(self, 'Error',
                                   'Username already exists!',
                                   QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Error',
                                   'Employee ID already exists!',
                                   QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Error',
                               f'An error occurred: {str(e)}',
                               QMessageBox.Ok)
        finally:
            if conn:
                conn.close()