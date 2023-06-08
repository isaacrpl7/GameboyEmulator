from cpu.opcodes import *
from cpu import cpu

def run_opcode(opcode: int):
    mapping = {
        0x00: [nop],
        0x01: [load_R_n16, [cpu.registers.bc]]

    }
    args = []
    try:
        if len(mapping[opcode]) == 2:
            args = mapping[opcode][1]
        mapping[opcode][0](*args)
    except:
        return -1