from gait_and_homing import completeOneMovementCycle, testI2CJoystick
from i2c_comm import I2CBus, GMTIno
from joystick import GMTJoystick
import time

# init bus and controller
print("Initializing I2C Bus and controller")
bus = I2CBus()
j = GMTJoystick()

# initialize legs
leg1 = GMTIno("leg1", 0x10)
# leg2 = GMTIno("leg2", 0x11)
# leg3 = GMTIno("leg3", 0x12)

# leg4 = GMTIno("leg4", 0x13)
# leg5 = GMTIno("leg5", 0x14)
# leg6 = GMTIno("leg6", 0x15)

# add legs to bus
bus.addDevices(leg1)
# bus.addDevices(leg1, leg2, leg3, leg4, leg5, leg6)
# print([d.name for d in bus.devices])
print([d for d in bus.devices.keys()])
print(bus.devices)
print(leg1.bus)

# set motors as idle
cycle_complete = True

# main loop for converting joystick to arduino-side commands
def joystickLoop():
    
    while True:
        
        # get raw controller input
        controls = j.getControls()
        print(controls)

        if controls is not None:
            
            # get controls
            x, y = controls
            
            # convert x and y signal to gait
            testI2CJoystick(x, y, bus)

        time.sleep(0.05)
        
joystickLoop()

