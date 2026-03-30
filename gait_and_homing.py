from i2c_comm import I2CBus, Instruction
import time

# instruction globals
HOME = 0x00
FORWARD = 0x01
BACK = 0x02
CW = 0x03
CCW = 0x04

# arduino-side register
REGISTER = 0x20 # modify later if needed

# phase globals
NO_MOVE = -1
LEG_UP = 0
LEG_DOWN = 1
HIP_FORWARD = 2
HIP_BACK = 3
HIP_FORWARD_GROUNDED = 4
HIP_BACK_GROUNDED = 5

# determine which movement cycle to conduct based on x and y from dpad
def completeOneMovementCycle(x: int, y:int , bus: I2CBus):
    
    if x == 1:
        print("Clockwise")
        moveCwOneCycle(bus)
    
    elif x == -1:
        print("Counterclockwise")
        moveCCwOneCycle(bus)
    
    elif y==1:
        print("Forward")
        moveForwardOneCycle(bus)
        
    elif y == -1:
        print("Back")
        moveBackOneCycle(bus)

# send homing signal for the entire hexapod
def homeHexapod(bus: I2CBus):
    # TODO
    
    home = Instruction(HOME, NO_MOVE)
    
    pass

# define coordinated movements for forward/back/cw/ccw
# hexapod wave gait makes the most sense (one cycle as all 6 legs move forward)
def moveForwardOneCycle(bus: I2CBus):
    
    # define instruction structs to send
    
    # for legs that move up
    up = Instruction(FORWARD, LEG_UP)
    over = Instruction(FORWARD, HIP_FORWARD)
    down = Instruction(FORWARD, LEG_DOWN)
    
    # for grounded legs attached at the hip
    ground_adjust = Instruction(FORWARD, HIP_FORWARD_GROUNDED)
    
    # TODO need to figure out how to do the ground adjustment
    
    # first 3 legs raise and move
    bus.devices["leg1"].sendData(REGISTER, up)
    bus.devices["leg1"].sendData(REGISTER, over)
    bus.devices["leg1"].sendData(REGISTER, down)
    
    # do we need this?
    time.sleep(0.02)
    bus.devices["leg2"].sendData(REGISTER, up)
    bus.devices["leg2"].sendData(REGISTER, over)
    bus.devices["leg2"].sendData(REGISTER, down)
    
    time.sleep(0.02)
    bus.devices["leg3"].sendData(REGISTER, up)
    bus.devices["leg3"].sendData(REGISTER, over)
    bus.devices["leg3"].sendData(REGISTER, down)
    
    
    # second 3 legs raise and move
    bus.devices["leg4"].sendData(REGISTER, up)
    bus.devices["leg4"].sendData(REGISTER, over)
    bus.devices["leg4"].sendData(REGISTER, down)
    
    # do we need this?
    time.sleep(0.02)
    bus.devices["leg5"].sendData(REGISTER, up)
    bus.devices["leg5"].sendData(REGISTER, over)
    bus.devices["leg5"].sendData(REGISTER, down)
    
    time.sleep(0.02)
    bus.devices["leg6"].sendData(REGISTER, up)
    bus.devices["leg6"].sendData(REGISTER, over)
    bus.devices["leg6"].sendData(REGISTER, down)
    

def moveBackOneCycle(bus: I2CBus):
    pass

def moveCwOneCycle(bus: I2CBus):
    pass

def moveCCwOneCycle(bus: I2CBus):
    pass


def testI2CJoystick(x: int, y:int , bus: I2CBus):
    
    # fwd - 0x01, back 0x02
    test_fwd = Instruction(FORWARD, LEG_UP)
    test_back = Instruction(BACK, LEG_DOWN)
    
    if x == 1:
        print("Clockwise")
        for _, device in bus.devices:
            device.sendData(test_fwd)
    
    elif x == -1:
        print("Counterclockwise")
        for device in bus.devices:
            device.sendData(test_back)
    
    elif y==1:
        print("Forward")
        for device in bus.devices:
            device.sendData(test_fwd)
        
    elif y == -1:
        print("Back")
        for device in bus.devices:
            device.sendData(test_back)

# homing a single leg
def homeSingleLeg():
    home_instr = Instruction(0x00, -1)
    
    
    