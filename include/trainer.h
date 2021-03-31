#pragma once

#include <stdint.h>

#include "pokemon.h"

#define NUM_MODS 3

extern bool moveChoices[][NUM_MODS];

void mod_1(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]);
void mod_2(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]);
void mod_3(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]);