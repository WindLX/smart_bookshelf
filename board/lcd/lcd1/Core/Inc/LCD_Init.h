#ifndef LCD_INIT_H
#define LCD_INIT_H

#define USE_HORIZONTAL 1  //设置横屏或者竖屏显示 0或1为竖屏 2或3为横屏

#if USE_HORIZONTAL==0||USE_HORIZONTAL==1
#define LCD_W 128
#define LCD_H 160

#else
#define LCD_W 160
#define LCD_H 128
#endif

void LCD_Init(void);//LCD初始化
void LCD_WR_DATA8(uint8_t data);//写入一个字节
void LCD_WR_DATA(uint16_t data);//写入两个字节
void LCD_WR_REG(uint8_t command);//写入一个指令
void LCD_Address_Set(uint16_t x1,uint16_t y1,uint16_t x2,uint16_t y2);//设置坐标函数
#endif