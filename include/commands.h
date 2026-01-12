
typedef bool (*callback)(char *);

struct cmd {
    char *command;
    callback handler;
    char *description;
};

struct Image {
    char *imageName;
    char *scripts;
    char *copyDir;
    char *workDir;
    int port;
    char *cmd;
};

struct Container {
};
