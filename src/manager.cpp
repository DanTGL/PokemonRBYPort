#include "manager.h"
#include <time.h>

typedef enum {
    BATTLE,
    WORLD
} GameState_t;

static int timer = 0;

static char* textBuffer;

void update() {
    if (timer > 2 * 60) {
        timer--;
        return;
    }
    
}
