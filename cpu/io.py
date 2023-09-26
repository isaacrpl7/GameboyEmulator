class IO:
    def __init__(self, cpu):
        self.cpu = cpu

    def read_io(self, address):
        if address == 0xFF01:
            return self.cpu.serial.read()

        if address == 0xFF02:
            print('Cannot read serial control')
            return 0xFF

        # Read interrupt flag
        if address == 0xFF0F:
            return self.cpu.interrupt_flag.get_value()

    def write_io(self, address, byte):
        if address == 0xFF01:
            self.cpu.serial.write(byte)

        if address == 0xFF02:
            self.cpu.serial.write_serial_control(byte)
            
        # Write interrupt flag
        if address == 0xFF0F:
            self.cpu.interrupt_flag.set_value(byte)