from cpu.utils import address_in_range
from cartridge.rom import ROM

class Cartridge:
    def __init__(self, rom: ROM):
        self.rom = rom
        self.ram = bytearray(8192) # 8KiB RAM (32 KiB is only available in cartridges with ROM <= 512 KiB (TODO))
        self.ram_enabled = False
    
    def write(self, address, byte):
        pass

    def read(self, address):
        pass

class MBC1(Cartridge):

    def __init__(self, rom: ROM):
        super().__init__(rom)
        self.rom = rom
        self.rom_bank = 0x1
        self.ram_bank = 0x0
    
    def write(self, address, byte):
        #  RAM Enable
        if address_in_range(address, 0x0000, 0x1FFFF):
            if (byte & 0x0F) == 0x0A:
                self.ram_enabled = True
            else:
                self.ram_enabled = False
        
        # ROM Bank Number
        if address_in_range(address, 0x2000, 0x3FFF):
            if byte == 0x0:
                self.rom_bank = 0x1

            if byte == 0x20:
                self.rom_bank = 0x21
                return
            if byte == 0x40:
                self.rom_bank = 0x41
                return
            if byte == 0x60:
                self.rom_bank = 0x61
                return

            rom_bank_bits = byte & 0x1F;
            self.rom_bank = rom_bank_bits
        
        if address_in_range(address, 0x6000, 0x7FFF):
            print('TODO, set upper bits of ROM bank number')

        if address_in_range(address, 0x6000, 0x7FFF):
            print('TODO, Banking mode select')
        
        # Writing in RAM
        if address_in_range(address, 0xA000, 0xBFFF):
            if not self.ram_enabled:
                return
            
            offset_ram = 0x2000 * self.ram_bank
            ram_address = (address - 0xA000) + offset_ram
            self.ram[ram_address] = byte

    def read(self, address):
        if address_in_range(address, 0x0000, 0x3FFF):
            return self.rom.memory_array[address]
        
        if address_in_range(address, 0x4000, 0x7FFF):
            address_inside_bank = address - 0x4000
            bank_offset = 0x4000 * self.rom_bank
            address_inside_rom = address_inside_bank + bank_offset
            return self.rom.memory_array[address_inside_rom]

        if address_in_range(address, 0xA000, 0xBFFF):
            offset_ram = 0x2000 * self.ram_bank
            ram_address = (address - 0xA000) + offset_ram
            return self.ram[ram_address]
        
        raise IndexError('Attemped to read a MBC1 address that is unmapped: ' + hex(address))
    
    
class CartridgeController:
    def __init__(self, cartridge:Cartridge=None):
        self.cartridge = cartridge

    def load_cartridge_type_from_rom(self, rom: ROM):
        if rom.cartridge_header['cartridge_type'][0] == 0x01:
            self.cartridge = MBC1(rom)
            print('Using MBC1')
        else:
            raise SystemError('This type of cartridge is not implemented!')