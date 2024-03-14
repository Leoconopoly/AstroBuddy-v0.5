import sys
import os
import subprocess

# Function to check for database existence and create if not found
def check_and_create_database():
    db_path = 'db/astrobuddy_v0.5.db'
    if not os.path.exists(db_path):
        print("Database not found, creating...")
        # Construct the absolute path to intents_db_main.py within the utils directory
        script_path = os.path.join(os.path.dirname(__file__), 'utils', 'intents_db_main.py')
        subprocess.run(['python', script_path], check=True)

# Function to check for trained model file existence and train if not found
def check_and_train_model():
    model_file_path = 'data.pth'
    if not os.path.exists(model_file_path):
        print("Model file not found, training model...")
        # Construct the absolute path to train.py within the model_logic directory
        script_path = os.path.join(os.path.dirname(__file__), 'model_logic', 'train.py')
        subprocess.run(['python', script_path], check=True)

if __name__ == "__main__":
    # Check and potentially create the database
    check_and_create_database()

    # Check and potentially train the model
    check_and_train_model()

    # Delayed import of QApplication and ChatApplication
    from PyQt5.QtWidgets import QApplication
    # Import here to ensure it is after the database check and creation
    from application.application_logic import ChatApplication

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

