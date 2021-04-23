#include "manager.h"
#include <time.h>

void update(GameState_t* gameState) {
    if (gameState->delayFrames > 0) {
        return;
    }
    
}

void render(GameState_t* gameState) {
    if (gameState->delayFrames > 0) {
        gameState->delayFrames--;
    }
}
