#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

struct ParserContext {
    char *action;
    char *validatedTokens;
    bool *err;
};

bool isActionLegit(const char *, const int);
bool isLoki(const char *);
bool computeTokens(const char cmd[], const char *, struct ParserContext *);
bool startFlagBasedTokenReaper(const char cmd[], struct ParserContext *);
bool startSimpleTokenReaper(char *cmd[], struct ParserContext *);

static char *actions[] = {
    "run", "exec", "create", "build",
    "start", "stop", "rm", "ps", "images",
};

bool parseCommands(const char cmd[], const int argc) {
    struct ParserContext *ctx;
    if (argc < 2) 
        return false;

    for (int i = 0; i < argc; i++) {
        if (!isLoki(&cmd[0]))
            return false;

        if (!isActionLegit(&cmd[1], argc))
            return false;

        ctx = (struct ParserContext *) malloc(sizeof(struct ParserContext));
        strcpy(&cmd[1], ctx->action);

        computeTokens(cmd, &cmd[1], ctx);

    }

    return false;
}

bool isLoki(const char *cmd) {
    return strcmp(cmd, "loki");
}

// this function is responsible of checking the
// presence of the main commands supported by Loki
// in the command line string given by the user.
bool isActionLegit(const char *cmd, const int len) {
    for (int i = 0; i < len; i++) {
        if (strcmp(cmd, actions[i])) 
            return true;
    }

    return false;
}


bool computeTokens(const char cmds[], const char *action, struct ParserContext *ctx) {
    if (strcmp(action, "run") || strcmp(action, "create")) {
        return startFlagBasedTokenReaper(cmds, ctx);
    }

    if (strcmp(action, "start") 
            || strcmp(action, "stop") 
            || strcmp(action, "rm")) {
        return startSimpleTokenReaper(cmds, ctx);
    }
    return true;
}

bool startFlagBasedTokenReaper(const char cmds[], struct ParserContext *ctx) {
    return false;
}

bool startSimpleTokenReaper(char *cmds[], struct ParserContext *ctx) {
    if (cmds[2] == NULL) {
        return false;
    }
    strcpy(cmds[2], ctx->validatedTokens);
    return true;
}
