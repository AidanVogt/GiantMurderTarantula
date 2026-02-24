import pygame
import time

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
    
        # read joystick axes (typically 0=left X, 1=left Y, 2=right X, 3=right Y)
        left_x = j.get_axis(0)
        left_y = j.get_axis(1)
        right_x = j.get_axis(2)
        right_y = j.get_axis(3)
        
        print(f"\rLeft: ({left_x:6.2f}, {left_y:6.2f})  |  Right: ({right_x:6.2f}, {right_y:6.2f})", end="")
        
        time.sleep(0.01)

   

