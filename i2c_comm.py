import smbus2

# Sending instructions from the pi to the arduinos
# Gait planning done at highest level
# Get instruction from d-pad -> translate into a movement class (i.e. forward, backwards)
    # map cycles to actions (have an action CLASS)
    
register = 0x09

class Instruction:
    def __init__(self, instr_type, phase):
        # instr types: 0x00 = home, 0x01 = fwd, 0x02 = back, 0x03 = cw, 0x04 - ccw
        self.instr_type = instr_type
        
        # phase: -1 = No movement, 0 = leg up, 1 = leg down, 2 = hip forward, 3 = hip back, 4 = groudned hip forward, 5 = grounded hip back
        self.phase = phase


class I2CBus:
    def __init__(self):
        # i2c 1 port on pi
        self.bus = smbus2.SMBus(1)
        self.devices = {}
        
    def addDevices(self, *devices):
        # add inos to devices list
        for device in devices:
            if isinstance(device, GMTIno):
                device.bus = self
                self.devices[device.name] = device

    def pollArduinos(self):
        # poll all arduinos on the bus to check their status
        # arduinos can send a true/false determining whether or not they are complete with one cycle of movement
        # ino sends either 0 or 1 (0 meaning still moving)
        
        finished_movement = True
        
        # TODO update iter
        for device in self.devices:

            try:
                response = self.bus.read_byte(device.address)  # read 1 byte from arduino
                if response != 1:
                    finished_movement = False
                    return finished_movement
            
            # check for issues with connectivity
            except OSError as e:
                print(f"Failed to poll device {hex(device.address)}: {e}")
                finished_movement = False
                break
    
        return finished_movement
    
class GMTIno:
    def __init__(self, name, address):
        # init unique address for Arduinos
        self.address = address
        self.name = name
        self.bus = None
        
    def sendData(self, data):
        # data should be of type Instruction
        
        if self.bus is None:
            raise RuntimeError(f"Device {hex(self.address)} not added to I2C bus")
        
        self.bus.bus.write_i2c_block_data(self.address, register, data=data)
        
    def readI2C(self):
        if self.bus is None:
            raise RuntimeError(f"Device {hex(self.address)} not added to I2C bus")
        
        return self.bus.bus.read_i2c_block_data(self.address, 0, 8)
    