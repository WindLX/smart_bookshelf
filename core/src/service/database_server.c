#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./database_server.h"

bool parseBooks(cJSON *books_array, Book **books, int *num_books)
{
    *num_books = cJSON_GetArraySize(books_array);
    *books = malloc(*num_books * sizeof(Book));

    for (int i = 0; i < *num_books; i++)
    {
        cJSON *book_object = cJSON_GetArrayItem(books_array, i);
        cJSON *index_item = cJSON_GetObjectItem(book_object, "index");
        cJSON *name_item = cJSON_GetObjectItem(book_object, "name");
        cJSON *position_item = cJSON_GetObjectItem(book_object, "position");

        if (name_item != NULL && position_item != NULL && index_item != NULL && cJSON_IsString(name_item) && cJSON_IsNumber(position_item) && cJSON_IsNumber(index_item))
        {
            strncpy((*books)[i].name, name_item->valuestring, MAX_BOOK_NAME_LENGTH - 1);
            (*books)[i].name[MAX_BOOK_NAME_LENGTH - 1] = '\0';
            (*books)[i].position = position_item->valueint;
            (*books)[i].index = index_item->valueint;
        }
        else
        {
            return false;
        }
    }
    return true;
}

const char *read_file(const char *file_path)
{
    FILE *file = fopen(file_path, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Failed to open file: %s\n", file_path);
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    rewind(file);

    char *buffer = (char *)malloc(file_size + 1);
    if (buffer == NULL)
    {
        fclose(file);
        fprintf(stderr, "Failed to allocate memory for file content.\n");
        return NULL;
    }

    fread(buffer, 1, file_size, file);

    buffer[file_size] = '\0';

    fclose(file);
    return buffer;
}

DatabaseServer *database_server_new(const char *json_path)
{
    cJSON *root = cJSON_Parse(read_file(json_path));
    if (root == NULL)
    {
        printf("JSON parse failed\n");
        return NULL;
    }

    cJSON *books_array = cJSON_GetObjectItem(root, "books");
    if (books_array == NULL || !cJSON_IsArray(books_array))
    {
        printf("Invalid books array\n");
        cJSON_Delete(root);
        return NULL;
    }

    Book *books;
    int num_books;
    if (parseBooks(books_array, &books, &num_books))
    {
        DatabaseServer *server = malloc(sizeof(DatabaseServer));
        strncpy(server->json_path, json_path, MAX_PATH_LENGTH - 1);
        server->json_path[MAX_PATH_LENGTH - 1] = '\0';
        server->books = books;
        server->num_books = num_books;

        cJSON_Delete(root);

        return server;
    }
    else
    {
        printf("JSON parse failed\n");
        return NULL;
    }
}

void database_server_drop(DatabaseServer *self)
{
    if (self == NULL)
    {
        return;
    }

    free(self->books);
    free(self);
}

bool database_server_update(DatabaseServer *self)
{
    cJSON *root = cJSON_Parse(self->json_path);
    if (root == NULL)
    {
        printf("JSON parse failed\n");
        return false;
    }

    cJSON *books_array = cJSON_GetObjectItem(root, "books");
    if (books_array == NULL || !cJSON_IsArray(books_array))
    {
        printf("Invalid books array\n");
        cJSON_Delete(root);
        return false;
    }

    Book *books;
    int num_books;
    if (parseBooks(books_array, &books, &num_books))
    {
        free(self->books);
        self->books = books;
        self->num_books = num_books;

        cJSON_Delete(root);

        return true;
    }
    else
    {
        printf("JSON parse failed\n");
        return false;
    }
}

Book *database_server_find(DatabaseServer *self, const char *book_name)
{
    for (int i = 0; i < self->num_books; i++)
    {
        if (strcmp(self->books[i].name, book_name) == 0)
        {
            return &(self->books[i]);
        }
    }

    return NULL;
}
