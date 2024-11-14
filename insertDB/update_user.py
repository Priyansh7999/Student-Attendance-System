from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
import sqlite3

class UpdateUserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update User")
        self.setFixedSize(500, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Employee ID field to search user
        search_label = QLabel("Enter Employee ID to Search:")
        self.search_employee_id = QLineEdit()
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_user)
        
        # Add search fields to layout
        layout.addWidget(search_label)
        layout.addWidget(self.search_employee_id)
        layout.addWidget(search_btn)
        
        # Username, Password, and Employee ID fields with labels
        self.username_label = QLabel("Username:")
        self.username = QLineEdit()
        self.username.setDisabled(True)
        
        self.password_label = QLabel("Password:")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setDisabled(True)
        
        self.employee_id_label = QLabel("Employee ID:")
        self.employee_id = QLineEdit()
        self.employee_id.setDisabled(True)
        
        # Update and Delete buttons
        update_btn = QPushButton("Update User")
        update_btn.clicked.connect(self.update_user)
        
        delete_btn = QPushButton("Delete User")
        delete_btn.clicked.connect(self.delete_user)
        
        # Initially hide these fields and buttons
        self.username_label.hide()
        self.username.hide()
        self.password_label.hide()
        self.password.hide()
        self.employee_id_label.hide()
        self.employee_id.hide()
        update_btn.hide()
        delete_btn.hide()
        
        # Add user detail fields and buttons to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password)
        layout.addWidget(self.employee_id_label)
        layout.addWidget(self.employee_id)
        layout.addWidget(update_btn)
        layout.addWidget(delete_btn)

        # Store buttons for later access to show/hide
        self.update_btn = update_btn
        self.delete_btn = delete_btn

    def search_user(self):
        employee_id = self.search_employee_id.text()
        if not employee_id:
            QMessageBox.warning(self, 'Warning', 'Please enter an Employee ID to search!', QMessageBox.Ok)
            return
        
        conn = None
        try:
            conn = sqlite3.connect('database/login.db')
            cursor = conn.cursor()
            cursor.execute("SELECT username, password, employee_id FROM users WHERE employee_id = ?", (employee_id,))
            result = cursor.fetchone()
            
            if result:
                # Show user details fields if a user is found
                self.username_label.show()
                self.username.show()
                self.password_label.show()
                self.password.show()
                self.employee_id_label.show()
                self.employee_id.show()
                self.update_btn.show()
                self.delete_btn.show()

                # Populate fields with user data
                self.username.setText(result[0])
                self.password.setText(result[1])
                self.employee_id.setText(result[2])

                # Enable editing for fields
                self.username.setDisabled(False)
                self.password.setDisabled(False)
                self.employee_id.setDisabled(False)
            else:
                QMessageBox.information(self, 'Not Found', 'No user found with this Employee ID.', QMessageBox.Ok)
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}', QMessageBox.Ok)
        
        finally:
            if conn:
                conn.close()
    
    def update_user(self):
        if not self.username.text() or not self.password.text() or not self.employee_id.text():
            QMessageBox.warning(self, 'Warning', 'Please fill in all fields!', QMessageBox.Ok)
            return
        
        conn = None
        try:
            conn = sqlite3.connect('database/login.db')
            cursor = conn.cursor()
            
            cursor.execute('''UPDATE users SET username = ?, password = ?, employee_id = ? 
                              WHERE employee_id = ?''',
                           (self.username.text(), self.password.text(), self.employee_id.text(), 
                            self.search_employee_id.text()))
            
            conn.commit()
            QMessageBox.information(self, 'Success', 'User data has been updated successfully!', QMessageBox.Ok)
            
            # Clear the fields
            self.clear_fields()
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}', QMessageBox.Ok)
        
        finally:
            if conn:
                conn.close()

    def delete_user(self):
        employee_id = self.employee_id.text()
        if not employee_id:
            QMessageBox.warning(self, 'Warning', 'Please search and select a user to delete!', QMessageBox.Ok)
            return
        
        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete this user?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            conn = None
            try:
                conn = sqlite3.connect('database/login.db')
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM users WHERE employee_id = ?", (employee_id,))
                conn.commit()
                
                QMessageBox.information(self, 'Deleted', 'User has been deleted successfully!', QMessageBox.Ok)
                
                # Clear the fields
                self.clear_fields()
            
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}', QMessageBox.Ok)
            
            finally:
                if conn:
                    conn.close()
    
    def clear_fields(self):
        # Clear the input fields and hide the user details section
        self.search_employee_id.clear()
        self.username.clear()
        self.password.clear()
        self.employee_id.clear()
        self.username.setDisabled(True)
        self.password.setDisabled(True)
        self.employee_id.setDisabled(True)
        
        # Hide user detail fields and buttons
        self.username_label.hide()
        self.username.hide()
        self.password_label.hide()
        self.password.hide()
        self.employee_id_label.hide()
        self.employee_id.hide()
        self.update_btn.hide()
        self.delete_btn.hide()
