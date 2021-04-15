#include "move.h"

bool is_super_effective(Move_t move, Pokemon_t* opponent) {
    return true;
}

float get_effectiveness(Move_t move, Pokemon_t* opponent) {
    // TODO: Implement effectiveness check
    return 1;
}

uint16_t calculate_damage(Move_t move, Pokemon_t* pokemon, Pokemon_t* opponent) {
    return (uint16_t) ((((2 * pokemon->level) / 5 + 2) * move.power * (pokemon->attack / opponent->defense) / 50 + 2) * get_effectiveness(move, opponent));
}
