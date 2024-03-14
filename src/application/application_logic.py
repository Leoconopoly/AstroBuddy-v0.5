import sys
import os

# Add the parent directory of 'src' to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from chat_logic.chat import get_response, bot_name
from utils.log_manager import logger
from application.app_utils import add_font
from application.ui_components import MediaViewer  

# Log that the AstroBuddy Chat Application has started
logger.info("AstroBuddy Chat Application Started")

class ChatApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.insertAstroBuddyGreeting()

    def initUI(self):
        # Set window title
        self.setWindowTitle("AstroBuddy - Chat (v0.5)")
        
        # Load the Open Dyslexic font
        dyslexic_font_family = add_font()

        mainHLayout = QHBoxLayout()

        # Initialize MediaViewer widget
        self.media_viewer = MediaViewer()
        self.media_viewer.display_nasa_apod()

        mediaViewerLayout = QVBoxLayout()
        mediaViewerLayout.addWidget(self.media_viewer)

        mainHLayout.addLayout(mediaViewerLayout)

        chatLayout = QVBoxLayout()
        
        # Add the project logo to the header label
        head_label = QLabel("AstroBuddy Chat")
        head_label.setFont(QFont(dyslexic_font_family, 32))  
        head_label.setStyleSheet("color: #f7cd3f;")  
        head_label.setAlignment(Qt.AlignCenter)

        # Load the logo
        logo_pixmap = QPixmap("project_media/astrobuddylogo.png")
        scaled_logo_pixmap = logo_pixmap.scaledToHeight(100)  
        logo_label = QLabel()
        logo_label.setPixmap(scaled_logo_pixmap)
        logo_label.setAlignment(Qt.AlignRight)

        # Create a horizontal layout for the header label and logo
        header_layout = QHBoxLayout()
        header_layout.addWidget(head_label)
        header_layout.addWidget(logo_label)

        # Set alignment of the header layout to top center
        header_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Add the header widget to the main layout
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("background-color: #93c2db; color: #333333;")

        chatLayout.addWidget(header_widget)

        self.chat_window = QTextEdit()
        self.chat_window.setReadOnly(True)
        self.chat_window.setFont(QFont(dyslexic_font_family, 24))  
        self.chat_window.setStyleSheet("background-color: #c7e0f4; color: #333333; border-radius: 10px; font-size: 24px;") 
        chatLayout.addWidget(self.chat_window, 1)

        bottomLayout = QHBoxLayout()
        self.msg_entry = QLineEdit()
        self.msg_entry.setFont(QFont(dyslexic_font_family, 24)) 
        self.msg_entry.setStyleSheet("background-color: #93c2db; color: #333333; border-radius: 5px; border: 2px solid #7289DA; font-size: 24px;")
        self.msg_entry.returnPressed.connect(self.onEnterPressed)
        bottomLayout.addWidget(self.msg_entry, 8)

        send_button = QPushButton("Send")
        send_button.setFont(QFont(dyslexic_font_family, 24)) 
        send_button.setStyleSheet("background-color: #f7cd3f; color: #333333; border-radius: 5px; font-size: 24px;") 
        send_button.clicked.connect(self.onEnterPressed)
        bottomLayout.addWidget(send_button, 2) 

        chatLayout.addLayout(bottomLayout)

        mainHLayout.addLayout(chatLayout, 3)

        # Set the background color for the main widget
        self.setStyleSheet("background-color: #c7e0f4; color: #333333;")  

        main_layout = QVBoxLayout()
        main_layout.addLayout(mainHLayout)
        self.setLayout(main_layout)


    def insertAstroBuddyGreeting(self):
        # Insert a greeting message from AstroBuddy when the application starts
        greeting_message = ("Hi there, space explorer! 🚀 I'm AstroBuddy, your guide to the incredible universe. "
                            "Are you ready to embark on an amazing adventure through the stars and planets?")
        self.insertMessage(greeting_message, bot_name)

    def onEnterPressed(self):
        # Handle the user pressing Enter to send a message
        msg = self.msg_entry.text()
        if msg:
            # Insert user's message into the chat window
            self.insertMessage(msg, "User")
            # Get response from AstroBuddy and display it in the chat window
            response, image_url = get_response(msg)  
            self.insertMessage(response, bot_name)
            # Display any image related to the response in the media viewer
            self.media_viewer.display_image_from_url(image_url)  
            # Log the user's message and AstroBuddy's response
            logger.info(f"User: {msg} | {bot_name}: {response}")

    def insertMessage(self, msg, sender):
        # Insert a message into the chat window
        self.msg_entry.clear()
        if sender == bot_name:
            formatted_msg = f"<b>{bot_name}:</b> {msg}"
        else:
            formatted_msg = f"<b>User:</b> {msg}"

        self.chat_window.append(formatted_msg)
