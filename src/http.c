/**
 * 
 */



typedef struct 
{
    char *crud_method;
    url_t url;
    header_t header;
    body_t body;
    char *host;
    char *pattern;

} http_request_t;


typedef struct
{

} http_response_t;


typedef struct
{

} url_t;

typedef struct
{

} header_t;

typedef struct
{

} body_t;