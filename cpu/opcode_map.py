from cpu.opcodes import *
from cpu import cpu

opcode_cycles = [
    1, 3, 2, 2, 1, 1, 2, 1, 5, 2, 2, 2, 1, 1, 2, 1,
    1, 3, 2, 2, 1, 1, 2, 1, 3, 2, 2, 2, 1, 1, 2, 1,
    2, 3, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1,
    2, 3, 2, 2, 3, 3, 3, 1, 2, 2, 2, 2, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    2, 3, 3, 4, 3, 4, 2, 4, 2, 4, 3, 0, 3, 6, 2, 4,
    2, 3, 3, 0, 3, 4, 2, 4, 2, 4, 3, 0, 3, 0, 2, 4,
    3, 3, 2, 0, 0, 4, 2, 4, 4, 1, 4, 0, 0, 0, 2, 4,
    3, 3, 2, 1, 0, 4, 2, 4, 3, 2, 4, 1, 0, 0, 2, 4
]

opcode_cycles_changed = [ # Some instructions change their cycle number based on a condition. (Note that this happens only with some jump, call and ret instructions)
    1, 3, 2, 2, 1, 1, 2, 1, 5, 2, 2, 2, 1, 1, 2, 1,
    1, 3, 2, 2, 1, 1, 2, 1, 3, 2, 2, 2, 1, 1, 2, 1,
    3, 3, 2, 2, 1, 1, 2, 1, 3, 2, 2, 2, 1, 1, 2, 1,
    3, 3, 2, 2, 3, 3, 3, 1, 3, 2, 2, 2, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1,
    5, 3, 4, 4, 6, 4, 2, 4, 5, 4, 4, 0, 6, 6, 2, 4,
    5, 3, 4, 0, 6, 4, 2, 4, 5, 4, 4, 0, 6, 0, 2, 4,
    3, 3, 2, 0, 0, 4, 2, 4, 4, 1, 4, 0, 0, 0, 2, 4,
    3, 3, 2, 1, 0, 4, 2, 4, 3, 2, 4, 1, 0, 0, 2, 4
]

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

        0x18: [jr_nn],

        0x1A: [load_R1_R2m, [cpu.registers.a, cpu.registers.de]],

        0x1C: [inc_R, [cpu.registers.e]],
        0x1D: [dec_R, [cpu.registers.e]],
        0x1E: [load_R_n8, [cpu.registers.e]],

        0x20: [jr_cond, ["NZ"]],
        0x21: [load_R_n16, [cpu.registers.hl]],
        0x22: [load_inc_mR_R2, [cpu.registers.hl, cpu.registers.a]],

        0x24: [inc_R, [cpu.registers.h]],
        0x25: [dec_R, [cpu.registers.h]],
        0x26: [load_R_n8, [cpu.registers.h]],
        0x27: [daa],
        0x28: [jr_cond, ["Z"]],

        0x2A: [load_inc_R_R2m, [cpu.registers.a, cpu.registers.hl]],

        0x2C: [inc_R, [cpu.registers.l]],
        0x2D: [dec_R, [cpu.registers.l]],
        0x2E: [load_R_n8, [cpu.registers.l]],
        0x2F: [cpl],
        0x30: [jr_cond, ["NC"]],
        0x31: [load_R_n16, [cpu.registers.sp]],
        0x32: [load_dec_mR_R2, [cpu.registers.hl, cpu.registers.a]],

        0x34: [inc_HLm],
        0x35: [dec_HLm],
        0x36: [load_Rm_n8, [cpu.registers.hl]],

        0x38: [jr_cond, ["C"]],

        0x3A: [load_dec_R_R2m, [cpu.registers.a, cpu.registers.hl]],

        0x3C: [inc_R, [cpu.registers.a]],
        0x3D: [dec_R, [cpu.registers.a]],
        0x3E: [load_R_n8, [cpu.registers.a]],

        0x40: [load_R1_R2, [cpu.registers.b, cpu.registers.b]],
        0x41: [load_R1_R2, [cpu.registers.b, cpu.registers.c]],
        0x42: [load_R1_R2, [cpu.registers.b, cpu.registers.d]],
        0x43: [load_R1_R2, [cpu.registers.b, cpu.registers.e]],
        0x44: [load_R1_R2, [cpu.registers.b, cpu.registers.h]],
        0x45: [load_R1_R2, [cpu.registers.b, cpu.registers.l]],
        0x46: [load_R1_R2m, [cpu.registers.b, cpu.registers.hl]],
        0x47: [load_R1_R2, [cpu.registers.b, cpu.registers.a]],
        0x48: [load_R1_R2, [cpu.registers.c, cpu.registers.b]],
        0x49: [load_R1_R2, [cpu.registers.c, cpu.registers.c]],
        0x4A: [load_R1_R2, [cpu.registers.c, cpu.registers.d]],
        0x4B: [load_R1_R2, [cpu.registers.c, cpu.registers.e]],
        0x4C: [load_R1_R2, [cpu.registers.c, cpu.registers.h]],
        0x4D: [load_R1_R2, [cpu.registers.c, cpu.registers.l]],
        0x4E: [load_R1_R2m, [cpu.registers.c, cpu.registers.hl]],
        0x4F: [load_R1_R2, [cpu.registers.c, cpu.registers.a]],
        0x50: [load_R1_R2, [cpu.registers.d, cpu.registers.b]],
        0x51: [load_R1_R2, [cpu.registers.d, cpu.registers.c]],
        0x52: [load_R1_R2, [cpu.registers.d, cpu.registers.d]],
        0x53: [load_R1_R2, [cpu.registers.d, cpu.registers.e]],
        0x54: [load_R1_R2, [cpu.registers.d, cpu.registers.h]],
        0x55: [load_R1_R2, [cpu.registers.d, cpu.registers.l]],
        0x56: [load_R1_R2m, [cpu.registers.d, cpu.registers.hl]],
        0x57: [load_R1_R2, [cpu.registers.d, cpu.registers.a]],
        0x58: [load_R1_R2, [cpu.registers.e, cpu.registers.b]],
        0x59: [load_R1_R2, [cpu.registers.e, cpu.registers.c]],
        0x5A: [load_R1_R2, [cpu.registers.e, cpu.registers.d]],
        0x5B: [load_R1_R2, [cpu.registers.e, cpu.registers.e]],
        0x5C: [load_R1_R2, [cpu.registers.e, cpu.registers.h]],
        0x5D: [load_R1_R2, [cpu.registers.e, cpu.registers.l]],
        0x5E: [load_R1_R2m, [cpu.registers.e, cpu.registers.hl]],
        0x5F: [load_R1_R2, [cpu.registers.e, cpu.registers.a]],
        0x60: [load_R1_R2, [cpu.registers.h, cpu.registers.b]],
        0x61: [load_R1_R2, [cpu.registers.h, cpu.registers.c]],
        0x62: [load_R1_R2, [cpu.registers.h, cpu.registers.d]],
        0x63: [load_R1_R2, [cpu.registers.h, cpu.registers.e]],
        0x64: [load_R1_R2, [cpu.registers.h, cpu.registers.h]],
        0x65: [load_R1_R2, [cpu.registers.h, cpu.registers.l]],
        0x66: [load_R1_R2m, [cpu.registers.h, cpu.registers.hl]],
        0x67: [load_R1_R2, [cpu.registers.h, cpu.registers.a]],
        0x68: [load_R1_R2, [cpu.registers.l, cpu.registers.b]],
        0x69: [load_R1_R2, [cpu.registers.l, cpu.registers.c]],
        0x6A: [load_R1_R2, [cpu.registers.l, cpu.registers.d]],
        0x6B: [load_R1_R2, [cpu.registers.l, cpu.registers.e]],
        0x6C: [load_R1_R2, [cpu.registers.l, cpu.registers.h]],
        0x6D: [load_R1_R2, [cpu.registers.l, cpu.registers.l]],
        0x6E: [load_R1_R2m, [cpu.registers.l, cpu.registers.hl]],
        0x6F: [load_R1_R2, [cpu.registers.l, cpu.registers.a]],
        0x70: [load_R1m_R2, [cpu.registers.hl, cpu.registers.b]],
        0x71: [load_R1m_R2, [cpu.registers.hl, cpu.registers.c]],
        0x72: [load_R1m_R2, [cpu.registers.hl, cpu.registers.d]],
        0x73: [load_R1m_R2, [cpu.registers.hl, cpu.registers.e]],
        0x74: [load_R1m_R2, [cpu.registers.hl, cpu.registers.h]],
        0x75: [load_R1m_R2, [cpu.registers.hl, cpu.registers.l]],

        0x77: [load_R1m_R2, [cpu.registers.hl, cpu.registers.a]],
        0x78: [load_R1_R2, [cpu.registers.a, cpu.registers.b]],
        0x79: [load_R1_R2, [cpu.registers.a, cpu.registers.c]],
        0x7A: [load_R1_R2, [cpu.registers.a, cpu.registers.d]],
        0x7B: [load_R1_R2, [cpu.registers.a, cpu.registers.e]],
        0x7C: [load_R1_R2, [cpu.registers.a, cpu.registers.h]],
        0x7D: [load_R1_R2, [cpu.registers.a, cpu.registers.l]],
        0x7E: [load_R1_R2m, [cpu.registers.a, cpu.registers.hl]],
        0x7F: [load_R1_R2, [cpu.registers.a, cpu.registers.a]],

        # ...

        0xC0: [ret_cond, ["NZ"]],

        0xC2: [jp_cond, ["NZ"]],
        0xC3: [jp_nn],
        0xC4: [call_cond, ["NZ"]],


        0xC7: [rst, [0x0]],
        0xC8: [ret_cond, ["Z"]],
        0xC9: [ret],
        0xCA: [jp_cond, ["Z"]],
        
        0xCC: [call_cond, ["Z"]],
        0xCD: [call_nn],

        0xCF: [rst, [0x08]],
        0xD0: [ret_cond, ["NC"]],

        0xD2: [jr_cond, ["NC"]],

        0xD4: [call_cond, ["NC"]],


        0xD7: [rst, [0x10]],
        0xD8: [ret_cond, ["C"]],

        0xDA: [jp_cond, ["C"]],

        0xDC: [call_cond, ["C"]],


        0xDF: [rst, [0x18]],

        # ...

        0xE7: [rst, [0x20]],

        0xE9: [jp_hl],





        0xEF: [rst, [0x28]],

        # ...

        0xF7: [rst, [0x30]],

        # ...
        
        0xFF: [rst, [0x38]]
    }
    args = []
    try:
        if len(mapping[opcode]) == 2:
            args = mapping[opcode][1]
        mapping[opcode][0](*args)
        return opcode_cycles[opcode] if not cpu.reset_change_cycle() else opcode_cycles_changed[opcode]
    except:
        return 0