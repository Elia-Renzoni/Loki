#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include "handlers.h"

bool isActionLegit(const char *);
bool isLoki(const char *);
struct ParserContext *startParsing(struct LexerContext *);
struct ParserContext *fillContext(void *, void *);

static char *actions[] = {
    "run", "exec", "create", "build",
    "start", "stop", "rm", "ps", "images",
};

struct ParserContext *parseCommands(char cmd[], const int argc) {
    struct LexerContext *ctx;
    if (argc < 2) return NULL;

    if (!isLoki(&cmd[1])) return NULL;

    if (!isActionLegit(&cmd[2])) return NULL;

    ctx = (struct LexerContext *) malloc(sizeof(struct LexerContext));
    strcpy(&cmd[1], ctx->action);
    
    for (int i = 2; i < argc; i++) strcpy(&cmd[i], ctx->validatedTokens);

    return startParsing(ctx);
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

struct ParserContext *startParsing(struct LexerContext *ctx) {
    if (ctx->err) return fillContext(ctx->err, NULL);

    if (strcmp(ctx->action, "ps")) {
    }
    if (strcmp(ctx->action, "images")) {
    }
    if (strcmp(ctx->action, "build")) {
    }
    if (strcmp(ctx->action, "start") || strcmp(ctx->action, "stop") || strcmp(ctx->action, "rm")) {
    }

    return NULL;
}

struct ParserContext *fillContext(void *errParam, void *actionBuilder) {
    struct ParserContext *ctx = (struct ParserContext *) malloc(sizeof(struct ParserContext));
    ctx->err = (bool *) errParam;

    return ctx;
}


