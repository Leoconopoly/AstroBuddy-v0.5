import requests
import json
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MediaViewer(QLabel):
    """
    A custom QLabel widget for displaying images fetched from external sources or local files.
    """

    def load_api_key(self, filepath):
        """
        Load API key from a JSON configuration file.

        Args:
            filepath (str): Path to the JSON configuration file.

        Returns:
            str: API key if found, otherwise None.
        """
        with open(filepath, 'r') as file:
            config = json.load(file)
            return config.get('api_key')

    def __init__(self):
        """
        Initialize the MediaViewer widget.
        """
        super().__init__()
        self.default_image_path = "project_media/astrobuddyfullavatar.png"  
        self.set_default_image()

    def set_default_image(self):
        """
        Set the default image for the MediaViewer.
        """
        pixmap = QPixmap(self.default_image_path)
        scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)

    def display_nasa_apod(self):
        """
        Display the Astronomy Picture of the Day (APOD) from NASA's API.
        """
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
        """
        Load an image from a URL and display it.

        Args:
            url (str): URL of the image.
        """
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
        else:
            print("Failed to load image from URL.")

    def display_image_from_url(self, url):
        """
        Display an image from a URL or a local file path.

        Args:
            url (str): URL or local file path of the image.
        """
        if url and url.startswith(('http://', 'https://')):  
            self.load_image(url)  
        elif url:  
            pixmap = QPixmap(url)  
            scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
        else:  
            self.set_default_image()

