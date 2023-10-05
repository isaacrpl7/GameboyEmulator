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
        
        # LCD Y coordinate
        if address == 0xFF44:
            print('Accessed LCD Y coordinate, but it is not implemented yet')
            return 0x90
        
        print(f'Address {hex(address)} not implemented')
        print(f'PC value is: {hex(self.cpu.registers.pc.get_value())}')
        return 0xFF

    def write_io(self, address, byte):
        if address == 0xFF01:
            # print('Wrote to Serial')
            self.cpu.serial.write(byte)

        if address == 0xFF02:
            # print('Wrote to Serial Control')
            # print(f'PC: {self.cpu.registers.pc.get_value()}')
            self.cpu.serial.write_serial_control(byte)
            
        # Write interrupt flag
        if address == 0xFF0F:
            self.cpu.interrupt_flag.set_value(byte)