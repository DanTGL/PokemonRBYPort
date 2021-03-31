#pragma once

#include <stdint.h>
#include "move.h"

enum Type : uint8_t {
    NORMAL,
    FIGHTING,
    FLYING,
    POISON,
    GROUND,
    ROCK,
    BIRD,
    BUG,
    GHOST,
    BLANK0,
    BLANK1,
    BLANk2,
    BLANK3,
    FIRE,
    WATER,
    GRASS,
    ELECTRIC,
    PSYCHIC,
    ICE,
    DRAGON
};

enum GrowthRate : uint8_t {
    MEDIUM_FAST = 0,
    MEDIUM_SLOW = 3,
    FAST = 4,
    SLOW = 5
};

enum StatusCondition : uint8_t {
    ASLEEP = 0x04,
    POISONED = 0x08,
    BURNED = 0x10,
    FROZEN = 0x20,
    PARALYZED = 0x40
};

typedef struct Species {
    uint8_t dexNumber;
    uint8_t baseHP;
    uint8_t baseAttack;
    uint8_t baseDefense;
    uint8_t baseSpeed;
    uint8_t baseSpecial;
    Type type1;
    Type type2;
    uint8_t catchRate;
    uint8_t BaseExpYield;
    uint8_t spriteDimensions;
    uint16_t fSpritePtr;
    uint16_t bSpritePtr;
    uint8_t baseMoves[MAX_MOVES];
    GrowthRate growthRate;
    uint8_t moveFlags[7];
    uint8_t padding;
} Species_t;

typedef struct Pokemon {
    uint8_t speciesIndex;
    uint16_t currentHP;
    uint8_t level;
    StatusCondition statCond;
    Type type1;
    Type type2;
    uint8_t catchRate;
    uint8_t moves[MAX_MOVES];
    uint16_t originalTrainerId;
    unsigned int expPoints : 24;
    uint16_t hpEv;
    uint16_t attackEv;
    uint16_t defenseEv;
    uint16_t speedEv;
    uint16_t specialEv;
    uint16_t iv;
    uint8_t pp[4];
    uint8_t level;
    uint16_t maxHP;
    uint16_t attack;
    uint16_t defense;
    uint16_t speed;
    uint16_t special;
} Pokemon_t;

extern Species_t pokemonSpecies[151];

uint16_t calculate_stat(Pokemon_t* pokemon, uint8_t base, uint16_t ev);
uint16_t get_hp(Pokemon_t* pokemon);
