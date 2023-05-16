class Register:

    def __init__(self, value, size=8):
        if value < 2**size:
            self.value = value
            self.size = size
            print(f'register initiated with value of {value}')
        else:
            raise ValueError('Registor value exceeds capacity!')
    
    def setValue(self, value):
        if value < 2**self.size:
            self.value = value
        else:
            raise ValueError('Registor value exceeds capacity!')
        
    def getSize(self):
        return self.size
    
    def getValue(self):
        return self.value
        

class RegisterPair:

    def __init__(self, msr, lsr):
        if msr.getSize() == 8 and lsr.getSize() == 8:
            self.msr = msr
            self.lsr = lsr
        else:
            raise ValueError('Cannot join two registers without 8-bit of size')
    
    def setValue(self, value):
        if value < 65536:
            self.msr.setValue(value >> 8)
            self.lsr.setValue(value & 0xFF)
        else:
            raise ValueError('Registor value exceeds capacity!')
    
    def getValue(self):
        return (self.msr.getValue() << 8) | self.lsr.getValue()
    


class CPURegisters:

    def __init__(self):
        self.a = Register(0x0)
        self.f = Register(0x0)
        self.b = Register(0x0)
        self.c = Register(0x0)
        self.d = Register(0x0)
        self.e = Register(0x0)
        self.h = Register(0x0)
        self.l = Register(0x0)

        self.sp = Register(0x0, 16)
        self.pc = Register(0x0, 16)

        self.bc = RegisterPair(self.b, self.c)
        self.de = RegisterPair(self.d, self.e)
        self.hl = RegisterPair(self.h, self.l)

    
    def set(self, register, value):
        if register == 'A':
            self.a.setValue(value)
        elif register == 'B':
            self.b.setValue(value)
        elif register == 'C':
            self.c.setValue(value)
        elif register == 'D':
            self.d.setValue(value)
        elif register == 'E':
            self.e.setValue(value)
        elif register == 'F':
            self.f.setValue(value)
        elif register == 'H':
            self.h.setValue(value)
        elif register == 'L':
            self.l.setValue(value)
        elif register == 'SP':
            self.sp.setValue(value)
        elif register == 'PC':
            self.pc.setValue(value)
        elif register == 'BC':
            self.bc.setValue(value)
        elif register == 'DE':
            self.de.setValue(value)
        elif register == 'HL':
            self.hl.setValue(value)

    
    def read(self, register):
        if register == 'A':
            return self.a.getValue()
        elif register == 'B':
            return self.b.getValue()
        elif register == 'C':
            return self.c.getValue()
        elif register == 'D':
            return self.d.getValue()
        elif register == 'E':
            return self.e.getValue()
        elif register == 'F':
            return self.f.getValue()
        elif register == 'H':
            return self.h.getValue()
        elif register == 'L':
            return self.l.getValue()
        elif register == 'SP':
            return self.sp.getValue()
        elif register == 'PC':
            return self.pc.getValue()
        elif register == 'BC':
            return self.bc.getValue()
        elif register == 'DE':
            return self.de.getValue()
        elif register == 'HL':
            return self.hl.getValue()