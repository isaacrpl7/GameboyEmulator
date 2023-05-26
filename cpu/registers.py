from cpu.utils import *

class Register:

    def __init__(self, value, size=8):
        if value < 2**size:
            self.value = value
            self.size = size
        else:
            raise ValueError('Registor value exceeds capacity!')
    
    def set_value(self, value):
        if value < 2**self.size:
            self.value = value
        else:
            raise ValueError('Registor value exceeds capacity!')
        
    def getSize(self):
        return self.size
    
    def get_value(self):
        return self.value
    
    def increment(self):
        self.value += 1
        
    def decrement(self):
        self.value -= 1

"""
7	z	Zero flag
6	n	Subtraction flag (BCD)
5	h	Half Carry flag (BCD)
4	c	Carry flag
"""
class FlagRegister(Register):
    def set_flag_zero(self, value):
        self.value = set_bit(self.value, 7, value)

    def set_flag_subtract(self, value):
        self.value = set_bit(self.value, 6, value)

    def set_flag_half_carry(self, value):
        self.value = set_bit(self.value, 5, value)

    def set_flag_carry(self, value):
        self.value = set_bit(self.value, 4, value)

class RegisterPair:

    def __init__(self, msb, lsb):
        if msb.getSize() == 8 and lsb.getSize() == 8:
            self.msb = msb
            self.lsb = lsb
        else:
            raise ValueError('Cannot join two registers without 8-bit of size')
    
    def set_value(self, value):
        if value < 65536:
            self.msb.set_value(value >> 8)
            self.lsb.set_value(value & 0xFF)
        else:
            raise ValueError('Registor value exceeds capacity!')
    
    def get_msb(self):
        return self.msb
    
    def get_lsb(self):
        return self.lsb

    def get_value(self):
        return compose_bytes(self.msb.get_value(), self.lsb.get_value())
    
    def increment(self):
        new_value = self.get_value() + 1
        self.set_value(new_value)
        
    def decrement(self):
        new_value = self.get_value() - 1
        self.set_value(new_value)
    


class CPURegisters:

    def __init__(self):
        self.a = Register(0x0)
        self.f = FlagRegister(0x0)
        self.b = Register(0x0)
        self.c = Register(0x0)
        self.d = Register(0x0)
        self.e = Register(0x0)
        self.h = Register(0x0)
        self.l = Register(0x0)

        self.sp = Register(0xFFFE, 16) # starts in 0xFFFE
        self.pc = Register(0x100, 16) # starts in 0x100

        self.af = RegisterPair(self.b, self.c)
        self.bc = RegisterPair(self.b, self.c)
        self.de = RegisterPair(self.d, self.e)
        self.hl = RegisterPair(self.h, self.l)

    
    # def set(self, register, value):
    #     if register == 'A':
    #         self.a.set_value(value)
    #     elif register == 'B':
    #         self.b.set_value(value)
    #     elif register == 'C':
    #         self.c.set_value(value)
    #     elif register == 'D':
    #         self.d.set_value(value)
    #     elif register == 'E':
    #         self.e.set_value(value)
    #     elif register == 'F':
    #         self.f.set_value(value)
    #     elif register == 'H':
    #         self.h.set_value(value)
    #     elif register == 'L':
    #         self.l.set_value(value)
    #     elif register == 'SP':
    #         self.sp.set_value(value)
    #     elif register == 'PC':
    #         self.pc.set_value(value)
    #     elif register == 'BC':
    #         self.bc.set_value(value)
    #     elif register == 'DE':
    #         self.de.set_value(value)
    #     elif register == 'HL':
    #         self.hl.set_value(value)

    
    # def read(self, register):
    #     if register == 'A':
    #         return self.a.get_value()
    #     elif register == 'B':
    #         return self.b.get_value()
    #     elif register == 'C':
    #         return self.c.get_value()
    #     elif register == 'D':
    #         return self.d.get_value()
    #     elif register == 'E':
    #         return self.e.get_value()
    #     elif register == 'F':
    #         return self.f.get_value()
    #     elif register == 'H':
    #         return self.h.get_value()
    #     elif register == 'L':
    #         return self.l.get_value()
    #     elif register == 'SP':
    #         return self.sp.get_value()
    #     elif register == 'PC':
    #         return self.pc.get_value()
    #     elif register == 'BC':
    #         return self.bc.get_value()
    #     elif register == 'DE':
    #         return self.de.get_value()
    #     elif register == 'HL':
    #         return self.hl.get_value()