#include "handlers.h"

struct LexerContext {
    char *action;
    char *validatedTokens;
    bool *err;
};

struct ParserContext {
    bool *err;
    union Action {
        Image image;
        Container cnt;
        Management mngmt;
    };
};

