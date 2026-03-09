import serial
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel
import sys


# GUI

# GLOBALS
BAUD_RATE = 9600
TIMEOUT = 0.05
PORT = "/dev/cu.usbmodem11301"

arduino = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)

# design the main window
class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # global gui things
        self.setMinimumSize(QSize(800, 800))
        self.setWindowTitle("System Demo 1: Arduino Joystick")
        global_title = QLabel("Joystick Demo - Giant Murder Tarantula")
        global_title.setStyleSheet("font-size: 40px;")
        
        
        # set central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # joystick
        title = QLabel("Normalized Joystick Values (-1 to 1)")
        title.setStyleSheet("font-size: 30px;")
        self.x_val = QLabel("empty")
        self.y_val = QLabel("empty")
        self.switch_tog = QLabel("idk")
        
        xlbl = QLabel("X-Value")
        xlbl.setStyleSheet("font-size: 18px;")
        ylbl = QLabel("Y-Value")
        ylbl.setStyleSheet("font-size: 18px;")
        
        main_layout.addWidget(global_title)
        main_layout.addWidget(title)
        main_layout.addWidget(xlbl)
        main_layout.addWidget(self.x_val)
        main_layout.addWidget(ylbl)
        main_layout.addWidget(self.y_val)
        main_layout.addWidget(self.switch_tog)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.serial_timer = QTimer(self)
        self.serial_timer.setInterval(50)
        self.serial_timer.timeout.connect(self.PollSerial)
        self.serial_timer.start()
        
    def PollSerial(self):
        
        # get vals
        try:
            line = arduino.readline().decode("utf-8", errors="ignore").strip()
            
        except serial.SerialException:
            return

        if not line:
            return

        # arduino output
        parts = [p.strip() for p in line.split(",")]

        # parse the string
        switch, norm_x, norm_y = parts[0], parts[1], parts[2]
        print(switch, norm_x, norm_y)
        
        # update sensor values
        self.x_val.setText(norm_x)
        self.y_val.setText(norm_y)
        
        if switch == "0":
            self.switch_tog.setText("ON")
            
        else:
            self.switch_tog.setText("OFF")


# run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainInterface()
    window.show()

    app.exec()


        
        
        
        
        
        
        