from cpu import cpu
from cartridge import rom
from cpu.opcodes import *


rom.load_file('snake.gb')


# decoder = Decoder(rom.memory_array)

# temp_address = 0x100
# for i in range(200):
#     next_addr, inst = decoder.decode_from(temp_address)
#     print(f'{hex(temp_address)} {decoder.print_instruction(inst)}')
#     temp_address = next_addr