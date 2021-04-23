#pragma once
#include <stdint.h>

typedef enum {
    BATTLE,
    WORLD
} StateEnum_t;

typedef struct {
    StateEnum_t type;
    uint8_t delayFrames = 0;
} GameState_t;

void update(GameState_t* gameState);
void render(GameState_t* gameState);
