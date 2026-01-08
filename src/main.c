#include<stdio.h>
#include<stdlib.h>

enum {
    SYNTAX_ERROR,
    UNKNOWN_COMMAND,
} lokiError;

lokiError commandStrainer(char *cmd) {
   lokiError err;
   return err;
}

int main(int argc, char **argv) {
    if (argc == 0) {
        printf("empty commands\n");
        exit(1);
    }
    commandStrainer(argv[0]);
    return 0;
}
