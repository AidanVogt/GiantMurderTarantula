import smbus2
from typing import Tuple
from gaits import ACTION_NONE

# Sending instructions from the pi to the arduinos
# Gait planning done at highest level
# Get instruction from d-pad -> translate into a movement class (i.e. forward, backwards)

class Instruction:
    def __init__(self, bus, instructions = Tuple[int, int, int, int, int, int]):
        
        # single byte defines instructions
        self.bus = bus
        self.instructions = instructions

        
    def sendToLegs(self):
        
        # names of the legs (match the order of instructions)
        legs = sorted(self.bus.devices.keys())
        print(len(legs))
        num = 0
        
        # send each to legs if not none
        for inst in self.instructions:
            
            if len(legs) == 1:
                self.bus.devices[legs[num]].sendData(inst)
                break
            num += 1
            
    def recallCommand(self):
        
        legs = sorted(self.bus.devices.keys())
        num = len(legs)
        print("Num devices connected: ", num)
        
        for i in range(num):
            cmd = self.bus.devices[legs[i]].readI2C()
            
            print(f"Command sent to {self.bus.devices[legs[i]].name}: {cmd}")
        
            
    def checkFinished(self):
        print("Checking if done")
        
        num_finished = 0
        finished_devices = self.bus.pollArduinos()
        
        while num_finished < len(self.bus.devices.keys()):
            finished_devices = self.bus.pollArduinos()
            num_finished += finished_devices
        
        print("All devices finished")



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
        # arduinos can send a true/false determining whether or not they complete instruction
        # each ino sends 1 (if the instruction is finished)
        
        finished_devices = 0
        
        for device in self.devices.values():

            try:
                response = device.readI2C()
                print(response, "response")
                
                # TODO: testing response is done or not
                if response == 1:
                    finished_devices += 1
                    print(f"{device.name} address {device.address} finished")
                
            # check for issues with connectivity
            except OSError as e:
                print(f"Failed to poll device {hex(device.address)}: {e}")
                # break
    
        return finished_devices
    
    def WriteByte(self, address, data):
        self.bus.write_byte(address, data)
        
    def ReadByte(self, address):
        return self.bus.read_byte(address)
    
class GMTIno:
    def __init__(self, name, address):
        # init unique address for Arduinos
        self.address = address
        self.name = name
        self.bus = None
        
    def sendData(self, data):
        print(f"Sending data to Arduino {self.name} address: {hex(self.address)}")
        
        if self.bus is None:
            raise RuntimeError(f"Device {hex(self.address)} not added to I2C bus")
        
        self.bus.WriteByte(self.address, data)
        
    def readI2C(self):
        if self.bus is None:
            raise RuntimeError(f"Device {hex(self.address)} not added to I2C bus")
        
        print("READING FROM address", self.address)
        return self.bus.ReadByte(self.address)
        
    
def testI2C(bus):
    # bus of type I2CBus
    a = tuple([i for i in range(len(bus.devices.items()))])
    b = a[::-1]
    
    # make instructs
    test = Instruction(bus, a)
    test2 = Instruction(bus, b)
    
    test.sendToLegs()
    test.recallCommand()
    print("Finish first test - copy instruction that was sent")
    
    test2.sendToLegs()
    test2.checkFinished()
    
    print("Sent second instruction to legs")
