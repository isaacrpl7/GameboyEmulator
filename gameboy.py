from cpu import cpu
from cartridge import rom
from cpu.opcodes import *
from cartridge.rom import Decoder
from cpu.opcode_map import run_opcode

# GUI IMPORTS
from gui.cpu_display import DisplayCPU

rom.load_file('snake.gb')

cpu_gui = DisplayCPU()
def step():
    # Decode instruction from ROM
    decoder = Decoder(rom.memory_array)
    next_addr, inst = decoder.decode_from(cpu.registers.pc.get_value())
    print(f'{hex(cpu.registers.pc.get_value())} {decoder.print_instruction(inst)}')

    opcode = cpu.read_byte_from_pc()
    print(opcode)
    # Implement and execute opcode map
    error = run_opcode(opcode)
    if error == -1: # If opcode does not exist, just increase PC without executing
        cpu.registers.pc.set_value(next_addr)
    cpu_gui.update(cpu.return_registers())

cpu_gui.init_gui(cpu.return_registers(), step)
