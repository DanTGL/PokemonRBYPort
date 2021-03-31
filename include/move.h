#pragma once

#include <stdint.h>

#include "pokemon.h"

#define MAX_MOVES 4

typedef struct Move {
    uint8_t animation;
    uint8_t effect;
    uint8_t power;
    uint8_t type;
    uint8_t accuracy;
} Move_t;

bool is_super_effective(Move_t move, Pokemon_t* opponent);

extern Move_t moves[];
