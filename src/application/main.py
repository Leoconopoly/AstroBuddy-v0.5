import sys
from PyQt5.QtWidgets import QApplication
from application_logic import ChatApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chatApp = ChatApplication()
    chatApp.show()
    exit_code = app.exec_()
    sys.exit(exit_code)
