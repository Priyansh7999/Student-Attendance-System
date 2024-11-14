import cv2
import face_recognition
import pickle
from PyQt5.QtCore import Qt, QTimer
from pathlib import Path
import logging
import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QColor

class StudentAttendance:
    def __init__(self):
        self.camera = None
        self.attendance_active = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)
        self.recognized_students = set()

    def fetch_students(self, selected_batches, selected_year):
        conn = sqlite3.connect('database/student_detail.db')
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(selected_batches))
        query = f'''SELECT name, enrollment_number, batch 
                FROM students 
                WHERE batch IN ({placeholders})
                AND study_year = ?
                ORDER BY batch, name ASC'''
        
        cursor.execute(query, selected_batches + [selected_year])
        students = cursor.fetchall()
        conn.close()
        
        return students

    def start_attendance(self, table):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open camera!")
            
        self.attendance_active = True
        self.timer.start(10)  # Process every 1 second
        self.current_table = table

    def process_frame(self):
        if not self.attendance_active:
            return
            
        ret, frame = self.camera.read()
        if not ret:
            return
            
        # Save frame temporarily
        temp_image_path = "temp_frame.jpg"
        cv2.imwrite(temp_image_path, frame)
        
        try:
            results = self.validate_face(temp_image_path)
            if results:
                for name in results.keys():
                    self.mark_attendance(name)
                    
        except Exception as e:
            logging.error(f"Error processing frame: {str(e)}")
            
        cv2.imshow("Attendance Camera", frame)
        cv2.waitKey(1)

    def validate_face(self, image_path, tolerance=0.6):
        try:
            with Path("output/encodings.pkl").open(mode="rb") as f:
                loaded_encodings = pickle.load(f)

            input_image = face_recognition.load_image_file(image_path)
            input_face_locations = face_recognition.face_locations(input_image, model="hog")
            input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

            results = {}
            for unknown_encoding in input_face_encodings:
                distances = face_recognition.face_distance(
                    loaded_encodings["encodings"], unknown_encoding
                )
                if len(distances) > 0:
                    min_distance = min(distances)
                    if min_distance <= tolerance:
                        index = distances.argmin()
                        name = loaded_encodings["names"][index]
                        results[name] = results.get(name, 0) + 1

            return results
            
        except Exception as e:
            logging.error(f"Error in face validation: {str(e)}")
            return {}

    def mark_attendance(self, recognized_name):
        if recognized_name in self.recognized_students:
            return
            
        for row in range(self.current_table.rowCount()):
            enrollment_item = self.current_table.item(row, 1)
            if enrollment_item and enrollment_item.text() == recognized_name:
                attendance_item = self.current_table.item(row, 3)
                if attendance_item and not attendance_item.text():
                    attendance_item = QTableWidgetItem("PRESENT")
                    font = QFont()
                    font.setPointSize(12)
                    font.setBold(True)
                    attendance_item.setFont(font)
                    attendance_item.setTextAlignment(Qt.AlignCenter)
                    attendance_item.setForeground(QColor("#4CAF50"))
                    self.current_table.setItem(row, 3, attendance_item)
                    self.recognized_students.add(recognized_name)
                    logging.info(f"Marked {recognized_name} as present")
                break

    def close_attendance(self, table):
        # Mark remaining students as absent
        for row in range(table.rowCount()):
            attendance_item = table.item(row, 3)
            if attendance_item and not attendance_item.text():
                absent_item = QTableWidgetItem("ABSENT")
                font = QFont()
                font.setPointSize(12)
                font.setBold(True)
                absent_item.setFont(font)
                absent_item.setTextAlignment(Qt.AlignCenter)
                absent_item.setForeground(QColor("#f44336"))
                table.setItem(row, 3, absent_item)
        
        # Clean up camera resources
        if self.camera is not None:
            self.attendance_active = False
            self.timer.stop()
            self.camera.release()
            cv2.destroyAllWindows()
            self.camera = None
            self.recognized_students.clear()