from text_utils import *
import json

FIRST_MOVE_NAME = "POUND"

NUM_MOVES = 165

FIRST_MOVE_ENTRY = b"\x01\x00\x28\x00\xFF\x23"

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

def find_name_offset(rom):
    return rom.find(text_encode(FIRST_MOVE_NAME))

def extract_names(rom):
    rom.seek(find_name_offset(rom.read()))

    names = []

    for i in range(NUM_MOVES):
        characters = []

        while True:
            c = read_bytes(rom, 1)
            
            if c == 0x50:
                break
                
            characters.append(text_decode([c]))
        
        names.append("".join(characters))
    
    return names

def extract_moves(rom, names):
    moves = []

    rom.seek(0)
    rom.seek(rom.read().find(FIRST_MOVE_ENTRY))

    for i in range(NUM_MOVES):
        id = read_bytes(rom, 1)

        moves.append(dict())
        moves[i]["id"] = id
        moves[i]["name"] = names[i]
        moves[i]["effect"] = read_bytes(rom, 1)
        moves[i]["power"] = read_bytes(rom, 1)
        moves[i]["type"] = read_bytes(rom, 1)
        moves[i]["accuracy"] = read_bytes(rom, 1)
        moves[i]["pp"] = read_bytes(rom, 1)
    
    return moves

if __name__ == "__main__":
    with open("pokemon.gb", "rb") as f:
        moves = extract_moves(f, extract_names(f))

        json_file = open("data/moves.json", "w")

        json.dump(moves, json_file)

        json_file.close()


