from io import BytesIO
from math import ceil
from textwrap import wrap

import bitarray
from bitarray.util import pprint

POKEMON_SPRITE_MAX_BYTES = ceil(3136 / 8)

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

def rle(it, width, height):
    
    out = bitarray.bitarray()

    packet = next(it)
    print(width, height)
    try:
        while len(out) / 2 < width * height * 8:

            if True:
                bits = []

                while True:
                    if len(out) / 2 >= width * height * 8:
                        return out

                    bit = next(it)

                    bits.append(bit)

                    if bit == 0:
                        break
                
                # Code has not been tested yet
                num1 = sum((1 if bits[i] == True else 0) << i for i in range(len(bits) - 1, -1, -1))
                num2 = sum((1 if next(it) == True else 0) << i for i in range(len(bits) - 1, -1, -1))

                out.extend([False for i in range((num1 + num2 + 1) * 2)])

            while True:
                bit1 = next(it)
                bit2 = next(it)

                if bit1 == bit2 == False:
                    break

                out.extend([bit1, bit2])
    except StopIteration:
        pass

    return out

def decomp_sprite(rom, addr, dims):
    rom.seek(addr)
    
    #dims = read_bytes(rom, 1)
    width = (dims >> 4) & 0x0F
    height = dims & 0x0F

    bits = bitarray.bitarray()
    bits.fromfile(rom, POKEMON_SPRITE_MAX_BYTES)
    
    #print(bits)

    bit_iter = iter(bits)

    primary_buffer = next(bit_iter)

    #initial_packet = next(bit_iter)

    #prev_bit = initial_packet

    print("\n".join(wrap(rle(bit_iter, width, height).to01(), width=width * 4)))

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
    bit_iter = iter(bitarray.bitarray("01001101100110100011111110100011011110110101000"))
    print(rle(bit_iter, 2, 2).to01())
