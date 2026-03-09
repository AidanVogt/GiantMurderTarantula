import serial
from joystick import GMTJoystick
import pygame

# GLOBALS
BAUD_RATE = 9600
TIMEOUT = 0.05
PORT = "/dev/ttyACM0"

arduino1 = serial.Serial(port=PORT, baudrate=BAUD_RATE, timeout=TIMEOUT)
# arduino2 later

# new instance of joystick
js = GMTJoystick()

try:
    while True:
        js.sendToSerial(arduino1)

except KeyboardInterrupt:
    print("Stopped")
    arduino1.close()
    pygame.quit()


