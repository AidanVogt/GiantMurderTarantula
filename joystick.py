import pygame
import time

# weird - for the raspberry pi connection, use axes 3 and 4 for
# the right thumb joystick. 2 is the left trigger
# NOTE - switched to the dpad for controls, easier to implement

class GMTJoystick:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        if pygame.joystick.get_count() == 0:
            print("no controller")
            exit(1)
            
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        print(f"Controller: {self.j.get_name()}")
        self.connected = True
        
    def getControls(self):
        # returns controls as [x, y, B]
            
        if not self.connected:
            return None

        try:
            pygame.event.pump()

            dpad = self.j.get_hat(0)
            x = dpad[0]   # -1 = left, 0 = neutral, 1 = right
            y = dpad[1]   # -1 = down, 0 = neutral, 1 = up
            
            # buttons
            for i in range(self.j.get_numbuttons()):
                if self.j.get_button(i):
                    print(f"Button pressed: {i}")
            
            return (x, y, -1)

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


