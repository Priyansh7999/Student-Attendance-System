# main.py
from PyQt5.QtWidgets import QApplication
import sys
from frontend.login import LoginWindow

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.setFixedSize(1500, 1500)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  