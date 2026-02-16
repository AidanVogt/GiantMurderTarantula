import serial
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QFrame
from qtwidgets import AnimatedToggle
from PyQt5.QtGui import QIntValidator
import sys


# GUI

# GLOBALS
BAUD_RATE = 9600
TIMEOUT = 0.05

# arduino = serial.Serial(port="/dev/cu.usbmodem2101", baudrate=BAUD_RATE, timeout=TIMEOUT)

# design the main window
class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # global gui things
        self.setMinimumSize(QSize(800, 800))
        self.setWindowTitle("Software 1")
        global_title = QLabel("Joystick")
        global_title.setStyleSheet("font-size: 30px;")
        
        
        # set central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # joystick
        title = QLabel("Joystick")
        self.sensor_value = QLabel("No Reading Detected")
        
        main_layout.addWidget(global_title)
        main_layout.addWidget(title)
        main_layout.addWidget(self.sensor_value)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        


# run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainInterface()
    window.show()

    app.exec()


        
        
        
        
        
        
        