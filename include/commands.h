
typedef bool (*callback)(char *);

struct cmd {
    char *command;
    callback handler;
    char *description;
};
