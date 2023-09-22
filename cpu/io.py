from cpu import cpu

def read_io(address):
    if address == 0xFF0F:
        return cpu.interrupt_flag.get_value()

def write_io(address, byte):
    if address == 0xFF0F:
        cpu.interrupt_flag.set_value(byte)