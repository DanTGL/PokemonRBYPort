#include "battle/battle.h"

#include <stdlib.h>

// TODO: Replace with struct and make start_battle return it to avoid using global variables
uint8_t cur_pokemon_player;
uint8_t cur_pokemon_trainer;
uint8_t player_chosen_move = -1;

enum MoveResult : uint8_t {
    MISSED = 0,
    HIT = 1,
    DEFEATED = 2
};

MoveResult use_move(uint8_t moveIndex, Pokemon_t* pokemon, Pokemon_t* opponent) {
    Move move = moves[moveIndex];

    uint8_t x = rand() % 256;
    if (x < move.accuracy) {
        // Move hit
        uint16_t damage = calculate_damage(move, pokemon, opponent);
        if (damage >= opponent->currentHP) {
            return DEFEATED;
        } else {
            opponent->currentHP -= damage;
            return HIT;
        }
    } else {
        // Move missed
        return MISSED;
    }
}

void start_battle(Player_t* player, Trainer_t* trainer) {
    for (uint8_t i = 0; i < 6; i++) {
        if (player->pokemon[i].currentHP != 0) {
            cur_pokemon_player = i;
            break;
        }
    }

    cur_pokemon_trainer = 0;

    // TODO: Initialize trainer
}

void trainer_turn(Trainer_t* trainer, Player_t* player) {
    Pokemon_t* trainerPokemon = &trainer->pokemon[cur_pokemon_trainer];
    Pokemon_t* playerPokemon = &trainer->pokemon[cur_pokemon_player];

    uint8_t move = choose_move(trainer->id, trainerPokemon, playerPokemon);
    MoveResult moveResult = use_move(move, trainerPokemon, playerPokemon);

    switch (moveResult) {
        case MISSED:
            break;
        case HIT:
            break;
        case DEFEATED:
            defeated_pokemon(player);
            break;
    }
}

bool defeated_pokemon(Player_t* player) {
    for (int i = 0; i < 6; i++) {
        Pokemon_t* pokemon = &player->pokemon[i];
        if (pokemon != NULL) {
            if (pokemon->currentHP > 0) {
                cur_pokemon_player = i;
                return false;
            }
        }
    }

    return true;
}

// Returns true if the trainer has no more pokemon left
bool defeated_pokemon(Trainer_t* trainer) {
    for (int i = 0; i < 6; i++) {
        Pokemon_t* pokemon = &trainer->pokemon[i];
        if (pokemon != NULL) {
            if (pokemon->currentHP > 0) {
                cur_pokemon_trainer = i;
                return false;
            }
        }
    }

    return true;
}

bool defeated_pokemon(Pokemon_t* pokemon) {
    return true;
}

void player_turn(Player_t* player, Pokemon_t* opponent) {
    if (chosen_move != -1) {
        
    }
}

void wild_turn(Pokemon_t* pokemon, Player_t* player) {
    use_move(wild_choose_move(pokemon), pokemon, &player->pokemon[cur_pokemon_player]);
}
