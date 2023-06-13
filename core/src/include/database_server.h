#ifndef DATABASE_SERVER_H
#define DATABASE_SERVER_H

#include <stdbool.h>
#include "cJSON.h"
#include "book.h"

#define MAX_PATH_LENGTH 100

typedef struct
{
    char json_path[MAX_PATH_LENGTH];
    Book *books;
    int num_books;
} DatabaseServer;

DatabaseServer *database_server_new(const char *json_path);
void database_server_drop(DatabaseServer *self);
bool database_server_update(DatabaseServer *self);
Book *database_server_find(DatabaseServer *self, const char *book_name);

#endif /* DATABASE_SERVER_H */
