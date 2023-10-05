from cpu.registers import CPURegisters
from cpu.registers import Register, RegisterPair
from cpu.serial import Serial
from cpu.mmu import MMU
from cpu.io import IO
from cpu.utils import compose_bytes, get_bit, set_bit

class CPU:
    
    def __init__(self):
        self.registers = CPURegisters(cpu=self)
        self.change_cycle = False

        # Interrupts
        self.interrupts = {
            'vblank': 0x40,
            'lcdc_status': 0x48,
            'timer': 0x50,
            'serial': 0x58,
            'joypad': 0x60
        }
        self.interrupt_flag = Register(0x0)
        self.interrupt_enabled = Register(0x0)
        self.interrupt_master_enabled = False
        self.halted = False

        # Serial port
        self.serial = Serial()

        self.mmu = MMU(cpu=self)
        self.io = IO(cpu=self)

        # Debug
        self.isCurrentInstructionImplemented = True
    
    def read_byte_from_pc(self):
        content = self.mmu.read_address(self.registers.pc.get_value())
        self.registers.pc.increment()
        return content
    
    def read_word_from_pc(self):
        """ word == 2 bytes """
        lsb = self.read_byte_from_pc()
        msb = self.read_byte_from_pc()
        return compose_bytes(msb, lsb)

    def set_change_cycle(self, value):
        self.change_cycle = value
    
    def reset_change_cycle(self):
        has_cycle_change = self.change_cycle
        self.change_cycle = False
        return has_cycle_change

    def check_condition(self, condition):
        condition_valuation = False
        match condition:
            case "C": # Condition is to have the carry flag active
                condition_valuation = self.registers.f.get_flag_carry()
            case "NC": # Condition is to have the carry flag set 0
                condition_valuation = not self.registers.f.get_flag_carry()
            case "Z": # Condition is to have the zero flag set 1
                condition_valuation = self.registers.f.get_flag_zero()
            case "NZ": # Condition is to have the zero flag set 0
                condition_valuation = not self.registers.f.get_flag_zero()
        if condition_valuation:
            self.set_change_cycle(True)
        return condition_valuation
    
    def stack_push(self, register: RegisterPair):
        self.registers.sp.decrement()
        self.mmu.write_address(self.registers.sp.get_value(),register.get_msb())
        self.registers.sp.decrement()
        self.mmu.write_address(self.registers.sp.get_value(),register.get_lsb())
    
    def stack_pop(self, register: RegisterPair):
        low_signf = self.mmu.read_address(self.registers.sp.get_value())
        self.registers.sp.increment()
        high_signif = self.mmu.read_address(self.registers.sp.get_value())
        self.registers.sp.increment()

        value = compose_bytes(high_signif, low_signf)
        register.set_value(value)

    def handle_interrupts(self):
        """ Functions like a call instruction. Push PC to stack, see the allowed interruptions in priority order, change PC to the respective interrupt address, 
        and then set low the bit of the interruption flag """
        if self.interrupt_master_enabled:
            allowed_interrupts = self.interrupt_flag & self.interrupt_enabled

            if allowed_interrupts == 0x0: # If there's no interrupt, just return
                return
            
            self.halted = False
            self.stack_push(self.registers.pc)

            if self.handle_interrupt('vblank', allowed_interrupts, 0):
                return
            if self.handle_interrupt('lcdc_status', allowed_interrupts, 1):
                return
            if self.handle_interrupt('timer', allowed_interrupts, 2):
                return
            if self.handle_interrupt('serial', allowed_interrupts, 3):
                return
            if self.handle_interrupt('joypad', allowed_interrupts, 4):
                return
            
    def handle_interrupt(self, type, allowed_interrupts, bit_position):
        if not get_bit(allowed_interrupts, bit_position):
            return False
        
        self.interrupt_flag = set_bit(self.interrupt_flag, bit_position, 0)
        self.registers.pc.set_value(self.interrupts.get(type))
        self.interrupt_master_enabled = False
        return True

    # Debug purposes
    def return_registers(self):
        return {
            'A': hex(self.registers.a.get_value()),
            'B': hex(self.registers.b.get_value()),
            'C': hex(self.registers.c.get_value()),
            'D': hex(self.registers.d.get_value()),
            'E': hex(self.registers.e.get_value()),
            'H': hex(self.registers.h.get_value()),
            'L': hex(self.registers.l.get_value()),
            'Z': hex(self.registers.f.get_flag_zero()),
            'S': hex(self.registers.f.get_flag_subtract()),
            'HC': hex(self.registers.f.get_flag_half_carry()),
            'CR': hex(self.registers.f.get_flag_carry()),
            'SP': hex(self.registers.sp.get_value()),
            'PC': hex(self.registers.pc.get_value())
        }
    
    def checkCurrentInstructionImplemented(self):
        if self.isCurrentInstructionImplemented:
            return True
        else:
            self.isCurrentInstructionImplemented = True
            return False
