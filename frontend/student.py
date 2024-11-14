from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                           QComboBox, QPushButton, QLineEdit, QTableWidget,
                           QTableWidgetItem, QScrollArea, QListWidget, 
                           QAbstractItemView, QHeaderView, QMessageBox,QHBoxLayout,QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QLinearGradient, QPalette, QColor, QFont
import sqlite3
from .student_attendance import StudentAttendance
from .save_attendance import AttendanceSaver

class StudentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")
        self.setFixedSize(1500, 1500)
        self.attendance_handler = StudentAttendance()
        self.attendance_saver = AttendanceSaver()
        
        # Set gradient background
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0.0, QColor(63, 81, 181))
        gradient.setColorAt(1.0, QColor(25, 118, 210))
        
        palette = self.palette()
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        
        # Create and style all UI components
        self.create_subject_input(scroll_layout)
        self.create_year_selection(scroll_layout)
        self.create_batch_selection(scroll_layout)
        self.create_submit_button(scroll_layout)
        self.create_table(scroll_layout)
        self.create_attendance_buttons(scroll_layout)
        
        # Add scroll area to main layout
        layout.addWidget(scroll_area)

    def create_subject_input(self, layout):
        subject_label = QLabel("Subject:")
        subject_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)
        
        self.subject_input = QLineEdit()
        self.subject_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 6px;
                background: white;
                margin: 10px;
                font-size: 20px;
                border: 2px solid #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        
        # Create a horizontal layout for date and time inputs
        date_time_layout = QHBoxLayout()
        
        # Add date input field
        date_label = QLabel("Date:")
        date_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-right: 10px;
            }
        """)
        
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("dd/mm/yy")
        self.date_input.setFixedWidth(500)
        self.date_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 6px;
                background: white;
                font-size: 20px;
                border: 2px solid #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        
        # Add time input field
        time_label = QLabel("Time:")
        time_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-left: 20px;
                margin-right: 10px;
            }
        """)
        
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("from - to am/pm")
        self.time_input.setFixedWidth(500)
        self.time_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 6px;
                background: white;
                font-size: 20px;
                border: 2px solid #E0E0E0;
            }
            QLineEdit:focus {
                border: 2px solid #2196F3;
            }
        """)
        
        # Add date and time inputs to the horizontal layout
        date_time_layout.addWidget(date_label)
        date_time_layout.addWidget(self.date_input)
        date_time_layout.addWidget(time_label)
        date_time_layout.addWidget(self.time_input)
        
        layout.addWidget(subject_label)
        layout.addWidget(self.subject_input)
        layout.addLayout(date_time_layout)

    def create_year_selection(self, layout):
        year_label = QLabel("Year:")
        year_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
                margin-top: 10px;
            }
        """)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(['I', 'II', 'III', 'IV'])
        self.year_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border-radius: 6px;
                background: white;
                margin: 10px;
                font-size: 20px;
                border: 2px solid #E0E0E0;
                min-width: 200px;
            }
            QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            QComboBox:hover {
                background: #F5F5F5;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 2px solid #E0E0E0;
                selection-background-color: #2196F3;
                selection-color: white;
                font-size: 20px;
            }
        """)
        
        layout.addWidget(year_label)
        layout.addWidget(self.year_combo)

    def create_batch_selection(self, layout):
        batch_label = QLabel("Select Batches:")
        batch_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 5px;
            }
        """)
        
        self.batch_list = QListWidget()
        self.batch_list.addItems([f"B{i}" for i in range(1, 15)])
        self.batch_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.batch_list.setStyleSheet("""
            QListWidget {
                padding: 8px;
                border-radius: 6px;
                background: white;
                margin: 10px;
                max-height: 200px;
                border: 2px solid #E0E0E0;
                font-size: 20px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: #2196F3;
                color: white;
            }
            QListWidget::item:hover {
                background: #E3F2FD;
                color: black;
            }
        """)
        
        layout.addWidget(batch_label)
        layout.addWidget(self.batch_list)

    def create_submit_button(self, layout):
        submit_container = QWidget()
        submit_container_layout = QVBoxLayout(submit_container)
        
        submit_btn = QPushButton("Submit")
        submit_btn.setFixedWidth(700)
        submit_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: #4CAF50;
                color: white;
                border-radius: 6px;
                margin: 5px auto;
                font-size: 22px;
                font-weight: bold;
                min-width: 120px;
            }
        """)
        submit_btn.clicked.connect(self.show_students)
        
        submit_container_layout.addWidget(submit_btn, 0, Qt.AlignCenter)
        layout.addWidget(submit_container)

    def create_table(self, layout):
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border-radius: 6px;
                margin: 10px;
                border: 2px solid #E0E0E0;
                font-size: 18px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #F5F5F5;
            }
            QTableWidget::item:selected {
                background: #E3F2FD;
                color: black;
            }
            QHeaderView::section {
                background: #1976D2;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 18px;
            }
            QTableWidget::item:alternate {
                background: #F5F5F5;
            }
        """)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

    def create_attendance_buttons(self, layout):
        self.start_btn = QPushButton("START ATTENDANCE")
        self.close_btn = QPushButton("CLOSE ATTENDANCE")
        self.save_btn = QPushButton("SAVE ATTENDANCE")
        
        button_style = """
            QPushButton {
                padding: 15px;
                color: white;
                border-radius: 6px;
                margin: 10px;
                font-size: 20px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
        """
        
        self.start_btn.setStyleSheet(button_style + """
            QPushButton {
                background: #2196F3;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        
        self.close_btn.setStyleSheet(button_style + """
            QPushButton {
                background: #f44336;
            }
            QPushButton:hover {
                background: #d32f2f;
            }
        """)
        
        self.save_btn.setStyleSheet(button_style + """
            QPushButton {
                background: #4CAF50;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        self.back_button = QPushButton("Sign Out")
        self.back_button.setStyleSheet(button_style + """
            QPushButton {
                background: #757575;
            }
            QPushButton:hover {
                background: #616161;
            }
        """)
        
        self.start_btn.clicked.connect(self.start_attendance)
        self.close_btn.clicked.connect(self.close_attendance)
        self.save_btn.clicked.connect(self.save_attendance)
        self.back_button.clicked.connect(self.on_back_button_clicked)
        # Create a 2x2 grid layout for buttons
        button_grid = QGridLayout()
        button_grid.addWidget(self.start_btn, 0, 0)
        button_grid.addWidget(self.close_btn, 0, 1)
        button_grid.addWidget(self.save_btn, 1, 0)
        button_grid.addWidget(self.back_button, 1, 1)
        
        layout.addLayout(button_grid)

    def save_attendance(self):
        if not hasattr(self, 'current_students_data') or self.table.rowCount() == 0:
            QMessageBox.warning(self, "Warning", "No attendance data to save!")
            return

        subject = self.subject_input.text()
        date = self.date_input.text()
        time = self.time_input.text()
        year = self.year_combo.currentText()
        selected_batches = [item.text() for item in self.batch_list.selectedItems()]

        if not all([subject, date, time, year, selected_batches]):
            QMessageBox.warning(self, "Warning", "Please fill all the required fields!")
            return

        self.attendance_saver.save_attendance_to_excel(
            subject,
            date,
            time,
            year,
            selected_batches,
            self.table
        )

    def show_students(self):
        selected_batches = [item.text() for item in self.batch_list.selectedItems()]
        selected_year = self.year_combo.currentText()
        if not selected_batches:
            return
            
        students = self.attendance_handler.fetch_students(selected_batches, selected_year)
        self.populate_table(students)

    def populate_table(self, students):
        self.table.setRowCount(len(students))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Name', 'Enrollment Number', 'Batch', 'Attendance'])
        
        table_width = self.table.viewport().width()
        self.table.setColumnWidth(0, int(table_width * 0.35))
        self.table.setColumnWidth(1, int(table_width * 0.25))
        self.table.setColumnWidth(2, int(table_width * 0.15))
        self.table.setColumnWidth(3, int(table_width * 0.2))
        
        for i, student in enumerate(students):
            name_item = QTableWidgetItem(student[0])
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            name_item.setFont(font)
            name_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            
            enrollment_item = QTableWidgetItem(student[1])
            enrollment_item.setFont(font)
            enrollment_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            
            batch_item = QTableWidgetItem(student[2])
            batch_item.setFont(font)
            batch_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            
            attendance_item = QTableWidgetItem("")
            attendance_item.setFont(font)
            attendance_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, enrollment_item)
            self.table.setItem(i, 2, batch_item)
            self.table.setItem(i, 3, attendance_item)
        self.current_students_data = students
        self.table.verticalHeader().setDefaultSectionSize(50)
        self.table.resizeRowsToContents()

    def start_attendance(self):
        if not hasattr(self, 'table') or self.table.rowCount() == 0:
            QMessageBox.warning(self, "Warning", "Please fetch student data first!")
            return
        
        self.attendance_handler.start_attendance(self.table)
        self.start_btn.setEnabled(False)

    def close_attendance(self):
        self.attendance_handler.close_attendance(self.table)
        self.start_btn.setEnabled(True)

    def on_back_button_clicked(self):
        self.start_btn.setEnabled(False)
        self.close_btn.setEnabled(False)
        self.close()

    def closeEvent(self, event):
        self.close_attendance()
        super().closeEvent(event)