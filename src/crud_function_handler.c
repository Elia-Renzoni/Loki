/**
 * 
 * 
 * 
 */

#include "http.h"
#include <stdlib.h>
#include <string.h>

typedef struct crud
{
    char *crud_method_type;
    char *api_endpoint;
    void (*method) (http_request_t, http_response_t *);
    struct crud *next;
} crud_t;

crud_t **top;

void
handle(const char crud_method[], const char endpoint[], void (*method) (http_request_t, http_response_t *))
{
   crud_t *crud_operation = (crud_t *) malloc(sizeof(crud_t));

   crud_operation->crud_method_type = crud_method;
   crud_operation->api_endpoint = endpoint;
   crud_operation->method = method;
   crud_operation->next = *top;
   *top = crud_operation;
}

crud_t *
search_for_task(const char api_endpoint[])
{
    for (crud_t *node = *top; (node != NULL); node = (*top)->next)
    {
        int cmp_result = strcmp(api_endpoint, node->api_endpoint);
        if (cmp_result)
        { 
            return node;
        }   
    }

    return NULL;
}