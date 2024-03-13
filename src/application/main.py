import sys
from PyQt5.QtWidgets import QApplication
from application_logic import ChatApplication

if __name__ == "__main__":
    # Create a QApplication instance
    app = QApplication(sys.argv)
    
    # Create an instance of the ChatApplication widget
    chatApp = ChatApplication()
    
    # Show the ChatApplication widget
    chatApp.show()
    
    # Execute the application event loop and retrieve the exit code
    exit_code = app.exec_()
    
    # Exit the application with the retrieved exit code
    sys.exit(exit_code)