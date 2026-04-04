from i2c_comm import I2CBus, Instruction
import time

# simpler method
# Decompose gait into instructions, modify code to send a single byte

# determine which movement cycle to conduct based on x and y from dpad
def completeOneMovementCycle(x: int, y:int , bus: I2CBus):
    
    if x == 1:
        print("Clockwise")

    
    elif x == -1:
        print("Counterclockwise")

    
    elif y==1:
        print("Forward")

        
    elif y == -1:
        print("Back")


def moveLeg(inst, bus: I2CBus):
    fwd = Instruction(bus, inst)
    fwd.sendToLegs()
    fwd.checkFinished()


def testI2CJoystick(x: int, y:int , bus: I2CBus):
    
    if x == 1:
        print("Clockwise")
        instr = 0 # TODO
        moveLeg(instr, bus)
    
    elif x == -1:
        print("Counterclockwise")
        for device in bus.devices.values():
            instr = 0 # TODO
            moveLeg(instr, bus)
    
    elif y==1:
        print("Forward")
        for device in bus.devices.values():
            instr = 0 # TODO
            moveLeg(instr, bus)
        
    elif y == -1:
        print("Back")
        for device in bus.devices.values():
            instr = 0 # TODO
            moveLeg(instr, bus)


    
    
    