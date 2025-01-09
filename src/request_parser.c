/**
 * 
 * 
 * 
 */

#include "http.h"
#include "sys/socket.h"
#include <string.h>
#include <stdio.h>

#define BUFFER_SIZE                2024
#define PACKET_NEWL_CHAR           '\n'
#define QUERY_INTERFACE            '?'
#define METHOD_NVERSION_NURL_CYCLE 0
#define HOST_INFO_CYCLE            1
#define HEADER_BASE_CYCLE          2
#define HEADER_MAX_CYCLE           8
#define BODY_BASE_CYCLE            9

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
        /**
         *  | method | endpoint + query | http | cycle = 0 
         *  | Host                             | cycle = 1
         *  | Header Info                      | cycle = 2 - m
         *  | Body Content                     | cycle = n - m
         */
        int loop_cycle = 0;
        char *request_token = strtok(buffer, PACKET_NEWL_CHAR);
        while (request_token != NULL)
        {
            token_processor(request_token, loop_cycle++, &request);
            request_token = strtok(NULL, PACKET_NEWL_CHAR);
        }
    }
}

static void
token_processor(char token[], int cycle, http_request_t *request)
{
    int index = 0;

    switch (cycle)
    {
        case METHOD_NVERSION_NURL_CYCLE:

        char *zero_cycle_token = strtok(token, " ");
        while (zero_cycle_token != NULL && index != 2)
        {
            if (index == 0)
                strcpy(request->crud_method, zero_cycle_token); 
            else if (index == 1)
                request->url = get_url_from_request(zero_cycle_token);
            zero_cycle_token = strtok(NULL, " ");
        }
        break;
    }


}

static url_t
get_url_from_request(char url_token[])
{
    url_t url;
    int result = 0;

    for (int i = 0; i < strlen(url_token); i++)
    {
        if (url_token[i] == QUERY_INTERFACE)
        {
            result = 1;
            break;
        }   
    }

    if (result == 1)
    {
        char *splitted_url_token = strtok(url_token, "?");
        strcpy(url.endpoints, splitted_url_token);
        parse_query(strtok(NULL, "?"), &url);
        return url;
    }

    strcpy(url.endpoints, url_token);
    return url;
}


static void 
parse_query(char *query_to_parse, url_t *url)
{
    char c;
    int i = 0;
    
    url->map = (query_map_t *) calloc(sizeof(query_map_t), 20);

    char *and_splitted = strtok(query_to_parse, "&");
    while (and_splitted != NULL)
    {
        char *key = strtok(and_splitted, "=");
        char *value = strtok(NULL, "=");

        url->map[i].key = key;
        url->map[i].value = value; 
        
        and_splitted = strtok(NULL, "&");
        i++;
    }
}