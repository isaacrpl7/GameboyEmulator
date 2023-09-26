from cpu.utils import get_bit

class Serial:

    def __init__(self):
        self.data = 0
    
    def read(self):
        return self.data

    def write(self, byte):
        self.data = byte

    def write_serial_control(self, byte):
        if get_bit(byte, 7):
            print(chr(byte))