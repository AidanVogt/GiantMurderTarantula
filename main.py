from gait_and_homing import JoystickToGait, TestOneLeg
from i2c_comm import I2CBus, GMTIno, testI2C
from joystick import GMTJoystick
import time

"""
Main loop for hexapod control. Continuously monitor the joystick for input and use higher level functions to convert the joystick input to gait commands
"""

# init bus and controller
print("Initializing I2C Bus and controller")
bus = I2CBus()
j = GMTJoystick()

# initialize legs
leg1 = GMTIno("leg1", 0x10)
leg2 = GMTIno("leg2", 0x11)
leg3 = GMTIno("leg3", 0x12)

leg4 = GMTIno("leg4", 0x13)
leg5 = GMTIno("leg5", 0x14)
leg6 = GMTIno("leg6", 0x15)

# add legs to bus
# bus.addDevices(leg1)
bus.addDevices(leg2)
# bus.addDevices(leg1, leg2, leg3, leg4, leg5, leg6)
print([d for d in bus.devices.keys()])
print([hex(d.address) for d in bus.devices.values()])
print(leg1.bus)

# main loop for converting joystick to arduino-side commands
def joystickLoop():
    
    while True:
        
        # get raw controller input
        controls = j.getControls()
        print(controls)

        if controls is not None:
            
            # get controls (y btn for coolness factor)
            x, y, a_btn, y_btn = controls
            
            print(x, y, a_btn, y_btn)
            
            # convert x and y signal to move single leg
            # TestOneLeg(x, y, bus)
            
            # test i2c comm
            testI2C(bus)
            
            # # converts user input to gait
            # JoystickToGait(x, y, a_btn, y_btn, bus)

        time.sleep(2)
    
# constantly run joystick loop    
joystickLoop()

