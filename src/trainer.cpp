#include "include/trainer.h"

#include "include/move.h"
#include <stdlib.h>

int8_t statusMoveEffects[];

bool moveChoices[][NUM_MODS];

void (*modifications[NUM_MODS])(Pokemon_t*, Pokemon_t*, uint8_t[4]) = {
    mod_1,
    mod_2,
    mod_3
};

void mod_1(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]) {
    if (opponent->statCond == 0x00) return;
    
    uint8_t i = 0;
    while (statusMoveEffects[i] != -1) {
        for (uint8_t moveIndex = 0; moveIndex < MAX_MOVES; moveIndex++) {
            uint8_t move = pokemon->moves[moveIndex];
            if (move == 0) continue;

            if (moves[move].effect == statusMoveEffects[i])
                priorityArray[moveIndex] += 5;

        }
        
        i++;
    }

}

void mod_2(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]) {
    // TODO: Implement modification 2
}

void mod_3(Pokemon_t* pokemon, Pokemon_t* opponent, uint8_t priorityArray[4]) {
    for (uint8_t moveIndex = 0; moveIndex < MAX_MOVES; moveIndex++) {
        uint8_t move = pokemon->moves[moveIndex];
        if (move == 0) continue;
        
        priorityArray[moveIndex] += is_super_effective(moves[move], opponent) ? 1 : -1;
    }
}

uint8_t random_move() {
    uint8_t x = rand() % 256;

    if (x < 0x3f) return 0;
    else if (x < 0x7f) return 1;
    else if (x < 0xbe) return 2;
    else return 3;
}

void choose_move(uint8_t trainerIndex, Pokemon_t* pokemon, Pokemon_t* opponent) {
    uint8_t priority[MAX_MOVES] = {10, 10, 10, 10};
    

    for (uint8_t i = 0; i < NUM_MODS; i++) {
        if (moveChoices[trainerIndex][i]) {
            modifications[i](pokemon, opponent, priority);
        }
    }

    uint8_t min_priority;

    for (uint8_t i = 0; i < MAX_MOVES; i++) {
        if (pokemon->moves[i] == 0) continue;
        
        if (min_priority == NULL || min_priority > priority[i]) {
            min_priority = priority[i];
        }
    }

    uint8_t chosenMove;

    do {
        chosenMove = random_move();
    } while (priority[chosenMove] > min_priority);

}