from text_utils import *

FIRST_MOVE_NAME = "POUND"

NUM_MOVES = 165

def read_bytes(file, size):
    return int.from_bytes(file.read(size), byteorder="little")

def find_name_offset(rom):
    return rom.find(text_encode(FIRST_MOVE_NAME))

def extract_names(rom):
    rom.seek(find_name_offset(rom.read()))

    moves = []

    for i in range(NUM_MOVES):
        characters = []

        while True:
            c = read_bytes(rom, 1)
            
            if c == 0x50:
                break
                
            characters.append(text_decode([c]))
        
        moves.append("".join(characters))
    
    print("\n".join(moves))

if __name__ == "__main__":
    with open("pokemon.gb", "rb") as f:
        extract_names(f)
