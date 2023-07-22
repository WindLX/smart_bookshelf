#ifndef INC_BOOK_H_
#define INC_BOOK_H_

// 数据模型

#define MAX_BOOK_NAME_LENGTH 100

typedef struct
{
    int index;
    char name[MAX_BOOK_NAME_LENGTH];
    float position;
} Book;

#endif /* BOOK_H */
