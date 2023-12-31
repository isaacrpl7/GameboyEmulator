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

prefixed_opcode_cycles = [
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2,
    2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2,
    2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2,
    2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2,
    2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 4, 2
]

def run_opcode(opcode: int):
    mapping = {
        0x00: [nop],
        0x01: [load_R_n16, [cpu.registers.bc]],
        0x02: [load_R1m_R2, [cpu.registers.bc, cpu.registers.a]],
        0x03: [inc_r16, [cpu.registers.bc]],
        0x04: [inc_R, [cpu.registers.b]],
        0x05: [dec_R, [cpu.registers.b]],
        0x06: [load_R_n8, [cpu.registers.b]],

        0x08: [load_n16m_SP],
        0x09: [add_HL_rr, [cpu.registers.bc]],
        0x0A: [load_R1_R2m, [cpu.registers.a, cpu.registers.bc]],
        0x0B: [dec_r16, [cpu.registers.bc]],
        0x0C: [inc_R, [cpu.registers.c]],
        0x0D: [dec_R, [cpu.registers.c]],
        0x0E: [load_R_n8, [cpu.registers.c]],


        0x11: [load_R_n16, [cpu.registers.de]],
        0x12: [load_R1m_R2, [cpu.registers.de, cpu.registers.a]],
        0x13: [inc_r16, [cpu.registers.de]],
        0x14: [inc_R, [cpu.registers.d]],
        0x15: [dec_R, [cpu.registers.d]],
        0x16: [load_R_n8, [cpu.registers.d]],
        0x17: [rl_a],
        0x18: [jr_nn],
        0x19: [add_HL_rr, [cpu.registers.de]],
        0x1A: [load_R1_R2m, [cpu.registers.a, cpu.registers.de]],
        0x1B: [dec_r16, [cpu.registers.de]],
        0x1C: [inc_R, [cpu.registers.e]],
        0x1D: [dec_R, [cpu.registers.e]],
        0x1E: [load_R_n8, [cpu.registers.e]],
        0x1F: [rr_a],
        0x20: [jr_cond, ["NZ"]],
        0x21: [load_R_n16, [cpu.registers.hl]],
        0x22: [load_inc_mR_R2, [cpu.registers.hl, cpu.registers.a]],
        0x23: [inc_r16, [cpu.registers.hl]],
        0x24: [inc_R, [cpu.registers.h]],
        0x25: [dec_R, [cpu.registers.h]],
        0x26: [load_R_n8, [cpu.registers.h]],
        0x27: [daa],
        0x28: [jr_cond, ["Z"]],
        0x29: [add_HL_rr, [cpu.registers.hl]],
        0x2A: [load_inc_R_R2m, [cpu.registers.a, cpu.registers.hl]],
        0x2B: [dec_r16, [cpu.registers.hl]],
        0x2C: [inc_R, [cpu.registers.l]],
        0x2D: [dec_R, [cpu.registers.l]],
        0x2E: [load_R_n8, [cpu.registers.l]],
        0x2F: [cpl],
        0x30: [jr_cond, ["NC"]],
        0x31: [load_R_n16, [cpu.registers.sp]],
        0x32: [load_dec_mR_R2, [cpu.registers.hl, cpu.registers.a]],
        0x33: [inc_r16, [cpu.registers.sp]],
        0x34: [inc_HLm],
        0x35: [dec_HLm],
        0x36: [load_Rm_n8, [cpu.registers.hl]],

        0x38: [jr_cond, ["C"]],
        0x39: [add_HL_rr, [cpu.registers.sp]],
        0x3A: [load_dec_R_R2m, [cpu.registers.a, cpu.registers.hl]],
        0x3B: [dec_r16, [cpu.registers.sp]],
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
        0x80: [add_A_R, [cpu.registers.b]],
        0x81: [add_A_R, [cpu.registers.c]],
        0x82: [add_A_R, [cpu.registers.d]],
        0x83: [add_A_R, [cpu.registers.e]],
        0x84: [add_A_R, [cpu.registers.h]],
        0x85: [add_A_R, [cpu.registers.l]],
        0x86: [add_A_HLm],
        0x87: [add_A_R, [cpu.registers.a]],
        0x88: [adc_A_R, [cpu.registers.b]],
        0x89: [adc_A_R, [cpu.registers.c]],
        0x8A: [adc_A_R, [cpu.registers.d]],
        0x8B: [adc_A_R, [cpu.registers.e]],
        0x8C: [adc_A_R, [cpu.registers.h]],
        0x8D: [adc_A_R, [cpu.registers.l]],
        0x8E: [adc_A_HLm],
        0x8F: [adc_A_R, [cpu.registers.a]],
        0x90: [sub_A_R, [cpu.registers.b]],
        0x91: [sub_A_R, [cpu.registers.c]],
        0x92: [sub_A_R, [cpu.registers.d]],
        0x93: [sub_A_R, [cpu.registers.e]],
        0x94: [sub_A_R, [cpu.registers.h]],
        0x95: [sub_A_R, [cpu.registers.l]],
        0x96: [sub_A_HLm],
        0x97: [sub_A_R, [cpu.registers.a]],
        0x98: [sbc_A_R, [cpu.registers.b]],
        0x99: [sbc_A_R, [cpu.registers.c]],
        0x9A: [sbc_A_R, [cpu.registers.d]],
        0x9B: [sbc_A_R, [cpu.registers.e]],
        0x9C: [sbc_A_R, [cpu.registers.h]],
        0x9D: [sbc_A_R, [cpu.registers.l]],
        0x9E: [sbc_A_HLm],
        0x9F: [sbc_A_R, [cpu.registers.a]],
        0xA0: [and_A_R, [cpu.registers.b]],
        0xA1: [and_A_R, [cpu.registers.c]],
        0xA2: [and_A_R, [cpu.registers.d]],
        0xA3: [and_A_R, [cpu.registers.e]],
        0xA4: [and_A_R, [cpu.registers.h]],
        0xA5: [and_A_R, [cpu.registers.l]],
        0xA6: [and_A_HLm],
        0xA7: [and_A_R, [cpu.registers.a]],
        0xA8: [xor_A_R, [cpu.registers.b]],
        0xA9: [xor_A_R, [cpu.registers.c]],
        0xAA: [xor_A_R, [cpu.registers.d]],
        0xAB: [xor_A_R, [cpu.registers.e]],
        0xAC: [xor_A_R, [cpu.registers.h]],
        0xAD: [xor_A_R, [cpu.registers.l]],
        0xAE: [xor_A_HLm],
        0xAF: [xor_A_R, [cpu.registers.a]],
        0xB0: [or_A_R, [cpu.registers.b]],
        0xB1: [or_A_R, [cpu.registers.c]],
        0xB2: [or_A_R, [cpu.registers.d]],
        0xB3: [or_A_R, [cpu.registers.e]],
        0xB4: [or_A_R, [cpu.registers.h]],
        0xB5: [or_A_R, [cpu.registers.l]],
        0xB6: [or_A_HLm],
        0xB7: [or_A_R, [cpu.registers.a]],
        0xB8: [cp_A_R, [cpu.registers.b]],
        0xB9: [cp_A_R, [cpu.registers.c]],
        0xBA: [cp_A_R, [cpu.registers.d]],
        0xBB: [cp_A_R, [cpu.registers.e]],
        0xBC: [cp_A_R, [cpu.registers.h]],
        0xBD: [cp_A_R, [cpu.registers.l]],
        0xBE: [cp_A_HLm],
        0xBF: [cp_A_R, [cpu.registers.a]],
        0xC0: [ret_cond, ["NZ"]],
        0xC1: [pop_R16, [cpu.registers.bc]],
        0xC2: [jp_cond, ["NZ"]],
        0xC3: [jp_nn],
        0xC4: [call_cond, ["NZ"]],
        0xC5: [push_R16, [cpu.registers.bc]],
        0xC6: [add_A_n8],
        0xC7: [rst, [0x0]],
        0xC8: [ret_cond, ["Z"]],
        0xC9: [ret],
        0xCA: [jp_cond, ["Z"]],
        
        0xCC: [call_cond, ["Z"]],
        0xCD: [call_nn],
        0xCE: [adc_A_n8],
        0xCF: [rst, [0x08]],
        0xD0: [ret_cond, ["NC"]],
        0xD1: [pop_R16, [cpu.registers.de]],
        0xD2: [jr_cond, ["NC"]],

        0xD4: [call_cond, ["NC"]],
        0xD5: [push_R16, [cpu.registers.de]],
        0xD6: [sub_A_n8],
        0xD7: [rst, [0x10]],
        0xD8: [ret_cond, ["C"]],
        0xD9: [reti],
        0xDA: [jp_cond, ["C"]],

        0xDC: [call_cond, ["C"]],

        0xDE: [sbc_A_n8],
        0xDF: [rst, [0x18]],
        0xE0: [load_io_A],
        0xE1: [pop_R16, [cpu.registers.hl]],
        0xE2: [load_ioC_A],



        0xE5: [push_R16, [cpu.registers.hl]],
        0xE6: [and_A_n8],
        0xE7: [rst, [0x20]],

        0xE9: [jp_hl],
        0xEA: [load_n16m_R, [cpu.registers.a]],



        0xEE: [xor_A_n8],
        0xEF: [rst, [0x28]],
        0xF0: [load_A_io],
        0xF1: [pop_R16, [cpu.registers.af]],
        0xF2: [load_A_ioC],
        0xF3: [disable_interrupts],
        
        0xF5: [push_R16, [cpu.registers.af]],
        0xF6: [or_A_n8],
        0xF7: [rst, [0x30]],

        0xF9: [load_SP_HL],
        0xFA: [load_R_n16m, [cpu.registers.a]],
        0xFB: [enable_interrupts],



        0xFE: [cp_A_n8],
        0xFF: [rst, [0x38]]
    }

    mapping_prefixed = {
        0x10: [CB_rl_r, [cpu.registers.b]],
        0x11: [CB_rl_r, [cpu.registers.c]],
        0x12: [CB_rl_r, [cpu.registers.d]],
        0x13: [CB_rl_r, [cpu.registers.e]],
        0x14: [CB_rl_r, [cpu.registers.h]],
        0x15: [CB_rl_r, [cpu.registers.l]],
        0x16: [CB_rl_HLm],
        0x17: [CB_rl_r, [cpu.registers.a]],
        0x18: [CB_rr_r, [cpu.registers.b]],
        0x19: [CB_rr_r, [cpu.registers.c]],
        0x1A: [CB_rr_r, [cpu.registers.d]],
        0x1B: [CB_rr_r, [cpu.registers.e]],
        0x1C: [CB_rr_r, [cpu.registers.h]],
        0x1D: [CB_rr_r, [cpu.registers.l]],
        0x1E: [CB_rr_HLm],
        0x1F: [CB_rr_r, [cpu.registers.a]],

        0x38: [CB_srl_r, [cpu.registers.b]],
        0x39: [CB_srl_r, [cpu.registers.c]],
        0x3A: [CB_srl_r, [cpu.registers.d]],
        0x3B: [CB_srl_r, [cpu.registers.e]],
        0x3C: [CB_srl_r, [cpu.registers.h]],
        0x3D: [CB_srl_r, [cpu.registers.l]],
        0x3E: [CB_srl_HLm],
        0x3F: [CB_srl_r, [cpu.registers.a]],
    }

    def execute_from_map(opcode_map, opcode):
        args = []
        # The opcode in dict is an array. It can be of size 1 or 2. If it is of size 2, there are parameters to be used.
        if len(opcode_map[opcode]) == 2:
            args = opcode_map[opcode][1]
        # Execute the function. (It is always present in the first position of the array)
        opcode_map[opcode][0](*args)

    prefixed = False
    try:
        if opcode == 0xcb:
            prefixed = True
            opcode = cpu.read_byte_from_pc()
            execute_from_map(mapping_prefixed, opcode)
            return prefixed_opcode_cycles[opcode]
        else:
            execute_from_map(mapping, opcode)
            return opcode_cycles[opcode] if not cpu.reset_change_cycle() else opcode_cycles_changed[opcode]
    except Exception as err:
        if type(err).__name__ == 'KeyError':
            cpu.isCurrentInstructionImplemented = False
            print(f'({hex(opcode)}) {"(prefixed)" if prefixed else ""} opcode is not implemented!')
            exit(1)
        print(f'({hex(opcode)}) {"(prefixed)" if prefixed else ""} opcode error!')
        print(f'Exception type: {type(err).__name__}, message: {str(err)}')
        print(f'pc: {hex(cpu.registers.pc.get_value())}')
        print(f'sp: {hex(cpu.registers.sp.get_value())}')
        print(f'Last memory read address: {hex(cpu.mmu.last_read_address)}')
        return 0