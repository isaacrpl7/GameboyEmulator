from cpu.opcodes import *
from cpu import cpu

def run_opcode(opcode: int):
    mapping = {
        0x00: [nop],
        0x01: [load_R_n16, [cpu.registers.bc]],
        0x02: [load_R1m_R2, [cpu.registers.bc, cpu.registers.a]],

        0x04: [inc_R, [cpu.registers.b]],
        0x05: [dec_R, [cpu.registers.b]],
        0x06: [load_R_n8, [cpu.registers.b]],

        0x08: [load_n16m_SP],

        0x0A: [load_R1_R2m, [cpu.registers.a, cpu.registers.bc]],

        0x0C: [inc_R, [cpu.registers.c]],
        0x0D: [dec_R, [cpu.registers.c]],
        0x0E: [load_R_n8, [cpu.registers.c]],


        0x11: [load_R_n16, [cpu.registers.de]],
        0x12: [load_R1m_R2, [cpu.registers.de, cpu.registers.a]],

        0x14: [inc_R, [cpu.registers.d]],
        0x15: [dec_R, [cpu.registers.d]],
        0x16: [load_R_n8, [cpu.registers.d]],



        0x1A: [load_R1_R2m, [cpu.registers.a, cpu.registers.de]],

        0x1C: [inc_R, [cpu.registers.e]],
        0x1D: [dec_R, [cpu.registers.e]],
        0x1E: [load_R_n8, [cpu.registers.e]],

        
        0x21: [load_R_n16, [cpu.registers.hl]],
        0x22: [load_inc_mR_R2, [cpu.registers.hl, cpu.registers.a]],

        0x24: [inc_R, [cpu.registers.h]],
        0x25: [dec_R, [cpu.registers.h]],
        0x26: [load_R_n8, [cpu.registers.h]],
        0x27: [daa],


        0x2A: [load_inc_R_R2m, [cpu.registers.a, cpu.registers.hl]],

        0x2C: [inc_R, [cpu.registers.l]],
        0x2D: [dec_R, [cpu.registers.l]],
        0x2E: [load_R_n8, [cpu.registers.l]],
        0x2F: [cpl]

    }
    args = []
    try:
        if len(mapping[opcode]) == 2:
            args = mapping[opcode][1]
        mapping[opcode][0](*args)
    except:
        return -1