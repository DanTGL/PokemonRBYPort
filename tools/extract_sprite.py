from io import BytesIO
from math import ceil, floor
from textwrap import wrap

import bitarray
from bitarray.util import pprint

import png

POKEMON_SPRITE_MAX_BYTES = ceil(3136 / 8)

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

def delta_decode(list):
    result = []

    prev_bit = False

    for b in list:
        if b == False:
            result.append(prev_bit)
        else:
            prev_bit = not prev_bit
            result.append(prev_bit)

    return result

def rle(it, width, height):
    
    out = bitarray.bitarray()

    
    packet = next(it)
    print(width, height)
    passed_initial = False
    while len(out) < width * height * 64 - 1:

        if passed_initial or (not passed_initial and not packet):
            bits = []

            while True:
                if len(out) >= width * height * 64 - 1:
                    return out

                bit = next(it)

                bits.append(bit)

                if bit == 0:
                    break
            
            # Code has not been tested yet
            num1 = sum((1 if bits[i] == True else 0) << i for i in range(len(bits) - 1, -1, -1))
            num2 = sum((1 if next(it) == True else 0) << i for i in range(len(bits) - 1, -1, -1))

            out.extend([False for i in range((num1 + num2 + 1) * 2)])

            if not passed_initial:
                passed_initial = True

        if passed_initial or (not passed_initial and packet):
            while True:
                if len(out) >= width * height * 64 - 1:
                    return out

                bit1 = next(it)
                bit2 = next(it)

                if bit1 == bit2 == False:
                    break
                
                out.extend([bit1, bit2])
        
            if not passed_initial:
                passed_initial = True

    return out

def decomp_sprite(rom, addr, dims, id):
    #print("Address: " + str(get_bank(id) * 0x4000 + addr % 0x4000))
    
    offset = get_offset(id, addr)
    #offset = get_bank(id) * 0x4000 + addr % 0x4000
    rom.seek(offset)
    print(offset)
    
    dims = read_bytes(rom, 1)
    
    width = (dims >> 4) & 0x0F
    height = dims & 0x0F

    bits = bitarray.bitarray()
    bits.fromfile(rom, POKEMON_SPRITE_MAX_BYTES * 8)

    
    
    #print(bits.to01())

    #print(bits)

    bit_iter = iter(bits)

    primary_buffer = next(bit_iter)

    #initial_packet = next(bit_iter)

    #prev_bit = initial_packet

    #out = [][height]


    sprite_array = rle(bit_iter, width, height).tolist()
    #print(sprite_array)
    
    encoding_mode = 0
    if next(bit_iter):
        encoding_mode = 2 if next(bit_iter) else 1

    print("Primary buffer:", "1" if primary_buffer else "0")

    print("Encoding:", encoding_mode)

    #print(sprite_array)
    #print(sprite_array)

    #print(arr)

    decoded_array = [[False for i in range(height * 8)] for j in range(width * 8)]

    for i in range(0, width * height * 32):
        x = 2 * floor(i / (height * 8))
        
        y = ceil(i / 2) % (height * 8)

        decoded_array[y][x] = sprite_array[2 * i]
        decoded_array[y][x + 1] = sprite_array[(2 * i) + 1]

    #print("\n".join(["".join(map(lambda b: "1" if b else "0", y)) for y in decoded_array]))
    arr = delta_decode([item for subl in decoded_array for item in subl])

    #print(arr)
    
    split_array = [["" for i in range(height * 8)] for j in range(width * 8)]
    for x in range(width * 8):
        for y in range(height * 8):
            #print(x, y)
                #print("test")
                #split_array.append([])
                #print(len(split_array[0]))
            split_array[y][x] = "1" if arr[x + y * height * 8] == True else "0"
            #split_array[x][y + 1] = "1" if arr[y + 1 + x * height * 8] == True else "0"
    #print(split_array)
    #split_array = [ for x in range(width * 8) for y in range(height)]

    p = [(0xff, 0xff, 0xff), (0x00, 0x00, 0x00)]
    w = png.Writer(width * 8, height * 8, palette=p, bitdepth=1)
    f = open("sprite.png", "wb")
    w.write(f, [[1 if c else 0 for c in row] for row in decoded_array])
    f.close()

    print()

    #print(pixels)
    output_list = "\n".join(["".join(split_array[i]) for i in range(len(split_array))])
    #print(output_list)

    #test_print_sprite(BytesIO(bitarray.bitarray(output_list).tobytes()), width, height)

    #print("\n".join(wrap(rle(bit_iter, width, height).to01(), width=width * 4)))

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
    bank = get_bank(id)
    print(bank)
    print(ptr)
    return ((get_bank(id)) << 14) + (ptr & 0x3FFF)

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
    print("Offset: " + str(offset))
    print(width, height)

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

def test_print_sprite(sprite_buffer, width, height):
    for tile_index in range(width * height * 8):
        value = read_bytes(sprite_buffer, 2)
        bits = []


        for bit in range(8 - 1, -1, -1):
            
            #pixel = (((value >> (bit + 8 - 1)) & 0x2) | ((value >> bit) & 0x1)) & 0x03
            pixel = (value >> bit) & 0x1

            bits.append(pixel)
        
        for b in bits:
            print(str(b) if b != 0 else ".", end="")

        if tile_index % width == width - 1:
            print()


if __name__ == "__main__":
    #test_print_sprite(BytesIO(b"\xFF\x00\x7E\xFF\x85\x81\x89\x83\x93\x85\xA5\x8B\xC9\x97\x7E\xFF"), 2, 2)
    #test_print_sprite(BytesIO(b"\x7C\x7C\x00\xC6\xC6\x00\x00\xFE\xC6\xC6\x00\xC6\xC6\x00\x00\x00"), 1, 1)
    bit_iter = iter(bitarray.bitarray("01001101100110100011111110100011011110110101000"))
    print(rle(bit_iter, 2, 2).to01())
    #print(test_print_sprite(BytesIO(rle(bit_iter, 2, 2).tobytes()), 2, 2))
