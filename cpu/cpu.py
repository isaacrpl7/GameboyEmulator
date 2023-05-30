from cpu.registers import CPURegisters
from cpu.mmu import *
from cpu.utils import compose_bytes

class CPU:
    
    def __init__(self):
        self.registers = CPURegisters()
    
    def read_byte_from_pc(self):
        content = read_address(self.registers.pc.get_value())
        self.registers.pc.increment()
        return content
    
    def read_word_from_pc(self):
        """ word == 2 bytes """
        lsb = self.read_byte_from_pc()
        msb = self.read_byte_from_pc()
        return compose_bytes(msb, lsb)
    
    # Debug purposes
    def print_registers(self):
        print('')
        print('---------------REGISTERS-----------------')
        print(f'A: {hex(self.registers.a.get_value())}')
        print(f'B: {hex(self.registers.b.get_value())}')
        print(f'C: {hex(self.registers.c.get_value())}')
        print(f'D: {hex(self.registers.d.get_value())}')
        print(f'E: {hex(self.registers.e.get_value())}')
        print(f'H: {hex(self.registers.h.get_value())}')
        print(f'L: {hex(self.registers.l.get_value())}')
        print('')
        print(f'Flags: Z: {hex(self.registers.f.get_flag_zero())} S:{hex(self.registers.f.get_flag_subtract())} H:{hex(self.registers.f.get_flag_half_carry())} C:{hex(self.registers.f.get_flag_carry())}')
        print('')
        print(f'SP: {hex(self.registers.sp.get_value())}')
        print(f'PC: {hex(self.registers.pc.get_value())}')
        print('-----------------------------------------')
        print('')