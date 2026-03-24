from i2c_comm import I2CBus, GMTIno
from joystick import GMTJoystick
import threading
import time

# init bus and controller
bus = I2CBus()
j = GMTJoystick()

# initialize legs
leg1 = GMTIno(0x10)
leg2 = GMTIno(0x11)
leg3 = GMTIno(0x12)

leg4 = GMTIno(0x13)
leg5 = GMTIno(0x14)
leg6 = GMTIno(0x15)

# add legs to bus
bus.addDevices(leg1, leg2, leg3, leg4, leg5, leg6)

# set motors as idle
motors_complete = threading.Event()
motors_complete.set()

# main loop for converting joystick to arduino-side commands
def joystickLoop():
    
    while True:
        
        # get raw controller input
        controls = j.getControls()
        print(controls)

        if controls is not None:
            x, y = controls

            # convert D-pad input to movement mappings
            # movement = processControls(x, y) TODO WRITE THIS FUNC

            # send relevant commands to the legs
            # sendToLegs(movement) TODO WRITE THIS FUNC
            
        time.sleep(0.05)

joystickLoop()

# def pollLoop():
    
#     while True:
#         # pollArduinos returns True when all motors confirm complete
#         if bus.pollArduinos():    
#             motors_complete.set() # release 
            
#         time.sleep(0.05)


# # concurrent polling and joystick processing
# t1 = threading.Thread(target=joystickLoop, daemon=True)
# t2 = threading.Thread(target=pollLoop, daemon=True)
# t1.start()
# t2.start()