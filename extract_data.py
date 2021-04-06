import json

FIRST_POKEMON_ENTRY = 0x0383DE

NUM_POKEMON = 151

pokemon = {}

# Extract pokemon data

with open("pokemon.rom", "rb") as file:
    file.seek(FIRST_POKEMON_ENTRY)

    for i in range(NUM_POKEMON):
        dex_num = file.read(1)
        pokemon[dex_num] = {}
        pokemon[dex_num]["BaseHP"] = file.read(1)
        pokemon[dex_num]["BaseAttack"] = file.read(1)
        pokemon[dex_num]["BaseDefense"] = file.read(1)
        pokemon[dex_num]["BaseSpeed"] = file.read(1)
        pokemon[dex_num]["BaseSpecial"] = file.read(1)
        pokemon[dex_num]["Type1"] = file.read(1)
        pokemon[dex_num]["Type2"] = file.read(1)
        pokemon[dex_num]["CatchRate"] = file.read(1)
        pokemon[dex_num]["BaseExpYield"] = file.read(1)

        pokemon[dex_num]["SpriteDims"] = file.read(1)
        pokemon[dex_num]["fSpritePtr"] = file.read(2)
        pokemon[dex_num]["bSpritePtr"] = file.read(2)

        # Read all four moves
        pokemon[dex_num]["Lvl1Attacks"] = [file.read(1) for i in range(4)]
        pokemon[dex_num]["GrowthRate"] = file.read(1)
        pokemon[dex_num]["MoveFlags"] = file.read(7)
        
        # Read and discard padding
        file.read(1)

# Output data to json file
with open("data/pokemon.json", "w") as json_file:
    json.dump(pokemon, json_file)
