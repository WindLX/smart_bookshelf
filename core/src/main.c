#include "include/database_server.h"
#include "include/event_bus.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void handle_event_print_data(Event *event)
{
    DatabaseServer *database_server = (DatabaseServer *)event->data;
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

int main()
{
    EventBus *event_bus = event_bus_new();
    DatabaseServer *database_server = database_server_new("../data/data.json");

    Handler handler_1 = {"print_data", handle_event_print_data};

    register_handler(event_bus, &handler_1);

    DatabaseServer *p = malloc(sizeof(DatabaseServer));
    memcpy(&p, &database_server, sizeof(DatabaseServer *));
    Event event_1 = {"print_data", p};

    publish_event(event_bus, &event_1);

    database_server_drop(database_server);
    event_bus_drop(event_bus);

    return 1;
}