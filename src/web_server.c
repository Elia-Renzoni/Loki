/**
 *  
 * 
 */


typedef struct 
{
    char *host;
    int listen_port;
    void (*start_listening)();
} web_server_t;

web_server_t* web_server_alloc(const char host_name[], int listen_port)
{
    web_server_t *inner_server = (web_server_t *) malloc(sizeof(web_server_t));
    inner_server->host = host_name;
    inner_server->listen_port = listen_port;
    inner_server->start_listening = &start_listening;

    return inner_server;
}

void start_listening()
{
    // TODO

}



