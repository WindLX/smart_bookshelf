#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include"cJSON.h"

typedef struct 
{
    /* data */
    char name[100];
    int position;
} Book;

Book book_database[100];
Book book_database_copy[100];
int book_count = 0;

void TakePhotoAndSend()
{}
void GetGravity()
{}



void Init_SD()//初始化SD卡
{}

void LoadToSD(Book books[], int num_books)//将数据存进SD卡中
{
    FILE* file = fopen("book_data.txt","w");
    if(file == NULL){
        return;
    }
    for(int i = 0;i <= num_books;i++){
        fprintf(file,"%s,%d\n",books[i].name, books[i].position);
    }

    fclose(file);
}

void Display()//也许是显示在屏幕上，或者语音输出
{}

const char* GetJSON()
{
}

void ProcessJSON(const char* json)
{   // 接收和处理JSON序列
    // 将结果序列化成结构体并存储到SD卡数据库中
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
    LoadToSD(books,numBooks);//将books加载到已经初始化的SD卡中
    // 释放内存
    free(books);
    cJSON_Delete(root);
}

float CalculateSimilarity(char user_input, char* book_name)
{}

void ProcessUserInput(const char user_input, float threshold)//此处用户输入的字符串是由语音信号转化而来
{
    for (int i = 0;i < book_count; i++){
        float similarity = CalculateSimilarity(user_input, book_database[i].name);
        if(similarity > threshold){
            Display();
        }
    }
}

void ManualUpdate()
{
    Init_SD();
    TakePhotoAndSend();
    ProcessJSON(GetJSON());
}

void GravityChanged(float threshold,Book *book_database,Book *book_database_copy)//进入识别模式
{    
    int num_before = book_count;
    int num_after;
    //依靠定时器中断完成每两分钟进行一次的以下操作
        TakePhotoAndSend();
        ProcessJSON(GetJSON());
        num_after = book_count;
        if(num_after <= num_before*threshold){
            num_before = num_after;
            *book_database = *book_database_copy;
        }else{
            //退出中断
        }

}



int main()
{
    
}