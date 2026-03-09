import pygame
import time
import struct 

# weird - for the raspberry pi connection, use axes 3 and 4 for
# the right thumb joystick. 2 is the left trigger

class GMTJoystick:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        if pygame.joystick.get_count() == 0:
            print("no contrller")
            exit(1)
            
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print(f"Controller: {self.j.get_name()}")
        
        # globals
        self.dead_zone = 0.05
        
    def sendToSerial(self, arduino_port):
        # start processing controls
        pygame.event.pump()

        try:
            # get axes (right joystick only)
            x = self.j.get_axis(3)
            y = -self.j.get_axis(4)
            print(x,y)

            # dead threshold
            x = x if abs(x) > self.dead_zone else 0.0
            y = y if abs(y) > self.dead_zone else 0.0
            
            data = struct.pack('cff', b"c", x, y)
            arduino_port.write(data)
            print(f"Sent: x={x:.2f}, y={y:.2f}")

        # disconnect if any errors
        except Exception:
            self.j = None
            print("Ctrl disconnected")
        
        
######################################################
# for testing
def startJoystick():
    
    # init a joystick 
    pygame.init()
    pygame.joystick.init()


    # check
    if pygame.joystick.get_count() == 0:
        print("no controller")
        exit(1)

    # start
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller: {joystick.get_name()}")
    
    return joystick

def monitorJoystick(j):
    # for testing...
    
    while True:
        pygame.event.pump()
    
        # read joystick axes
        left_x = j.get_axis(0)
        left_y = j.get_axis(1)
        right_x = j.get_axis(3)
        right_y = j.get_axis(4)
        
        print(f"\rLeft: ({left_x:6.2f}, {left_y:6.2f})  |  Right: ({right_x:6.2f}, {right_y:6.2f})", end="")
        
        time.sleep(0.01)


