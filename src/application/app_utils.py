import os
from PyQt5.QtGui import QFont, QFontDatabase

def add_font():
    # Add the font loading logic here
    dyslexic_font_id = QFontDatabase.addApplicationFont("C:/Users/leoco/AppData/Local/Microsoft/Windows/Fonts/OpenDyslexic-Regular.otf")
    dyslexic_font_family = QFontDatabase.applicationFontFamilies(dyslexic_font_id)[0]
    return dyslexic_font_family
