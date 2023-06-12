#ifndef DATABASE_SERVER_H
#define DATABASE_SERVER_H

#include <stdbool.h>
#include "../../include/cJSON.h"
#include "../model/book.h"

#define MAX_PATH_LENGTH 100

// Forward declaration for the DatabaseServer structure
typedef struct DatabaseServer DatabaseServer;

// DatabaseServer structure definition
struct DatabaseServer
{
    char json_path[MAX_PATH_LENGTH];
    Book *books;
    int num_books;
};

// Function declarations
DatabaseServer *database_server_new(const char *json_path);
void database_server_drop(DatabaseServer *self);
bool database_server_update(DatabaseServer *self);
Book *database_server_find(DatabaseServer *self, const char *book_name);

#endif /* DATABASE_SERVER_H */
