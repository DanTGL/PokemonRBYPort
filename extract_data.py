import os
import json
import struct

from tools.extract_sprite import *

FIRST_POKEMON_ENTRY = 0x0383DE

DEX_ORDER_ADDRESS = 0x41024 # Possibly 0x41023
MAX_INDEX = 0xBE

NUM_POKEMON = 151

pokemon = {}

dex_order = [0]

# Extract pokemon data

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

with open("pokemon.gb", "rb") as file:
    file.seek(DEX_ORDER_ADDRESS)
    for i in range(MAX_INDEX):
        dex_num = read_bytes(file, 1)

        dex_order.append(dex_num)

    file.seek(FIRST_POKEMON_ENTRY)

    printed_sprite = False

    for i in range(NUM_POKEMON):
        dex_num = struct.unpack("B", file.read(1))[0]
        pokemon[dex_num] = {}
        pokemon[dex_num]["BaseHP"] = read_bytes(file, 1)
        pokemon[dex_num]["BaseAttack"] = read_bytes(file, 1)
        pokemon[dex_num]["BaseDefense"] = read_bytes(file, 1)
        pokemon[dex_num]["BaseSpeed"] = read_bytes(file, 1)
        pokemon[dex_num]["BaseSpecial"] = read_bytes(file, 1)
        pokemon[dex_num]["Type1"] = read_bytes(file, 1)
        pokemon[dex_num]["Type2"] = read_bytes(file, 1)
        pokemon[dex_num]["CatchRate"] = read_bytes(file, 1)
        pokemon[dex_num]["BaseExpYield"] = read_bytes(file, 1)

        pokemon[dex_num]["SpriteDims"] = read_bytes(file, 1)
        pokemon[dex_num]["fSpritePtr"] = read_bytes(file, 2)
        pokemon[dex_num]["bSpritePtr"] = read_bytes(file, 2)

        # Read all four moves
        pokemon[dex_num]["Lvl1Attacks"] = [read_bytes(file, 1) for i in range(4)]
        pokemon[dex_num]["GrowthRate"] = read_bytes(file, 1)
        pokemon[dex_num]["MoveFlags"] = read_bytes(file, 7)

        # Read and discard padding
        file.read(1)

        # Only print out sprite once as a test
        # This will be removed in the future
        if not printed_sprite:
            cur_off = file.tell()
            rom = decomp_sprite(file, pokemon[dex_num]["fSpritePtr"], pokemon[dex_num]["SpriteDims"])
            #print_sprite(file, dex_order.index(dex_num), pokemon[dex_num]["fSpritePtr"], pokemon[dex_num]["SpriteDims"])
            file.seek(cur_off)
            
            printed_sprite = True

if not os.path.exists("data"):
    os.mkdir("data")

#print(str(dex_order))

#for key, value in pokemon.items():
#    print(key, value, "\n")

# Output data to json file
with open("data/pokemon.json", "w") as json_file:
    json.dump(pokemon, json_file)
