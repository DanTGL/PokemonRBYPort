#pragma once

#include "ai.h"
#include "player.h"
#include "pokemon.h"

void start_trainer_battle(Player_t* player, Trainer_t* trainer);

void trainer_turn(Trainer_t* trainer, Pokemon_t* opponent);
void player_turn(Player_t* player, Pokemon_t* opponent);
void wild_turn(Pokemon_t* pokemon, Pokemon_t* opponent);


