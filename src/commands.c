#include <string.h>
#include "commands.h"
#include "handlers.h"

#define LIST_ELEMS 9

static struct cmd *commandList[] = {
    {"run", cmdRun},
    {"exec", cmdExec},
    {"build", cmdBuild},
    {"create", cmdCreate},
    {"start", cmdStart},
    {"stop", cmdStop},
    {"rm", cmdRm},
    {"ps", cmdPs},
    {"images", cmdImages},
};

callback fetchCommandHandler(const char *command) {
    for (int i = 0; i < LIST_ELEMS; i++) {
        struct cmd pair = commandList[i];
        if (strcmp(command, pair.command)) 
            return pair.handler;
    }
    return NULL;
}
