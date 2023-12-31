def compose_bytes(high_signf, low_signf):
    return (high_signf << 8) | low_signf

def decompose_bytes(bytes):
    return bytes >> 8, bytes & 0xFF

def set_bit(byte, bit_position, value):
    """ Set a bit in a byte to a value at bit_position (the 0 position is the right-most bit) """
    if not value:
        return byte & ((0x01 << bit_position) ^ 0xFF)
    else:
        return byte | (0x01 << bit_position)

def get_bit(byte, bit_position):
    """ Return a bit of a byte at bit_position (the 0 position is the right-most bit) """
    return (byte & (0x01 << bit_position)) >> bit_position

def address_in_range(address, lower, upper):
    if address >= lower and address <= upper:
        return True
    else:
        return False