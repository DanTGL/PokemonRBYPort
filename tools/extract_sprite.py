from io import BytesIO

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

def get_bank(id):
    if id == 0x15:
        return 0x01
    elif id == 0xB6:
        return 0x0B
    elif id <= 0x1E:
        return 0x09
    elif id <= 0x49:
        return 0x0A
    elif id <= 0x73:
        return 0x0B
    elif id <= 0x98:
        return 0x0C
    else:
        return 0x0D

def get_offset(id, ptr):
    return ((get_bank(id) - 1) << 14) + ptr

def get_size(spr_dims):
    return ((spr_dims >> 4) & 0x0F), (spr_dims & 0x0F)

def print_sprite_at_addr(rom, addr, width, height):

    rom.seek(addr)

    for tile_index in range(width * height):
        value = read_bytes(rom, 2)
        bits = []

        for bit in range(8 - 1, -1, -1):
            pixel = (((value >> (bit + 8 - 1)) & 0x2) | ((value >> bit) & 0x1)) & 0x03

            bits.append(pixel)
        
        print("".join(map(lambda x: str(x) if x != 0 else ".", bits)), end="")

        if tile_index % width == width - 1:
            print()

# Not functioning properly since Pokemon sprites are compressed: https://www.youtube.com/watch?v=aF1Yw_wu2cM
def print_sprite(rom, id, ptr, spr_dims):
    offset = get_offset(id, ptr)
    width, height = get_size(spr_dims)

    rom.seek(offset)

    for tile_index in range(width * height):
        value = read_bytes(rom, 2)
        bits = []

        for bit in range(8 - 1, -1, -1):
            pixel = (((value >> (bit + 8 - 1)) & 0x2) | ((value >> bit) & 0x1)) & 0x03
            
            bits.append(pixel)
        
        print("".join(map(lambda x: str(x) if x != 0 else ".", bits)), end="")

        if tile_index % width == width - 1:
            print()

def test_print_sprite(sprite_buffer):
    for tile_index in range(1 * 8):
        value = read_bytes(sprite_buffer, 2)
        bits = []


        for bit in range(8 - 1, -1, -1):
            pixel = (((value >> (bit + 8 - 1)) & 0x2) | ((value >> bit) & 0x1)) & 0x03

            bits.append(pixel)
        
        for b in bits:
            print(str(b) if b != 0 else ".", end="")

        if tile_index % 1 == 1 - 1:
            print()


if __name__ == "__main__":
    test_print_sprite(BytesIO(b"\xFF\x00\x7E\xFF\x85\x81\x89\x83\x93\x85\xA5\x8B\xC9\x97\x7E\xFF"))
    #test_print_sprite(BytesIO(b"\x7C\x7C\x00\xC6\xC6\x00\x00\xFE\xC6\xC6\x00\xC6\xC6\x00\x00\x00"))
