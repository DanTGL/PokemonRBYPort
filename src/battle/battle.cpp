#include "battle/battle.h"

#include <stdlib.h>

uint8_t cur_pokemon_player;
uint8_t cur_pokemon_trainer;

void use_move(uint8_t moveIndex, Pokemon_t* pokemon, Pokemon_t* opponent) {
    Move move = moves[moveIndex];

    uint8_t x = rand() % 256;
    if (x < move.accuracy) {
        // Move hit
        
    } else {
        // Move missed
    }
}

void start_trainer_battle(Player_t* player, Trainer_t* trainer) {
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
    use_move(move, trainerPokemon, playerPokemon);
}

void player_turn(Player_t* player, Pokemon_t* opponent) {

}

void wild_turn(Pokemon_t* pokemon, Player_t* player) {
    use_move(wild_choose_move(pokemon), pokemon, &player->pokemon[cur_pokemon_player]);
}
