#include "./service/database_server.h"
#include <stdio.h>

int main()
{
    DatabaseServer *database_server = database_server_new("../data/data.json");
    if (database_server != NULL)
    {
        for (int i = 0; i < database_server->num_books; i++)
        {
            printf("%d\n", database_server->books[i].index);
            printf("%s\n", database_server->books[i].name);
            printf("%f\n", database_server->books[i].position);
            printf("\n");
        }
    }
}