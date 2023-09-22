from cpu import cpu
from cartridge import rom
from cpu.opcodes import *
from cartridge.rom import Decoder
from cpu.opcode_map import run_opcode

# GUI IMPORTS
import sys
from gui.cpu_display import QTCPUDisplay
from PyQt5 import QtWidgets

rom.load_file('test_roms/07-jr,jp,call,ret,rst.gb')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    cpu_gui = QTCPUDisplay()

def step():
    cpu.handle_interrupts()

    if cpu.halted:
        return 1

    # Decode instruction from ROM
    decoder = Decoder(rom.memory_array)
    next_addr, inst = decoder.decode_from(cpu.registers.pc.get_value())
    addr = cpu.registers.pc.get_value()
    #print(f'{hex(cpu.registers.pc.get_value())} {decoder.print_instruction(inst)}')

    opcode = cpu.read_byte_from_pc()
    cpu_gui.insert_instruction(hex(addr), decoder.print_instruction(inst), hex(opcode))
    
    # Implement and execute opcode map
    cycles = run_opcode(opcode)
    if cycles == 0: # If opcode does not exist, just increase PC without executing
        cpu.registers.pc.set_value(next_addr)
    cpu_gui.update_registers(cpu.return_registers())

cpu_gui.init_gui(cpu.return_registers(), step)
sys.exit(app.exec_())