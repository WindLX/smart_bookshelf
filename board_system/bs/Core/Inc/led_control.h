#ifndef _LED_CONTROL_H_
#define _LED_CONTROL_H_

#include <string.h>
#include "tim.h"
#include "dma.h"
#include "utils.h"

/*
硬件定时器PWM+DMA:
需要:
    1.定时器:
        PWM输出一个通道
        不分频
        计数值为 1.25us(公式: 1.25 *系统频率(单位MHz))
        输出IO设置为开漏浮空输出(外接5V上拉)
    2.DMA
        内存到外设
        字(word)模式
        开启DMA中断
0码的是 0.4us,1码是0.8us
公式是 t(us)*系统频率(单位MHz)
 */
#define LED_CODE_0 (90u)
#define LED_CODE_1 (207u)

#define LED_NUM 60
#define LED_TRUE_NUM 23

typedef struct {
	uint32_t led_data[LED_NUM];
	TIM_HandleTypeDef *htim;
	uint32_t channel;
	uint32_t led_SendBuf0[25];   // 发送缓冲区0
	uint32_t led_SendBuf1[25];   // 发送缓冲区1
	uint32_t led_En;               // 发送使能
	uint32_t led_Rst[240]; // 复位码缓冲区
}Led_HandleTypeDef;

extern Led_HandleTypeDef led;

void Led_Init(Led_HandleTypeDef *led, TIM_HandleTypeDef *htim, uint32_t Channel);
void Led_Start(Led_HandleTypeDef *led);
void Led_Code_Reset(Led_HandleTypeDef *led);
void Led_Send(Led_HandleTypeDef *led);
void Led_Set(Led_HandleTypeDef *led, int index, uint8_t r, uint8_t g, uint8_t b);
void Led_Reset(Led_HandleTypeDef *led, int index);
void Led_All_Reset(Led_HandleTypeDef *led);
void Led_Range_Set(Led_HandleTypeDef *led, float coor, uint8_t r, uint8_t g, uint8_t b);

#endif
