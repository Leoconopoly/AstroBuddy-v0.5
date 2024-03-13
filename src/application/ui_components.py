import requests
import json
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MediaViewer(QLabel):

    def load_api_key(self, filepath):
        with open(filepath, 'r') as file:
            config = json.load(file)
            return config.get('api_key')

    def __init__(self):
        super().__init__()
        self.default_image_path = "project_media/astrobuddyfullavatar.png"  
        self.set_default_image()

    def set_default_image(self):
        pixmap = QPixmap(self.default_image_path)
        # Scale pixmap to a new size while keeping the aspect ratio
        scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)

    def display_nasa_apod(self):
        apod_url = "https://api.nasa.gov/planetary/apod"
        api_key = self.load_api_key("config.json") 
        params = {"api_key": api_key}
        response = requests.get(apod_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "url" in data:
                image_url = data["url"]
                self.load_image(image_url)
            else:
                print("No image URL found in response.")
        else:
            print("Failed to fetch APOD image.")

    def load_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            # Scale pixmap to a new size while keeping the aspect ratio
            scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
        else:
            print("Failed to load image from URL.")

    def display_image_from_url(self, url):
        if url and url.startswith(('http://', 'https://')):  # If a valid URL is provided
            self.load_image(url)  # Load image from URL
        elif url:  # If a local file path is provided
            pixmap = QPixmap(url)  # Load image from file system
            scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
        else:  # Display default image if no URL or file path is provided
            self.set_default_image()




