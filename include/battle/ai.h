#pragma once

#include <stdint.h>

#include "pokemon.h"

#define NUM_MODS 3

typedef struct {
    uint8_t id; // Will remove this later
    Pokemon_t pokemon[6];
} Trainer_t;

extern bool moveChoices[][NUM_MODS];

void mod_1(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]);
void mod_2(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]);
void mod_3(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]);

uint8_t choose_move(uint8_t trainerIndex, Pokemon_t* pokemon, Pokemon_t* opponent);

uint8_t wild_choose_move(Pokemon_t* pokemon);