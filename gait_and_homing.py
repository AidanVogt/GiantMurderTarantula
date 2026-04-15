from i2c_comm import I2CBus, Instruction
from gaits import gaits, GAIT_FORWARD, GAIT_BACKWARD, GAIT_TURN_LEFT, GAIT_TURN_RIGHT, ACTION_FORWARD, ACTION_BACKWARD, GAIT_COOL
import time

"""
Functions to handle the joystick to gait conversion and testing single legs.
"""

# simpler method
# Decompose gait into instructions, modify code to send a single byte

def MoveLegs(bus: I2CBus, inst):
    """Send commands to multiple legs in bus, waits until completion"""
    
    fwd = Instruction(bus, inst)
    fwd.sendToLegs()
    fwd.checkFinished()

# determine which movement cycle to conduct based on x and y from dpad
def CompleteOneMovementCycle(gait_type, bus: I2CBus):
    
    # gait type is a list of tuples (len 6) specifying instructions
    for inst in gait_type:
        MoveLegs(bus, inst)
        

def JoystickToGait(x: int, y:int, coolness: bool, bus: I2CBus):

    if coolness:
        print("Wiggle/Coolness fct")
        CompleteOneMovementCycle(gaits[GAIT_COOL], bus)
    
    # handle d-pad inputs
    elif x == 1:
        print("Turn right")
        # CompleteOneMovementCycle(gaits[GAIT_TURN_RIGHT], bus)
    
    elif x == -1:
        print("Turn Left")
        # CompleteOneMovementCycle(gaits[GAIT_TURN_LEFT], bus)

    elif y==1:
        print("Forward")
        CompleteOneMovementCycle(gaits[GAIT_FORWARD], bus)

        
    elif y == -1:
        print("Back")
        CompleteOneMovementCycle(gaits[GAIT_BACKWARD], bus)
     

def HomeMotors(bus, joystick):
    
    legs = sorted(bus.devices.keys())
    
    # for each leg, move until y btn is pressed again
    for i in range(len(legs)):
        
        # enter loop to home
        finished = False
        
        # allow user to adjust hip motor, if y_bt pressed, move to next one
        while not finished:
            x, y, a_btn, y_btn = joystick.getControls()
            
            if y_btn:
                print(f"Finished homing {legs[i]}")
                finished = True
                
            elif y == 1:
                bus.devices[legs[i]].sendData(ACTION_FORWARD)
                
            elif y == -1:
                bus.devices[legs[i]].sendData(ACTION_BACKWARD)
    
       
        
def TestOneLeg(x: int, y: int, bus: I2CBus):
    
    if y == 1:
        print("Move up")
        inst = (3, 0, 0, 0, 0, 0)
        MoveLegs(bus, inst)
    
    
    elif y == -1:
        print("Move down")
        inst = (4, 0, 0, 0, 0, 0)
        MoveLegs(bus, inst)
        
    elif x == 1:
        print("Move fwd")
        inst = (1, 0, 0, 0, 0 ,0)
        MoveLegs(bus, inst)
    
    elif x == -1:
        print("Move back")
        inst = (2, 0, 0, 0, 0 ,0)
        MoveLegs(bus, inst)
        
    


    
    
    