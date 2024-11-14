from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QMessageBox)
import sqlite3

class UpdateStudentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student")
        self.setFixedSize(500, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Enrollment field to search for student
        enrollment_label = QLabel("Enter Enrollment Number:")
        self.enrollment_search = QLineEdit()
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_student)
        
        # Fields for student details
        self.name_label = QLabel("Student Name:")
        self.name = QLineEdit()
        
        self.study_year_label = QLabel("Study Year:")
        self.study_year_combo = QComboBox()
        self.study_year_combo.addItems(["I", "II", "III", "IV"])
        
        self.batch_label = QLabel("Batch:")
        self.batch_combo = QComboBox()
        self.batch_combo.addItems([f"B{i}" for i in range(1, 15)])
        
        # Update and Delete buttons
        self.update_btn = QPushButton("Update Student")
        self.update_btn.clicked.connect(self.update_student)
        
        self.delete_btn = QPushButton("Delete Student")
        self.delete_btn.clicked.connect(self.delete_student)
        
        # Add initial widgets to layout (only Enrollment and Search button)
        layout.addWidget(enrollment_label)
        layout.addWidget(self.enrollment_search)
        layout.addWidget(search_btn)
        
        # Add student detail fields and buttons to layout but hide them initially
        layout.addWidget(self.name_label)
        layout.addWidget(self.name)
        layout.addWidget(self.study_year_label)
        layout.addWidget(self.study_year_combo)
        layout.addWidget(self.batch_label)
        layout.addWidget(self.batch_combo)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.delete_btn)
        
        # Initially hide student detail fields and action buttons
        self.name_label.hide()
        self.name.hide()
        self.study_year_label.hide()
        self.study_year_combo.hide()
        self.batch_label.hide()
        self.batch_combo.hide()
        self.update_btn.hide()
        self.delete_btn.hide()

    def search_student(self):
        enrollment = self.enrollment_search.text()
        
        if not enrollment:
            QMessageBox.warning(self, 'Warning', 'Please enter an enrollment number!', QMessageBox.Ok)
            return

        conn = None
        try:
            conn = sqlite3.connect('database/student_detail.db')
            cursor = conn.cursor()
            
            # Search for student by enrollment number
            cursor.execute("SELECT * FROM students WHERE enrollment_number = ?", (enrollment,))
            student = cursor.fetchone()
            
            if student:
                # Populate fields if student is found
                self.name.setText(student[0])
                self.study_year_combo.setCurrentText(student[3])
                self.batch_combo.setCurrentText(student[2])
                
                # Show and enable fields for updating
                self.name_label.show()
                self.name.show()
                self.study_year_label.show()
                self.study_year_combo.show()
                self.batch_label.show()
                self.batch_combo.show()
                self.update_btn.show()
                self.delete_btn.show()

                self.name.setEnabled(True)
                self.study_year_combo.setEnabled(True)
                self.batch_combo.setEnabled(True)
                self.update_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Warning', 'No student found with that enrollment number.', QMessageBox.Ok)
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}', QMessageBox.Ok)
        finally:
            if conn:
                conn.close()

    def update_student(self):
        enrollment = self.enrollment_search.text()
        name = self.name.text()
        study_year = self.study_year_combo.currentText()
        batch = self.batch_combo.currentText()
        
        if not name:
            QMessageBox.warning(self, 'Warning', 'Please fill in the name field!', QMessageBox.Ok)
            return

        conn = None
        try:
            conn = sqlite3.connect('database/student_detail.db')
            cursor = conn.cursor()
            
            # Update student details in the database
            cursor.execute('''UPDATE students SET name = ?, study_year = ?, batch = ?
                            WHERE enrollment_number = ?''', (name, study_year, batch, enrollment))
            conn.commit()
            
            QMessageBox.information(self, 'Success', 'Student details updated successfully!', QMessageBox.Ok)
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}', QMessageBox.Ok)
        finally:
            if conn:
                conn.close()

    def delete_student(self):
        enrollment = self.enrollment_search.text()
        
        conn = None
        try:
            conn = sqlite3.connect('database/student_detail.db')
            cursor = conn.cursor()
            
            # Delete student from the database
            cursor.execute("DELETE FROM students WHERE enrollment_number = ?", (enrollment,))
            conn.commit()
            
            QMessageBox.information(self, 'Success', 'Student deleted successfully!', QMessageBox.Ok)
            
            # Clear fields and disable them
            self.enrollment_search.clear()
            self.name.clear()
            self.name.setEnabled(False)
            self.study_year_combo.setEnabled(False)
            self.batch_combo.setEnabled(False)
            self.name_label.hide()
            self.name.hide()
            self.study_year_label.hide()
            self.study_year_combo.hide()
            self.batch_label.hide()
            self.batch_combo.hide()
            self.update_btn.hide()
            self.delete_btn.hide()
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}', QMessageBox.Ok)
        finally:
            if conn:
                conn.close()
