/**
 * 
 * 
 */

#include <http.h>


typedef struct
{
    char *crud_method_type;
    char *api_endpoint;
    void (*method) (http_request_t, http_response_t *);
    struct crud *next;
    struct crud *top;
} crud_t;

extern crud_t **top;
extern void handle(const char crud_method[], const char endpoint[], void (*method) (http_request_t, http_response_t *));

