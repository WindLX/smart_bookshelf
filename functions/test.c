#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cJSON.h"

typedef struct {
    char name[100];
    int position;
} Book;

void processJSON(const char* json) {//输入一个指向json序列的指针
    // 解析 JSON 序列
    cJSON* root = cJSON_Parse(json);
    if (root == NULL) {
        printf("JSON 解析失败\n");
        return;
    }
    // 获取 books 数组
    cJSON* booksArray = cJSON_GetObjectItem(root, "books");
    if (booksArray == NULL || !cJSON_IsArray(booksArray)) {
        printf("无效的 books 数组\n");
        cJSON_Delete(root);
        return;
    }

    int numBooks = cJSON_GetArraySize(booksArray);
    Book* books = malloc(numBooks * sizeof(Book));

    // 遍历 books 数组，解析每个书籍对象
    for (int i = 0; i < numBooks; i++) {
        cJSON* bookObject = cJSON_GetArrayItem(booksArray, i);
        cJSON* nameItem = cJSON_GetObjectItem(bookObject, "name");
        cJSON* positionItem = cJSON_GetObjectItem(bookObject, "position");

        if (nameItem != NULL && positionItem != NULL && cJSON_IsString(nameItem) && cJSON_IsNumber(positionItem)) {
            strcpy(books[i].name, nameItem->valuestring);
            books[i].position = positionItem->valueint;
        }
    }

    // 处理结构体数据，例如存储到数据库或进行其他操作
    for (int i = 0; i < numBooks; i++) {
        printf("Book name: %s, position: %d\n", books[i].name, books[i].position);
    }

    // 释放内存
    free(books);
    cJSON_Delete(root);
}

int main() {
    // 模拟接收到的 JSON 序列
    const char* receivedJson = "{\"books\":[{\"name\":\"Book 1\",\"position\":1},{\"name\":\"Book 2\",\"position\":2}]}";

    processJSON(receivedJson);

    return 0;
}
