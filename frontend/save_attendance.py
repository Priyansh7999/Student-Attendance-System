import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from datetime import datetime

class AttendanceSaver:
    def __init__(self):
        self.default_filename = f"Attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    def save_attendance_to_excel(self, subject, date, time, year, batches, table):
        try:
            # Ask user for save location
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Save Attendance",
                self.default_filename,
                "Excel Files (*.xlsx)"
            )

            if not file_path:  # If user cancels
                return False

            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'

            # Create a dictionary with class details
            class_details = {
                'Subject': [subject],
                'Date': [date],
                'Time': [time],
                'Year': [year],
                'Batches': [', '.join(batches)]
            }

            # Create a DataFrame for class details
            df_details = pd.DataFrame(class_details)

            # Create a DataFrame for attendance data
            data = []
            for row in range(table.rowCount()):
                name = table.item(row, 0).text()
                enrollment = table.item(row, 1).text()
                batch = table.item(row, 2).text()
                attendance = table.item(row, 3).text()
                data.append([name, enrollment, batch, attendance])

            df_attendance = pd.DataFrame(data, columns=['Name', 'Enrollment Number', 'Batch', 'Attendance'])

            # Calculate summary
            total_students = len(df_attendance)
            present_students = df_attendance['Attendance'].value_counts().get('PRESENT', 0)
            absent_students = total_students - present_students
            attendance_percentage = (present_students / total_students * 100) if total_students > 0 else 0

            summary_data = {
                'Total Students': [total_students],
                'Present': [present_students],
                'Absent': [absent_students],
                'Attendance %': [f'{attendance_percentage:.2f}%']
            }
            df_summary = pd.DataFrame(summary_data)

            # Create a Pandas Excel writer using XlsxWriter as the engine
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df_details.to_excel(writer, sheet_name='Attendance Report', index=False, startrow=0, startcol=0)
                df_attendance.to_excel(writer, sheet_name='Attendance Report', index=False, startrow=7, startcol=0)
                df_summary.to_excel(writer, sheet_name='Attendance Report', index=False, startrow=df_attendance.shape[0] + 10, startcol=0)

                # Get the xlsxwriter workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets['Attendance Report']

                # Add some cell formats
                header_format = workbook.add_format({'bold': True, 'bg_color': '#366092', 'font_color': 'white'})
                cell_format = workbook.add_format({'border': 1})

                # Apply formats to the header and cells
                for col_num, value in enumerate(df_attendance.columns.values):
                    worksheet.write(7, col_num, value, header_format)

                # Set column widths
                for i, col in enumerate(df_attendance.columns):
                    max_len = max(df_attendance[col].astype(str).map(len).max(), len(col)) + 1
                    worksheet.set_column(i, i, max_len)

            QMessageBox.information(
                None,
                "Success",
                f"Attendance has been saved successfully to:\n{file_path}"
            )
            return True

        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"An error occurred while saving the attendance:\n{str(e)}"
            )
            return False