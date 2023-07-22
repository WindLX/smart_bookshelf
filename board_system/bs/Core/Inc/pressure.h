/*
 * pressure.h
 *
 *  Created on: 2023年7月15日
 *      Author: wind
 */

#ifndef INC_PRESSURE_H_
#define INC_PRESSURE_H_

#include <string.h>
#include "adc.h"

#define PRESS_MIN	150
#define PRESS_MAX	20000

#define VOLTAGE_MIN 100
#define VOLTAGE_MAX 3300

typedef struct {
	ADC_HandleTypeDef *hadc;
	int32_t bottom;
} Pressure_HandleTypeDef;

typedef enum {
	Pressure_AD=0,
	Pressure_Vol=1,
	Pressure_Pre=2,
} Pressure_ReadMode;

extern Pressure_HandleTypeDef pressure;

void Pressure_Init(Pressure_HandleTypeDef *pressure, ADC_HandleTypeDef *hadc, int32_t bottom);
int32_t Pressure_Read(Pressure_HandleTypeDef *pressure, Pressure_ReadMode mode, uint8_t times);

#endif /* INC_PRESSURE_H_ */
