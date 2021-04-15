#include "pokemon.h"
#include <math.h>

Species_t pokemonSpecies[151];

uint16_t calculateStat(Pokemon_t* pokemon, uint8_t base, uint16_t ev) {
    return (uint16_t) (((base + pokemon->iv) * 2 + floor(ceil(sqrt(ev)) / 4) * pokemon->level) / 100) + 5;
}

uint16_t getHP(Pokemon_t* pokemon) {
    return calculateStat(pokemon, pokemonSpecies[pokemon->speciesIndex].baseHP, pokemon->hpEv);
}
