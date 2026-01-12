
struct Image {
    char *imageName;
    char *scripts;
    char *copyDir;
    char *workDir;
    int port;
    char *cmd;
};

struct Container {
    char *containerName;
    char *envs;
    char *host;
    char *entryPoint;
    char *version;
};

struct Management {
    char *victim;
};


bool cmdRun(char *cmd);

bool cmdExec(char *cmd);

bool cmdBuild(char *cmd);

bool cmdCreate(char *cmd);

bool cmdStart(char *cmd);

bool cmdStop(char *cmd);

bool cmdRm(char *cmd);

bool cmdPs(char *cmd);

bool cmdImages(char *cmd);
