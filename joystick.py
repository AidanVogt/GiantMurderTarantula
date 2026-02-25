import pygame
import time

# weird - for the raspberry pi connection, use axes 3 and 4 for
# the right thumb joystick. 2 is the left trigger

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


#j = startJoystick()
#monitorJoystick(j)
