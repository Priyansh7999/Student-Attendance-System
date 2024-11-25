# Student Attendance System

## Overview

The **Student Attendance System** is a Python-based application designed to simplify the process of student attendance using face recognition technology. This project combines the power of machine learning with an interactive PyQt GUI to offer a user-friendly and efficient solution for managing attendance records.

---

## Features

### 1. **Face Recognition System**
- Built using **HOG (Histogram of Oriented Gradients)** and **ResNet** models from the `face_recognition` library.
- Achieves an **accuracy of 90%** in predicting and recognizing student faces.
- Matches recognized faces against a database to mark attendance.

---

### 2. **PyQt5 GUI with Multi-Page Navigation**
The GUI provides an intuitive interface with the following key panels:

#### **Login Page**
- Secure login with **username** and **password**.
- Access to:
  - **Data Management Panel**
  - **Student Management Panel**

#### **Data Management Panel**
- Add new users and students.
- Update existing user and student information.
- Encode faces and store them in the database for recognition.

#### **Student Management Panel**
- Input fields for:
  - **Subject Name**
  - **Date & Time**
  - **Year** and **Batch**
- Fetches the list of students (names, roll numbers, and batch) based on the selected criteria.
- Starts the **Face Recognition System** to:
  - Recognize faces in real time.
  - Mark recognized students as **Present**.
  - Automatically mark unrecognized or absent students as **Absent** upon closing attendance.
- Save attendance records for future use.

---

## How It Works

1. **Login**: 
   - Users log in through the login page to access the system.

2. **Data Management**:
   - Users can manage student and user data, including adding, updating, and encoding faces into the system.

3. **Attendance Process**:
   - In the Student Management Panel:
     1. Select the **subject**, **date**, **time**, **year**, and **batch**.
     2. Fetch the student data for the selected batch.
     3. Press **Start Attendance** to open the face recognition system.
     4. Recognized faces are marked **Present**, while others are marked **Absent**.
     5. Save the attendance data.

---

## Installation

### Prerequisites
- Python 3.7 or above
- Required Python libraries: 
  - PyQt5
  - OpenCV
  - face_recognition
  - NumPy
  - Pandas

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/Priyansh7999/Student-Attendance-System.git
   
2. Install the required libraries:
   ```bash
   pip install pyqt5 opencv-python face-recognition numpy pandas

3. Run the application::
   ```bash
   python main.py
   
### Usage
1. Login to the system.
2. Navigate to the appropriate panel:
    - Data Management Panel to manage user/student data and encode faces.
    - Student Management Panel to mark attendance.
       -Use the Face Recognition System to identify students and save attendance records.

### Future Improvements
1. Enhance the face recognition model for higher accuracy.
2. Integrate real-time database synchronization for cloud-based attendance management.
3. Add analytics and reporting features for attendance trends.

### Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.
### License
This project is licensed under the MIT License. See the LICENSE file for details.


