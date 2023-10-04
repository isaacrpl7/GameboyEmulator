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
            raise ValueError(f'Register value of {hex(value)} exceeds capacity of {hex(2**self.size)}!')
    
    def get_msb(self):
        if self.size == 16:
            return (self.value & 0xFF00) >> 8
        else:
            raise ValueError('Trying to get msb of a non 16-bit register')
    
    def get_lsb(self):
        if self.size == 16:
            return self.value & 0x00FF
        else:
            raise ValueError('Trying to get lsb of a non 16-bit register')

    def getSize(self):
        return self.size
    
    def get_value(self):
        return self.value
    
    def increment(self):
        self.value += 1
        return self.value
        
    def decrement(self):
        self.value -= 1
        return self.value

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
    
    def get_flag_zero(self):
        return get_bit(self.value, 7)

    def get_flag_subtract(self):
        return get_bit(self.value, 6)
    
    def get_flag_half_carry(self):
        return get_bit(self.value, 5)
    
    def get_flag_carry(self):
        return get_bit(self.value, 4)

class RegisterPair:

    def __init__(self, msr: Register, lsr: Register):
        if msr.getSize() == 8 and lsr.getSize() == 8:
            self.msr = msr
            self.lsr = lsr
        else:
            raise ValueError('Cannot join two registers without 8-bit of size')
    
    def set_value(self, value):
        if value < 65536:
            self.msr.set_value(value >> 8)
            self.lsr.set_value(value & 0xFF)
        else:
            raise ValueError(f'RegisterPair value {hex(value)} exceeds capacity!')
    
    def get_msb(self):
        return self.msr.get_value()
    
    def get_lsb(self):
        return self.lsr.get_value()

    def get_value(self):
        return compose_bytes(self.msr.get_value(), self.lsr.get_value())
    
    def increment(self):
        new_value = self.get_value() + 1
        self.set_value(new_value)
        return new_value
        
    def decrement(self):
        new_value = self.get_value() - 1
        self.set_value(new_value)
        return new_value
    


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