#ifndef OCR_SERVER_H
#define OCR_SERVER_H

#define MAX_ADDRESS_LENGTH 100

typedef struct {
    char address[MAX_ADDRESS_LENGTH];
    char json_path[MAX_PATH_LENGTH];
}OcrServer;

OcrServer *ocr_server_new(const char* address);

void ocr_server_drop(OcrServer* self);

bool ocr_server_request(const char* image_path);

#endif