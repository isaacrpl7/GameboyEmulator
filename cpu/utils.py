def compose_bytes(high_signf, low_signf):
    return (high_signf << 8) | low_signf

def decompose_bytes(bytes):
    return bytes >> 8, bytes & 0xFF

def set_bit(byte, bit_position, value):
    if not value:
        return byte & (0xFE << bit_position)
    else:
        return byte | (0x01 << bit_position)