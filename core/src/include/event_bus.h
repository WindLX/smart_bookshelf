#ifndef EVENT_BUS_H
#define EVENT_BUS_H

#define MAX_HANDLERS 100

typedef struct
{
    const char *event_name;
    void *data;
} Event;

typedef struct
{
    const char *event_name;
    void (*handler)(Event *);
} Handler;

typedef struct
{
    int num_handlers;
    Handler *handlers[];
} EventBus;

EventBus *event_bus_new();

void event_bus_drop(EventBus *self);

void register_handler(EventBus *self, Handler *handler);

void publish_event(EventBus *self, Event *event);

#endif
