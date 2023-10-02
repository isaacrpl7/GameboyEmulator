from cpu import cpu
from cpu.registers import Register, RegisterPair, FlagRegister
from cpu.utils import *
""" 
    When PC read an opcode identifier byte, it will increment.
    If the instruction have more arguments,
    it will pass execution to the function of the opcode 
    which will control the PC by itself
"""

def nop():
    pass
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
    register1.set_value(cpu.mmu.read_address(register2.get_value()))

def load_R1m_R2(register1: RegisterPair, register2: Register):
    """ LD (r16), r'
        Load the content of a register into the memory at address denoted by the register pair R1 """
    cpu.mmu.write_address(register1.get_value(), register2.get_value())

def load_R_n16m(register: Register):
    """ LD r, (n16)
        Load to register1 the value in the memory location of the 2 byte operands that PC will get """
    address = cpu.read_word_from_pc()
    register.set_value(cpu.mmu.read_address(address))

def load_n16m_R(register: Register):
    """ LD (n16), r
        Load the content of a register into the memory at address denoted by u16 (fetched by PC) """
    address = cpu.read_word_from_pc()
    cpu.mmu.write_address(address, register.get_value())

def load_Rm_n8(register: RegisterPair):
    """ LD (r16), n8
        Load 8-bit value fetched by PC to the memory location pointed by register R """
    content = cpu.read_byte_from_pc()
    cpu.mmu.write_address(register.get_value(), content)

def load_A_io():
    """ ld A, (FF00+n)
        Load from I/O registers in memory to a chosen register """
    offset = cpu.read_byte_from_pc()
    cpu.registers.a.set_value(cpu.mmu.read_address(0xFF00 + offset))

def load_io_A():
    """ ld (FF00+n), A
        Load from A register to I/O memory """
    offset = cpu.read_byte_from_pc()
    cpu.mmu.write_address(0xFF00 + offset, cpu.registers.a.get_value())

def load_A_ioC():
    """ ld A, (FF00+C)
        Load from I/O address in C to register A """
    offset = cpu.registers.c.get_value()
    cpu.registers.a.set_value(cpu.mmu.read_address(0xFF00 + offset))

def load_ioC_A():
    """ ld (FF00+C), A
        Load from A register into I/O address C """
    offset = cpu.registers.c.get_value()
    cpu.mmu.write_address(0xFF00 + offset, cpu.registers.a.get_value())

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
    cpu.mmu.write_address(address, cpu.registers.sp.get_value())

def load_SP_HL():
    """ ld SP,HL
        Load from HL register value to SP """
    cpu.registers.sp.set_value(cpu.registers.hl.get_value())

def push_R16(register: RegisterPair):
    """ push r16
        Push r16 value to stack """
    cpu.stack_push(register)

def pop_R16(register: RegisterPair):
    """ pop r16
        Pop the value from top of stack and store in r16 """
    cpu.stack_pop(register)


# 8-BIT ARITHMETIC
def add_A_R(register: Register):
    value = register.get_value() + cpu.registers.a.get_value()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((register.get_value() & 0xF) + (cpu.registers.a.get_value() & 0xF) > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)

def add_A_n8():
    content = cpu.read_byte_from_pc()
    value = content + cpu.registers.a.get_value()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((content & 0xF) + (cpu.registers.a.get_value() & 0xF) > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)

def add_A_HLm():
    """ A = A + (HL) """
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = content + cpu.registers.a.get_value()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((content & 0xF) + (cpu.registers.a.get_value() & 0xF) > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)

def adc_A_R(register: Register):
    """ Adding with carry """
    value = register.get_value() + cpu.registers.a.get_value() + cpu.registers.f.get_flag_carry()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((register.get_value() & 0xF) + (cpu.registers.a.get_value() & 0xF) + cpu.registers.f.get_flag_carry() > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)

def adc_A_n8():
    """ Adding with carry """
    content = cpu.read_byte_from_pc()
    value = content + cpu.registers.a.get_value() + cpu.registers.f.get_flag_carry()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((content & 0xF) + (cpu.registers.a.get_value() & 0xF) + cpu.registers.f.get_flag_carry() > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)

