/*
 * utils.c
 *
 *  Created on: 2023年7月12日
 *      Author: wind
 */

#include "utils.h"

uint8_t receive_data[BUFFER_SIZE];

double* parseStringToArray(const char* str, int* count) {
	if (str[0] == '[') return NULL;

    const char* delimiter = ", ";

    if (strlen(str) == 0) return NULL;
    else {
    	*count =1;
		for (int i = 0; i < strlen(str); i++) {
			if (str[i] == ',') {
				(*count)++;
			}
		}
    }

    double* array = (double*)malloc(*count * sizeof(double));

    if (*count != 1)
	{
		char *token = strtok((char *)str, delimiter);
		int index = 0;

		while (token != NULL)
		{
			array[index++] = (double)atof(token);
			token = strtok(NULL, delimiter);
		}
	}
	else
	{
		array[0] = atof(str);
	}

    return array;
}
