#ifndef BOOK_H
#define BOOK_H

// 数据库模型

#define MAX_BOOK_NAME_LENGTH 100

typedef struct
{
    int index;
    char name[MAX_BOOK_NAME_LENGTH];
    float position;
} Book;

#endif /* BOOK_H */
