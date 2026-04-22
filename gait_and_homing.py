from i2c_comm import I2CBus, Instruction
from gaits import gaits, ACTION_ZERO, GAIT_LOWER_ALL, GAIT_RAISE_ALL, ACTION_HOME_FORWARD, ACTION_HOME_BACKWARD, GAIT_COOL, ACTION_UP, ACTION_DOWN
from gaits import GAIT_SWIM_TURN_RIGHT, GAIT_SWIM_TURN_LEFT
import time

"""
Functions to handle the joystick to gait conversion and testing single legs.
"""

# global for lifting and lowering
LIFT_LOWER = False

def MoveLegs(bus: I2CBus, inst):
    """Send commands to multiple legs in bus, waits until completion"""
    
    fwd = Instruction(bus, inst)
    fwd.sendToLegs()
    fwd.checkFinished()

# determine which movement cycle to conduct based on x and y from dpad
def CompleteOneMovementCycle(gait_type, bus: I2CBus):
    
    """
    Execute a full cycle of movement as defined in a single gait from gaits.py
    """
    
    # gait type is a list of tuples (len 6) specifying instructions
    for inst in gait_type:
        MoveLegs(bus, inst)
        print("Done with current instruction")
        time.sleep(3)
       
def StopHoming(bus, curr_leg, joystick):
    """
    Returns whether or not to stop homing the motors
    """

    _, _, _, _, b_btn, x_btn = joystick.getControls()
    
    if b_btn:
        print("B button pressed, stopping")
        bus.devices[curr_leg].sendData(ACTION_DOWN)
        
        done_moving = False
                
        # wait until done
        while not done_moving:
            print("waiting for leg down")
            done_moving = bus.pollSingleLeg(bus.devices[curr_leg])
            
        bus.devices[curr_leg].sendData(ACTION_ZERO)
        
        return True

    else: 
        return False

def JoystickToGait(x: int, y:int, coolness: bool, lift_lower: bool, bus: I2CBus):
    
    # use the global variable for this
    global LIFT_LOWER
    
    if lift_lower:
        
        # change flag if pressed
        LIFT_LOWER = not LIFT_LOWER
        
        if LIFT_LOWER:
            print("lifting")
            CompleteOneMovementCycle(gaits[GAIT_RAISE_ALL], bus)
        
        else:
            print("lowering")
            CompleteOneMovementCycle(gaits[GAIT_LOWER_ALL], bus)

    elif coolness:
        print("Wiggle/Coolness fct")
        CompleteOneMovementCycle(gaits[GAIT_COOL], bus)
    
    # handle d-pad inputs
    elif x == 1:
        print("Turn right")
        CompleteOneMovementCycle(gaits[GAIT_SWIM_TURN_RIGHT], bus)
    
    elif x == -1:
        print("Turn Left")
        CompleteOneMovementCycle(gaits[GAIT_SWIM_TURN_LEFT], bus)

    elif y==1:
        print("Forward")
        # CompleteOneMovementCycle(gaits[GAIT_FORWARD], bus)

        
    elif y == -1:
        print("Back")
        # CompleteOneMovementCycle(gaits[GAIT_BACKWARD], bus)
     

def HomeMotors(bus, joystick):
    """
    Home hip motors individually via joystick. Use the B button to exit the homing loop, use Y button to move to each hip motor
    Use Y to exit the 
    Use d pad either x or y direction to move the hip forward or back
    """
    
    # get all legs
    legs = sorted(bus.devices.keys())
    
    print("Legs to home", legs)
    
    # for each leg, move until y btn is pressed again
    for i in range(len(legs)):
        
        # store current leg as var
        curr_leg = bus.devices[legs[i]]
        
        # enter loop to home
        finished = False
        
        # move leg up before homing
        curr_leg.sendData(ACTION_UP)
        
        # allow user to adjust hip motor, if y_bt pressed, move to next one
        while not finished:
            
            print(f"in homing loop for {legs[i]}")
            time.sleep(1)
            
            # exit here if needed
            stop = StopHoming(bus, legs[i], joystick)
            print("Stop: ", stop)
        
            if stop:
                return
            
            x, y, a_btn, y_btn, b_btn, x_btn = joystick.getControls()
            
            print("y_btn value: ", y_btn)
            print(x, y)
        
            # use y button to terminate homing for a single leg
            if y_btn:
                # move leg down after finshing homing
                print(f"Finished homing {legs[i]}")
                curr_leg.sendData(ACTION_DOWN)
                
                done_moving = False
                
                # wait until done
                while not done_moving:
                    done_moving = bus.pollSingleLeg(curr_leg)
                    
                # send home byte
                curr_leg.sendData(ACTION_ZERO)
                finished = True
            
            elif x == 1:
                
                print("fwd")
                curr_leg.sendData(ACTION_HOME_FORWARD)
                done_moving = False
                
                # wait until done
                while not done_moving:
                    done_moving = bus.pollSingleLeg(curr_leg)
                    
            elif y == 1:
                print("up")
                curr_leg.sendData(ACTION_UP)
                done_moving = False
                
                # wait until done
                while not done_moving:
                    done_moving = bus.pollSingleLeg(curr_leg)
                    
            elif x == -1:
                
                print("back")
                bus.devices[legs[i]].sendData(ACTION_HOME_BACKWARD)
                
                done_moving = False
                
                # wait until done
                while not done_moving:
                    done_moving = bus.pollSingleLeg(curr_leg)
                    
            elif y == -1:
                print("down")
                bus.devices[legs[i]].sendData(ACTION_DOWN)
                
                done_moving = False
                
                # wait until done
                while not done_moving:
                    done_moving = bus.pollSingleLeg(curr_leg)
        
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
        
    


    
    
    