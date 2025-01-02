/**
 *  
 * 
 */

#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <pthread.h>
#include "crud_function_handler.h"
#include "http.h"

typedef struct 
{
    char *host;
    int listen_port;
    void (*start_listening) ();
} web_server_t;

web_server_t *inner_server;

web_server_t* 
web_server_alloc(const char host_name[], int listen_port)
{
    if (inner_server == NULL)
    {
        inner_server = (web_server_t *) malloc(sizeof(web_server_t));
        inner_server->host = host_name;
        inner_server->listen_port = listen_port;
        inner_server->start_listening = &start_listening;
    } 
    else {
        exit(1);
    }

    return inner_server;
}

static void 
start_listening()
{   
    int server_fd;
    struct sockaddr_in server;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        exit(1);
    }

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htonl(inner_server->listen_port);

    if (bind(server_fd, &server, sizeof(server)) < 0)
    {
        exit(1);
    }

    if (listen(server_fd, 0) < 0)
    {
        exit(1);
    }

    while (1)
    {
        struct sockaddr_in requester;
        socklen_t requester_len = sizeof(requester);
        int *requester_fd = malloc(sizeof(int));

        requester_fd = accept(server_fd, &requester, &requester_len);

        if (requester_fd < 0)
        {
            // to log
            continue;
        }

        router_request(requester_fd, requester, requester_len);

        /*pthread_t th_id;
        pthread_create(&th_id, NULL, handle_request, requester_fd);
        pthread_detach(th_id);*/
    }

}

static void
route_requeste(int *client_fd, struct sockaddr_in client, socklen_t len)
{

}




