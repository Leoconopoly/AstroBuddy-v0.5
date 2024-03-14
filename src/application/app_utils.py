# Importing necessary libraries
from PyQt5.QtGui import QFontDatabase

# Function to add a custom font
def add_font():
    # Add the font loading logic here
    # Path to the custom font file
    font_path = "project_media/OpenDyslexic-Regular.otf"
    # Add the font to the application font database and get its ID
    dyslexic_font_id = QFontDatabase.addApplicationFont(font_path)
    # Get the font family name from the font ID
    dyslexic_font_family = QFontDatabase.applicationFontFamilies(dyslexic_font_id)[0]
    # Return the font family name
    return dyslexic_font_family

