import os
import json
import struct

FIRST_POKEMON_ENTRY = 0x0383DE

DEX_ORDER = 0x41024 # Possibly 0x41023

NUM_POKEMON = 151

pokemon = {}

# Extract pokemon data

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

with open("pokemon.gb", "rb") as file:
    file.seek(FIRST_POKEMON_ENTRY)

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

if not os.path.exists("data"):
    os.mkdir("data")

for key, value in pokemon.items():
    print(key, value, "\n")

# Output data to json file
with open("data/pokemon.json", "w") as json_file:
    json.dump(pokemon, json_file)