def adc_A_HLm():
    """ Adding with carry """
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = content + cpu.registers.a.get_value() + cpu.registers.f.get_flag_carry()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((content & 0xF) + (cpu.registers.a.get_value() & 0xF) + cpu.registers.f.get_flag_carry() > 0xF)
    cpu.registers.f.set_flag_carry(value > 0xFF)

    cpu.registers.a.set_value(value & 0xFF)

def sub_R(register: Register):
    """ A = A - R """
    content = register.get_value()
    value = cpu.registers.a.get_value() - content

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) < 0)
    cpu.registers.f.set_flag_carry(value < 0)

    cpu.registers.a.set_value(value & 0xFF)

def sub_n8():
    """ A = A - n8 """
    content = cpu.read_byte_from_pc()
    value = cpu.registers.a.get_value() - content

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) < 0)
    cpu.registers.f.set_flag_carry(value < 0)

    cpu.registers.a.set_value(value & 0xFF)

def sub_HLm():
    """ A = A - (HL) """
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = cpu.registers.a.get_value() - content

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) < 0)
    cpu.registers.f.set_flag_carry(value < 0)

    cpu.registers.a.set_value(value & 0xFF)

def sbc_R(register: Register):
    """ A = A - R - carry """
    content = register.get_value()
    value = cpu.registers.a.get_value() - content - cpu.registers.f.get_flag_carry()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) - cpu.registers.f.get_flag_carry() < 0)
    cpu.registers.f.set_flag_carry(value < 0)

    cpu.registers.a.set_value(value & 0xFF)

def sbc_n8():
    """ A = A - n8 - carry """
    content = cpu.read_byte_from_pc()
    value = cpu.registers.a.get_value() - content - cpu.registers.f.get_flag_carry()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) - cpu.registers.f.get_flag_carry() < 0)
    cpu.registers.f.set_flag_carry(value < 0)

    cpu.registers.a.set_value(value & 0xFF)

def sbc_HLm():
    """ A = A - (HL) - carry"""
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = cpu.registers.a.get_value() - content - cpu.registers.f.get_flag_carry()

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) - cpu.registers.f.get_flag_carry() < 0)
    cpu.registers.f.set_flag_carry(value < 0)

    cpu.registers.a.set_value(value & 0xFF)

def and_A_R(register: Register):
    content = register.get_value()
    value = cpu.registers.a.get_value() & content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(True)
    cpu.registers.f.set_flag_carry(False)

def and_A_n8():
    content = cpu.read_byte_from_pc()
    value = cpu.registers.a.get_value() & content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(True)
    cpu.registers.f.set_flag_carry(False)

def and_A_HLm():
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = cpu.registers.a.get_value() & content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(True)
    cpu.registers.f.set_flag_carry(False)

def xor_A_R(register: Register):
    content = register.get_value()
    value = cpu.registers.a.get_value() ^ content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(False)
    cpu.registers.f.set_flag_carry(False)

def xor_A_n8():
    content = cpu.read_byte_from_pc()
    value = cpu.registers.a.get_value() ^ content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(False)
    cpu.registers.f.set_flag_carry(False)

def xor_A_HLm():
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = cpu.registers.a.get_value() ^ content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(False)
    cpu.registers.f.set_flag_carry(False)

def or_A_R(register: Register):
    content = register.get_value()
    value = cpu.registers.a.get_value() | content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(False)
    cpu.registers.f.set_flag_carry(False)

def or_A_n8():
    content = cpu.read_byte_from_pc()
    value = cpu.registers.a.get_value() | content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(False)
    cpu.registers.f.set_flag_carry(False)

def or_A_HLm():
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = cpu.registers.a.get_value() | content
    cpu.registers.a.set_value(value)

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry(False)
    cpu.registers.f.set_flag_carry(False)

def cp_A_R(register: Register):
    """ Compare A and R (subtract without storing)"""
    content = register.get_value()
    value = cpu.registers.a.get_value() - content

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) < 0)
    cpu.registers.f.set_flag_carry(value < 0)

def cp_A_n8():
    """ Compare A and n8 (subtract without storing)"""
    content = cpu.read_byte_from_pc()
    value = cpu.registers.a.get_value() - content

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) < 0)
    cpu.registers.f.set_flag_carry(value < 0)

