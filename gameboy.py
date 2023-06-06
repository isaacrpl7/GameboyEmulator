from cpu import cpu
from cartridge import rom
from cpu.opcodes import *


rom.load_file('snake.gb')
cpu.print_registers()
load_R_n8(cpu.registers.a)
#load_R_n8(cpu.registers.a)
load_R_n8(cpu.registers.b)
push_R16(cpu.registers.bc)
cpu.print_registers()
add_A_R(cpu.registers.c)
cpu.print_registers()
sub_R(cpu.registers.b)
cpu.print_registers()

# decoder = Decoder(rom.memory_array)

# temp_address = 0x100
# for i in range(200):
#     next_addr, inst = decoder.decode_from(temp_address)
#     print(f'{hex(temp_address)} {decoder.print_instruction(inst)}')
#     temp_address = next_addr