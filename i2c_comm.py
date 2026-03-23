import smbus2

# Sending instructions from the pi to the arduinos
# Gait planning done at highest level
# Get instruction from d-pad -> translate into a movement class (i.e. forward, backwards)
    # map cycles to actions (have an action CLASS)
# blocker to read input - want to wait until we have processed the full movement before
# getting next input

class InoBus:
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        
    def addArduinoToBus(self):
        pass
    
    def pollArduinos(self):
        # poll all arduinos on the bus to check their status
        # arduinos can send a true/false determining whether or not they are complete with one cycle of movement
        pass
    
class GMTIno:
    def __init__(self, address):
        
        # init unique address for Arduinos
        self.address = address
        
    def readI2C(self):
        # bus.write_i2c_block_data(address, 0, [1, 2, 3])
        pass