def cp_A_HLm():
    """ Compare A and (HL) (subtract without storing)"""
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = cpu.registers.a.get_value() - content

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((cpu.registers.a.get_value() & 0xF) - (content & 0xF) < 0)
    cpu.registers.f.set_flag_carry(value < 0)

def inc_R(register:Register):
    content = register.get_value()
    value = content + 1

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((register.get_value() & 0xF) + 1 > 0xF)

    register.set_value((value & 0xFF))

def inc_HLm():
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = content + 1

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(False)
    cpu.registers.f.set_flag_half_carry((content & 0xF) + 1 > 0xF)

    cpu.mmu.write_address(cpu.registers.hl.get_value(), value & 0xFF)

def dec_R(register: Register):
    content = register.get_value()
    value = content - 1

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((content & 0xF) - 1 < 0)

    register.set_value(value & 0xFF)

def dec_HLm():
    content = cpu.mmu.read_address(cpu.registers.hl.get_value())
    value = content - 1

    cpu.registers.f.set_flag_zero((value & 0xFF) == 0)
    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry((content & 0xF) - 1 < 0)

    cpu.mmu.write_address(cpu.registers.hl.get_value(), value & 0xFF)

def daa():
    """ Transform A register into BCD representation using carry if necessary """
    a_value = cpu.registers.a.get_value()
    if not cpu.registers.f.get_flag_subtract(): # after an addition, adjust if (half-)carry occurred or if result is out of bounds
        if cpu.registers.f.get_flag_carry() or a_value > 0x99:
            a_value += 0x60
            cpu.registers.f.set_flag_carry(True)
        if cpu.registers.f.get_flag_half_carry() or (a_value & 0x0F) > 0x09:
            a_value += 0x06
    else: # after a subtraction, only adjust if (half-)carry occurred
        if cpu.registers.f.get_flag_carry():
            a_value -= 0x60
        if cpu.registers.f.get_flag_half_carry():
            a_value -= 0x06
    
    cpu.registers.a.set_value((a_value & 0xFF))
    cpu.registers.f.set_flag_zero((a_value & 0xFF) == 0)
    cpu.registers.f.set_flag_half_carry(False)

def cpl():
    """ A = A xor FF """
    content = cpu.registers.a.get_value()
    cpu.registers.a.set_value(content ^ 0xFF)

    cpu.registers.f.set_flag_subtract(True)
    cpu.registers.f.set_flag_half_carry(True)

# JUMP INSTRUCTIONS

def jp_nn():
    address = cpu.read_word_from_pc()
    cpu.registers.pc.set_value(address)

def jp_hl():
    cpu.registers.pc.set_value(cpu.registers.hl.get_value())

def jp_cond(condition: str):
    if cpu.check_condition(condition): # Remember to change cycle number: 3 cycles if condition is false, 4 cycles if it is true
        jp_nn()
    else:
        cpu.read_word_from_pc()

def jr_nn():
    offset = cpu.read_byte_from_pc()
    offset = offset - 256 if offset >= 128 else offset # Unsigned to signed

    pc_value = cpu.registers.pc.get_value()
    cpu.registers.pc.set_value(pc_value + offset)

def jr_cond(condition: str):
    if cpu.check_condition(condition):
        jr_nn()
    else:
        cpu.read_byte_from_pc()
    
# CALL INSTRUCTIONS

def call_nn():
    address = cpu.read_word_from_pc()
    push_R16(cpu.registers.pc)
    cpu.registers.pc.set_value(address)

def call_cond(condition: str):
    if cpu.check_condition(condition):
        call_nn()
    else:
        cpu.read_word_from_pc()

# RETURN INSTRUCTIONS

def ret():
    pop_R16(cpu.registers.pc)

def ret_cond(condition: str):
    if cpu.check_condition(condition):
        ret()
    
def reti():
    ret()
    enable_interrupts()
    
# RST
def rst(address: int):
    push_R16(cpu.registers.pc)
    cpu.registers.pc.set_value(address)

# CONTROL INSTRUCTIONS

def disable_interrupts():
    cpu.interrupt_master_enabled = False

def enable_interrupts():
    cpu.interrupt_master_enabled = True

# 16-bit arithmetic
def inc_r16(register: RegisterPair):
    """ Increment a 16-bit register """
    register.increment()

def dec_r16(register: RegisterPair):
    """ Decrement a 16-bit register """
    register.decrement()