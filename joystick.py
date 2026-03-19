import pygame
import time

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
            dpad = self.j.get_hat(0)
            x = dpad[0]   # -1 = left, 0 = neutral, 1 = right
            y = dpad[1]   # -1 = down, 0 = neutral, 1 = up
            print(x, y)

        # disconnect if any errors
        except Exception:
            self.j = None
            print("ERRRRROR")
        
        
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
        dpad = j.get_hat(0)
        x = dpad[0]   # -1 = left, 0 = neutral, 1 = right
        y = dpad[1]   # -1 = down, 0 = neutral, 1 = up
        print(x, y)

        time.sleep(0.01)
        
        
        
j = startJoystick()
monitorJoystick(j)


