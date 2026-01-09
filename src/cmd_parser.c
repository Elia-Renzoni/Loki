#include <stdbool.h>
#include <string.h>

bool parseFirstIndexCommand(const char *, const int);

static char *cmds[] = {
    "run", "exec", "create", "build",
    "start", "stop", "rm", "ps", "image",
};

bool parseCommands(const char cmd[]) {
    const int len = strlen(cmd);
    if (len == 0) 
        return false;

    for (int i = 0; i < len; i++) {
        if (parseFirstIndexCommand(cmd, len))
            return false;
        
    }

    return false;
}

bool parseFirstIndexCommand(const char *cmd, const int len) {
    for (int i = 0; i < len; i++) {
        if (strcmp(cmd, cmds[i])) 
            return true;
    }

    return false;
}
