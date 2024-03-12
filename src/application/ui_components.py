import requests
import json
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

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
        self.setPixmap(pixmap)

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
            self.setPixmap(pixmap)
        else:
            print("Failed to load image from URL.")

