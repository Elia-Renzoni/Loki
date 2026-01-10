#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

struct ParserContext {
    char *action;
    char *validatedTokens;
    bool *err;
};

bool isActionLegit(const char *);
bool isLoki(const char *);

static char *actions[] = {
    "run", "exec", "create", "build",
    "start", "stop", "rm", "ps", "images",
};

static char *tokens[] = {};

bool parseCommands(char cmd[], const int argc) {
    struct ParserContext *ctx;
    if (argc < 2) return false;

    if (!isLoki(&cmd[1])) return false;

    if (!isActionLegit(&cmd[2])) return false;

    ctx = (struct ParserContext *) malloc(sizeof(struct ParserContext));
    strcpy(&cmd[1], ctx->action);
    
    for (int i = 2; i < argc; i++) {
        strcpy(&cmd[i], ctx->validatedTokens);
    }

    return false;
}

bool isLoki(const char *cmd) {
    return strcmp(cmd, "loki");
}

// this function is responsible of checking the
// presence of the main commands supported by Loki
// in the command line string given by the user.
bool isActionLegit(const char *cmd) {
    for (int i = 0; i < strlen(actions); i++) {
        if (strcmp(cmd, actions[i])) 
            return true;
    }

    return false;
}
