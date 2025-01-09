/**
 * 
 * 
 * Loki 
 */


typedef struct 
{
    char *host;
    int listen_port;
    void (*start_listening) ();
} web_server_t;


extern web_server_t* web_server_alloc(const char host_name[], int listen_port);