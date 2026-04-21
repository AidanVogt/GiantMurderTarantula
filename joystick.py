import pygame
import time

"""
Joystick-specific functions for initialization and monitoring. Uses the pygame class to get specific inputs.
NOTE - switched to the dpad for controls, easier to implement
"""

class GMTJoystick:
    def __init__(self):
        
        pygame.init()
        pygame.joystick.init()
        
        # check for connection to xbox controller (sets self.j as joystick)
        self.j = self.tryConnection()
        self.j.init()
        
        print(f"Controller: {self.j.get_name()}")
        self.connected = True
        
    def tryConnection(self):
        
        """ Continually try reconnecting until joystick is added """
        
        print("Finding controller")
        
        while True:
            
            print("no controller")
            
            for event in pygame.event.get():
                
                # check whether a joystick was added
                if event.type == pygame.JOYDEVICEADDED:
                    
                    # store it as the joystick in the object if connected
                    joy = pygame.joystick.Joystick(event.device_index)

                    print(f"Controller found: {joy.get_name()}")
                    
                    return joy

            time.sleep(1)
                
    
    def getControls(self):
        # returns controls
            
        if not self.connected:
            return None

        try:
            pygame.event.pump()

            dpad = self.j.get_hat(0)
            a_btn = bool(self.j.get_button(0))
            y_btn = bool(self.j.get_button(3))
            b_btn = bool(self.j.get_button(1))
            
            x = dpad[0]   # -1 = left, 0 = neutral, 1 = right
            y = dpad[1]   # -1 = down, 0 = neutral, 1 = up
            
            return (x, y, a_btn, y_btn, b_btn)

        except Exception as e:
            self.connected = False
            self.j = None
            print(f"Err: {e}")
            return None
            
    
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
    
    while True:
        pygame.event.pump()
    
        # read dpad
        dpad = j.get_hat(0)
        x = dpad[0]   # -1 = left, 0 = neutral, 1 = right
        y = dpad[1]   # -1 = down, 0 = neutral, 1 = up
        print(x, y)

        time.sleep(0.01)
        
        
# test joystick readings        
# j = startJoystick()
# monitorJoystick(j)


