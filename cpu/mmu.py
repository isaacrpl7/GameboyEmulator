from cartridge import cartridge_controller
from cpu.utils import address_in_range
"""
    Start	End	    Description	                    Notes
    0000	3FFF	16 KiB ROM bank 00	            From cartridge, usually a fixed bank
    4000	7FFF	16 KiB ROM Bank 01~NN	        From cartridge, switchable bank via mapper (if any)
    8000	9FFF	8 KiB Video RAM (VRAM)	        In CGB mode, switchable bank 0/1
    A000	BFFF	8 KiB External RAM	            From cartridge, switchable bank if any
    C000	CFFF	4 KiB Work RAM (WRAM)	
    D000	DFFF	4 KiB Work RAM (WRAM)	        In CGB mode, switchable bank 1~7
    E000	FDFF	Mirror of C000~DDFF (ECHO RAM)	Nintendo says use of this area is prohibited.
    FE00	FE9F	Sprite attribute table (OAM)	
    FEA0	FEFF	Not Usable	                    Nintendo says use of this area is prohibited
    FF00	FF7F	I/O Registers	
    FF80	FFFE	High RAM (HRAM)	
    FFFF	FFFF	Interrupt Enable register (IE)	
"""
ranges = {
    'ROM_BANK_00': [0x0, 0x3FFF],
    'ROM_BANK_NN': [0x4000, 0x7FFF],
    'VRAM': [0x8000, 0x9FFF],
    'EXT_RAM': [0xA000, 0xBFFF],
    'WORK_RAM1': [0xC000, 0xCFFF],
    'WORK_RAM2': [0xD000, 0xDFFF],
    'PROHIBITED1': [0xE000, 0xFDFF],
    'OAM': [0xFE00, 0xFE9F],
    'PROHIBITED2': [0xFEA0, 0xFEFF],
    'IO_REGISTERS': [0xFF00, 0xFF7F],
    'HRAM': [0xFF80, 0xFFFE],
    'IE': [0xFFFF, 0xFFFF],
}
class MMU:
    def __init__(self, cpu):
        self.cpu = cpu
        self.work_ram = bytearray(0x8000)
        self.high_ram = bytearray(0x80)

        self.last_read_address = 0x00 # Debug purposes

    # return the range the address is in
    def address_range(self, address):
        if not address_in_range(address, 0, 0xFFFF):
            raise ValueError('Address is out of range')
        for range in ranges.keys():
            if address_in_range(address, ranges[range][0], ranges[range][1]):
                return range
        
    def read_address(self, address):
        # print(f'Reading address: {hex(address)}')
        self.last_read_address = address

        if self.address_range(address) == 'PROHIBITED1':
            raise ValueError('You cannot access this area of memory')
        
        if self.address_range(address) == 'PROHIBITED2':
            raise ValueError('You cannot access this area of memory')
        
        if self.address_range(address) == 'ROM_BANK_00' or self.address_range(address) == 'ROM_BANK_NN':
            return cartridge_controller.cartridge.read(address)
        
        if self.address_range(address) == 'EXT_RAM':
            return cartridge_controller.cartridge.read(address)

        if self.address_range(address) == 'IO_REGISTERS':
            return self.cpu.io.read_io(address)
        
        if self.address_range(address) == 'WORK_RAM1' or self.address_range(address) == 'WORK_RAM2':
            return self.work_ram[(address - 0xC000)]
        
        if self.address_range(address) == 'HRAM':
            return self.high_ram[(address - 0xFF80)]
        
        if self.address_range(address) == 'IE':
            return self.cpu.interrupt_enabled.get_value()

    def write_address(self, address, byte):
        # print(f'Writing in address: {hex(address)}, byte: {hex(byte)}')
        self.last_read_address = address

        if self.address_range(address) == 'ROM_BANK_00' or self.address_range(address) == 'ROM_BANK_NN':
            cartridge_controller.cartridge.write(address, byte)
        
        if self.address_range(address) == 'EXT_RAM':
            cartridge_controller.cartridge.read(address, byte)

        if self.address_range(address) == 'IO_REGISTERS':
            self.cpu.io.write_io(address, byte)
        
        if self.address_range(address) == 'WORK_RAM1' or self.address_range(address) == 'WORK_RAM2':
            self.work_ram[(address - 0xC000)] = byte
        
        if self.address_range(address) == 'HRAM':
            self.high_ram[(address - 0xFF80)] = byte
        
        if self.address_range(address) == 'IE':
            self.cpu.interrupt_enabled.set_value(byte)