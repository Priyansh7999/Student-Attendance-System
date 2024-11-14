import sys
import os
import cv2
import sqlite3
import threading
import time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QMessageBox, QHBoxLayout)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class InsertStudentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student")
        self.setFixedSize(1100, 500)

        # Create a central widget and set the layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)  # Use horizontal layout

        # Left side layout for student details
        left_layout = QVBoxLayout()
        
        # Name field with label
        name_label = QLabel("Enter Student Name:")
        self.name = QLineEdit()
        
        # Enrollment field with label
        enrollment_label = QLabel("Enter Enrollment Number:")
        self.enrollment = QLineEdit()
        
        # Study year field with label
        study_year_label = QLabel("Enter the Year:")
        self.study_year_combo = QComboBox()
        self.study_year_combo.addItems(["I", "II", "III", "IV"])
        
        # Batch field with label
        batch_label = QLabel("Enter the Batch:")
        self.batch_combo = QComboBox()
        self.batch_combo.addItems([f"B{i}" for i in range(1, 15)])
        
        insert_btn = QPushButton("Insert Student")
        insert_btn.clicked.connect(self.insert_student)

        # Add widgets to left layout
        left_layout.addWidget(name_label)
        left_layout.addWidget(self.name)
        left_layout.addWidget(enrollment_label)
        left_layout.addWidget(self.enrollment)
        left_layout.addWidget(study_year_label)
        left_layout.addWidget(self.study_year_combo)
        left_layout.addWidget(batch_label)
        left_layout.addWidget(self.batch_combo)
        left_layout.addWidget(insert_btn)

        # Add left layout to the main layout
        layout.addLayout(left_layout)

        # Video stream section
        self.video_label = QLabel()
        layout.addWidget(self.video_label)

        self.take_photo_btn = QPushButton("Take Photos")
        self.take_photo_btn.clicked.connect(self.take_photos)
        left_layout.addWidget(self.take_photo_btn)

        # Start video capture
        self.cap = cv2.VideoCapture(0)  # Change the index if you have multiple cameras
        self.timer = threading.Thread(target=self.update_frame)
        self.timer.daemon = True
        self.timer.start()

    def update_frame(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def check_if_exists(self, conn, enrollment):
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE enrollment_number = ?", (enrollment,))
        count = cursor.fetchone()[0]
        return count > 0
    
    def insert_student(self):
        if not self.name.text() or not self.enrollment.text():
            QMessageBox.warning(self, 'Warning',
                              'Please fill in all fields!',
                              QMessageBox.Ok)
            return
        
        conn = None
        try:
            conn = sqlite3.connect('database/student_detail.db', timeout=10)
            conn.execute("PRAGMA busy_timeout = 5000")  # Set timeout to 5 seconds
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS students
                            (name TEXT,
                             enrollment_number TEXT PRIMARY KEY,
                             batch TEXT,
                             study_year TEXT)''')
            
            # Check if enrollment number already exists
            if self.check_if_exists(conn, self.enrollment.text()):
                QMessageBox.critical(self, 'Error',
                                   'Enrollment number already exists!',
                                   QMessageBox.Ok)
                return
            
            # Insert new student
            cursor.execute('''INSERT INTO students
                            (name, enrollment_number, batch, study_year)
                            VALUES (?, ?, ?, ?)''', 
                           (self.name.text(), 
 self.enrollment.text(), 
                            self.batch_combo.currentText(), 
                            self.study_year_combo.currentText()))
            conn.commit()
            QMessageBox.information(self, 'Success',
                                    'Student inserted successfully!',
                                    QMessageBox.Ok)
            self.clear_fields()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error',
                                 str(e),
                                 QMessageBox.Ok)
        finally:
            if conn:
                conn.close()

    def clear_fields(self):
        self.name.clear()
        self.enrollment.clear()
        self.study_year_combo.setCurrentIndex(0)
        self.batch_combo.setCurrentIndex(0)

    def take_photos(self):
        enrollment_number = self.enrollment.text()
        if not enrollment_number:
            QMessageBox.warning(self, 'Warning',
                                'Please enter an enrollment number to take photos!',
                                QMessageBox.Ok)
            return
        
        # Create a directory for the student in the "training" folder if it doesn't exist
        directory = f"training/{enrollment_number}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Capture and save 3 photos with a 1-second delay
        for i in range(3):
            ret, frame = self.cap.read()
            if ret:
                photo_path = os.path.join(directory, f"{enrollment_number}_{i + 1}.jpg")
                cv2.imwrite(photo_path, frame)
                time.sleep(1)  # Wait for 1 second before taking the next photo
            else:
                QMessageBox.critical(self, 'Error',
                                     'Failed to capture photo!',
                                     QMessageBox.Ok)
                return
        
        QMessageBox.information(self, 'Success',
                                f'3 photos saved in {directory}!',
                                QMessageBox.Ok)

    def closeEvent(self, event):
        self.cap.release()  # Release the camera when closing the app
        event.accept()
