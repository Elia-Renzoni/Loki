/**
 * 
 * 
 * 
 */

#include "http.h"
#include "sys/socket.h"
#include <string.h>
#include <stdio.h>

#define BUFFER_SIZE 2024
#define PACKET_TAB_CHAR '\t'

http_request_t 
parse_request(int requesteer_fd)
{
    char buffer[BUFFER_SIZE];
    http_request_t request;

    int read_result = recv(requesteer_fd, buffer, BUFFER_SIZE, 0);
    if (read_result != 1)
    {
        printf("Print Some Error State!!!\n");
    }
    else
    {
        // bytes scanning
        char *request_token = strtok(buffer, "\n");
        while (request_token != NULL)
        {
            char *inner_token = strtok(request_token, " ");
            while (inner_token != NULL)
            {
                // TODO: filling http_request_t struct... 
            }
        }
    }
}