from pathlib import Path
from struct import *
from dataclasses import dataclass, field
import json


@dataclass
class ROM:
    memory_array: bytearray = field(default_factory=list)
    cartridge_header: dict = field(default_factory=dict)

    def load_file(self, rom_path):
        p = Path(rom_path)
        self.memory_array = bytearray(p.read_bytes())
        self.__load_header()
    
    def __load_header(self):
        header = [
            (None, "="),
            (None, 'xxxx'),
            (None, '48x'),
            ('title', '15s'),
            ('CGB_flag', 'B'),
            ('new_licensee_code', '2s'),
            ('SGB_flag', 'B'),
            ('cartridge_type', 'B'),
            ('ROM_size', 'B'),
            ('RAM_size', 'B'),
            ('destination_code', 'B'),
            ('old_licensee_code', 'B'),
            ('version_number', 'B'),
            ('header_checksum', 'B'),
            ('global_checksum', 'H'),
        ]

        reader = "".join([field for _, field in header])
        header_values = unpack_from(reader, self.memory_array, 0x100)

        CARTRIDGE_HEADER = {}
        i=0
        for name, _ in header:
            if name != None:
                if name != 'title' and name != 'new_licensee_code':
                    if name == 'global_checksum':
                        CARTRIDGE_HEADER[name] = int.to_bytes(header_values[i],2,'little')
                    else:
                        CARTRIDGE_HEADER[name] = int.to_bytes(int(header_values[i]),1,'little')
                else:
                    CARTRIDGE_HEADER[name] = header_values[i]
                i+=1
        self.cartridge_header = CARTRIDGE_HEADER

    def print_memory_slice(self, start, end):
        slice = self.memory_array[start : end+1]
        hexstring_arr = []
        for i in slice:
            hexstring_arr.append(hex(i))
        print(hexstring_arr)

@dataclass
class Decoder:
    bytearray_to_decode: bytearray
    address: int=0
    regular_instructions: list = field(default_factory=list)
    prefixed_instructions: list = field(default_factory=list)

    def __post_init__(self):
        f = open('cpu_opcodes.json')
        instructions_dict = json.load(f)
        f.close()
        for i in instructions_dict['unprefixed'].values():
            self.regular_instructions.append(i)
        for i in instructions_dict['cbprefixed'].values():
            self.prefixed_instructions.append(i)

    def get_bytes(self, loc, cpu, size=1):
        data = []
        for i in range(loc, loc+size):
            data.append(cpu.mmu.read_address(i))
        return int.from_bytes(data, 'little')
    
    def decode_from(self, addr=0, cpu=None):
        if addr != 0:
            self.address = addr
        
        opcode = self.get_bytes(self.address, cpu)
        self.address += 1

        instruction = None
        if opcode == 0xcb:
            instruction = self.prefixed_instructions[self.get_bytes(self.address, cpu)]
            self.address += 1
        else:
            instruction = self.regular_instructions[opcode]
        
        operands_with_values = []
        for operand in instruction['operands']:
            if operand.get('bytes') is not None:
                value = self.get_bytes(self.address, cpu, operand.get('bytes'))
                self.address += operand.get('bytes')
                mod = dict(operand)
                mod['value'] = value
                operands_with_values.append(mod)
            else:
                operands_with_values.append(operand)
        
        mod_inst = dict(instruction)
        mod_inst['operands'] = operands_with_values
        decoded_instruction = mod_inst

        return self.address, decoded_instruction
    
    def print_instruction(self, instruction):
        operands_string = ' '
        for operand in instruction['operands']:
            if operand.get('value') is not None:
                operands_string += hex(operand['value']) + ' '
            else:
                if operand.get('immediate') == True:
                    operands_string += operand['name'] + ' '
                else:
                    operands_string +=  '(' + operand['name'] + ')' + ' '

        return instruction['mnemonic'] + operands_string