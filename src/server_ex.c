/**
 * Simple Example of a web server using Loki Framework.
 */


#include "loki.h"
#include "crud_function_handler.h"
#include "http.h"


void my_http_method_handler(http_request_t r, http_response_t *w)
{
    // Some code...
}

void my_http_method_handler2(http_request_t r, http_response_t *w)
{
    // Some code...
}


int main(void)
{
    web_server_t *my_server = web_server_alloc("127.0.0.1", 8080);
    handle("GET", "/foo", my_http_method_handler);
    handle("POST", "/foo/bar/qux", my_http_method_handler2);
    my_server->start_listening();
    return 0;
}