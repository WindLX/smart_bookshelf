SysState sys_state = Normal;
int t = 0;

int main(void)
{
	#ifndef MYDEBUG
	HAL_UARTEx_ReceiveToIdle_DMA(&huart3, receive_data, BUFFER_SIZE);
	__HAL_DMA_DISABLE_IT(&hdma_usart3_rx, DMA_IT_HT);
	#else
	HAL_UARTEx_ReceiveToIdle_DMA(&huart6, receive_data, BUFFER_SIZE);
	__HAL_DMA_DISABLE_IT(&hdma_usart6_rx, DMA_IT_HT);
	#endif

	__HAL_TIM_CLEAR_IT(&htim3, TIM_IT_UPDATE);
	HAL_TIM_Base_Start_IT(&htim3);

	Led_Init(&led, &htim2, TIM_CHANNEL_1);
	Led_Code_Reset(&led);

	Camera_Init(&camera, &huart2);

	Pressure_Init(&pressure, &hadc2, 0);
	int32_t last_press = Pressure_Read(&pressure, Pressure_Pre, 100);

	OLED_Init();
	OLED_Clear();
	OLED_Display_On();
	DrawBG();
	HAL_TIM_Base_Start_IT(&htim6);

	HAL_Delay(2000);

	HAL_Delay(12000);

	Led_Range_Set(&led, 0.1, 0, 212, 70);
	Led_Range_Set(&led, 0.2, 0, 212, 70);
	Led_Range_Set(&led, 0.45, 0, 212, 70);
	Led_Start(&led);

  while (1)
  {
	  int32_t press = Pressure_Read(&pressure, Pressure_Pre, 100);

	  if (sys_state == Normal) {
		  // 正常模式下检测压力传感器
		  HAL_GPIO_WritePin(LD1_GPIO_Port, LD1_Pin, GPIO_PIN_SET);
		  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_RESET);
		  if (ABS(press - last_press) > 12) {
			  sys_state = Monitor;
			  DrawText(2);
		  }
		  last_press = press;
	  }
	  else if (sys_state == Monitor) {
		  // 2min 定时拍照
		  HAL_GPIO_WritePin(LD1_GPIO_Port, LD1_Pin, GPIO_PIN_RESET);
		  HAL_GPIO_WritePin(LD3_GPIO_Port, LD3_Pin, GPIO_PIN_SET);
		  if (Camera_GetState(&camera) == Camera_Idle)
		  {
			  Camera_Start(&camera);
		  }
		  else if (Camera_GetCount(&camera) > 10)
		  {
			  Camera_Reset(&camera);
			  Led_All_Reset(&led);
			  Led_Start(&led);
			  sys_state = Normal;
		  }
	  }
  }
}