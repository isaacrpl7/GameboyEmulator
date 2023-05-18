from cpu import cpu
from cpu.mmu import *
from cpu.registers import Register, RegisterPair, FlagRegister
""" 
    When PC read an opcode identifier byte, it will increment.
    If the instruction have more arguments,
    it will pass execution to the function of the opcode 
    which will control the PC by itself
"""

def load_R_n8(register: Register):
    """ Load 8-bit value read by pc in the opcode operand to a register """
    content = cpu.read_byte_from_pc()
    register.set_value(content)

def load_R1_R2(register1: Register, register2: Register):
    """ Load 8-bit register R2 into R1 """
    register1.set_value(register2.get_value())

def load_R1_R2m(register1: Register, register2: RegisterPair):
    """ LD r, (r16') 
        Load to register1 the value in the memory location of register2 (16-bits)
    """
    register1.set_value(read_address(register2.get_value()))

def load_R_u16m(register1: Register):
    """ Load to register1 the value in the memory location of the 2 byte operands that PC will get """
    address = cpu.read_word_from_pc()
    register1.set_value(read_address(address))