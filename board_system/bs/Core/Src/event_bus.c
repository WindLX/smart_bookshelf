#include "event_bus.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

EventBus *event_bus_new()
{
    EventBus *bus = malloc(sizeof(EventBus));
    bus->num_handlers = 0;
    return bus;
}

void event_bus_drop(EventBus *self)
{
    free(self);
}

void register_handler(EventBus *bus, Handler *handler)
{
    if (bus->num_handlers < MAX_HANDLERS)
    {
        bus->handlers[bus->num_handlers++] = handler;
    }
}

void publish_event(EventBus *bus, Event *event)
{
    int i;
    for (i = 0; i < bus->num_handlers; i++)
    {
        if (strcmp(event->event_name, bus->handlers[i]->event_name) == 0)
        {
            bus->handlers[i]->handler(event);
        }
    }
}
