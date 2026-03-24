from i2c_comm import Instruction

# globals for movement
HOME = 0x00
MOVE = 0x01
STOP = 0x02

FORWARD = 0
BACK = 1
CW = 2
CCW = 3

def signalsToGait(x, y):
    
    if x == 1:
        moveCwOneCycle()
    
    elif x == -1:
        moveCCwOneCycle()
    
    elif y==1:
        moveForwardOneCycle()
        
    elif y == -1:
        moveBackOneCycle()


# define coordinated movements for forward/back/cw/ccw
def moveForwardOneCycle():
    pass

def moveBackOneCycle():
    pass

def moveCwOneCycle():
    pass

def moveCCwOneCycle():
    pass

def homeSingleLeg():
    home_instr = Instruction(0x00, -1)
    
    
    pass