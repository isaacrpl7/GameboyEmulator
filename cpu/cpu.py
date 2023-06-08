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
    def return_registers(self):
        return {
            'A': hex(self.registers.a.get_value()),
            'B': hex(self.registers.b.get_value()),
            'C': hex(self.registers.c.get_value()),
            'D': hex(self.registers.d.get_value()),
            'E': hex(self.registers.e.get_value()),
            'H': hex(self.registers.h.get_value()),
            'L': hex(self.registers.l.get_value()),
            'Z': hex(self.registers.f.get_flag_zero()),
            'S': hex(self.registers.f.get_flag_subtract()),
            'H': hex(self.registers.f.get_flag_half_carry()),
            'C': hex(self.registers.f.get_flag_carry()),
            'SP': hex(self.registers.sp.get_value()),
            'PC': hex(self.registers.pc.get_value())
        }