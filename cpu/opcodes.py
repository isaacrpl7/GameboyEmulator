from cpu import cpu
from cpu.mmu import *
from cpu.registers import Register, RegisterPair, FlagRegister
from cpu.utils import *
""" 
    When PC read an opcode identifier byte, it will increment.
    If the instruction have more arguments,
    it will pass execution to the function of the opcode 
    which will control the PC by itself
"""


# 8-BIT LOAD INSTRUCTIONS
def load_R_n8(register: Register):
    """ LD R, n8
        Load 8-bit value read by pc in the opcode operand to a register """
    content = cpu.read_byte_from_pc()
    register.set_value(content)

def load_R1_R2(register1: Register, register2: Register):
    """ LD r, r'
        Load 8-bit value of register R2 into R1 """
    register1.set_value(register2.get_value())

def load_R1_R2m(register1: Register, register2: RegisterPair):
    """ LD r, (r'16) 
        Load to register1 the value in the memory location of register2 (16-bits)
    """
    register1.set_value(read_address(register2.get_value()))

def load_R1m_R2(register1: RegisterPair, register2: Register):
    """ LD (r16), r'
        Load the content of a register into the memory at address denoted by the register pair R1 """
    write_address(register1.get_value(), register2.get_value())

def load_R_n16m(register: Register):
    """ LD r, (n16)
        Load to register1 the value in the memory location of the 2 byte operands that PC will get """
    address = cpu.read_word_from_pc()
    register.set_value(read_address(address))

def load_n16m_R(register: Register):
    """ LD (n16), r
        Load the content of a register into the memory at address denoted by u16 (fetched by PC) """
    address = cpu.read_word_from_pc()
    write_address(address, register.get_value())

def load_Rm_n8(register: RegisterPair):
    """ LD (r16), n8
        Load 8-bit value fetched by PC to the memory location pointed by register R """
    content = cpu.read_byte_from_pc()
    write_address(register.get_value(), content)

def load_A_io():
    """ ld A, (FF00+n)
        Load from I/O registers in memory to a chosen register """
    offset = cpu.read_byte_from_pc()
    cpu.registers.a.set_value(read_address(0xFF00 + offset))

def load_io_A():
    """ ld (FF00+n), A
        Load from A register to I/O memory """
    offset = cpu.read_byte_from_pc()
    write_address(0xFF00 + offset, cpu.registers.a.get_value())

def load_A_ioC():
    """ ld A, (FF00+C)
        Load from I/O address in C to register A """
    offset = cpu.registers.c.get_value()
    cpu.registers.a.set_value(read_address(0xFF00 + offset))

def load_ioC_A():
    """ ld (FF00+C), A
        Load from A register into I/O address C """
    offset = cpu.registers.c.get_value()
    write_address(0xFF00 + offset, cpu.registers.a.get_value())

def load_inc_mR_R2(register1: RegisterPair, register2: Register):
    """ ldi (r16), r'
        Load from register r' to memory pointed by r16 and then increment r16"""
    load_R1m_R2(register1, register2)
    register1.increment()
    
def load_inc_R_R2m(register1: Register, register2: RegisterPair):
    """ ldi r, (r'16)
        Load from memory pointed by r16 to register r and then increment r16"""
    load_R1_R2m(register1, register2)
    register2.increment()

def load_dec_mR_R2(register1: RegisterPair, register2: Register):
    """ ldd (r16), r'
        Load from register r' to memory pointed by r16 and then decrement r16"""
    load_R1m_R2(register1, register2)
    register1.decrement()
    
def load_dec_R_R2m(register1: Register, register2: RegisterPair):
    """ ldd r, (r'16)
        Load from memory pointed by r16 to register r and then decrement r16"""
    load_R1_R2m(register1, register2)
    register2.decrement()


# 16-BIT LOAD INSTRUCTIONS
def load_R_n16(register: RegisterPair):
    """ ld r16, nn
        Load from 2 bytes operand that PC will get to the given 16-bit register"""
    content = cpu.read_word_from_pc()
    register.set_value(content)

def load_n16m_SP():
    """ ld (nn),SP
        Load from Stack Pointer to the memory address pointed by 2 bytes fetched from PC """
    address = cpu.read_word_from_pc()
    write_address(address, cpu.registers.sp.get_value())

def load_SP_HL():
    """ ld SP,HL
        Load from HL register value to SP """
    cpu.registers.sp.set_value(cpu.registers.hl.get_value())

def push_R16(register: RegisterPair):
    """ push r16
        Push r16 value to stack """
    cpu.registers.sp.decrement()
    write_address(cpu.registers.sp.get_value(),register.get_msb())
    cpu.registers.sp.decrement()
    write_address(cpu.registers.sp.get_value(),register.get_lsb())

def pop_R16(register: RegisterPair):
    """ pop r16
        Pop the value from top of stack and store in r16 """
    low_signf = read_address(cpu.registers.sp.get_value())
    cpu.registers.sp.increment()
    high_signif = read_address(cpu.registers.sp.get_value())
    cpu.registers.sp.increment()

    value = compose_bytes(high_signif, low_signf)
    register.set_value(value)


# 8-BIT ARITHMETIC
def add_A_R(register: Register):
    value = register.get_value() + cpu.registers.a.get_value()

    cpu.registers.f.set_flag_zero(value == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((register.get_value() & 0xF) + (cpu.registers.a.get_value() & 0xF) > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)