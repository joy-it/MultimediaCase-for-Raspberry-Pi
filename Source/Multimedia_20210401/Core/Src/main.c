/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/************************************************************************************************************************************************************

 MultimediaCase for Raspberry Pi - by Joy-IT
 OpenSource-Firmware published under MIT-License

************************************************************************************************************************************************************

 The following code defines the firmware for the STM32 controller of the RB-MultimediaCase01. The code uses the
 Infrared-Multiprotocoll-Decoder (IRMP - licensed under GNU General Public License v3.0) to recognize IR-remote signals
 and process these. The WS2812B LEDs can be controlled with the STM32 controller or with the Raspberry Pi. The Case Button
 is handled by an interrupt routine.
 The STM32 is mainly used to control the power status of the connected Raspberry Pi. It is able to power the Raspberry Pi via
 the 5 V pins and can send a shutdown-command via serial (which is processed via an addon). After shutdown of the Raspberry Pi
 the STM32 cuts the 5 V supply.
 During the different routines (starting, shutdown, learning) the STM32 takes the control of the 4 WS2812B and displays
 the actual active routine with the help of colors.

 */


/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "irmp.h"
#include "ws28xx.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
IRMP_DATA irmp_data;
IRMP_DATA irmp_new_data;
IRMP_DATA irmp_temp_data;


PAGEError = 0;
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc;

SPI_HandleTypeDef hspi1;
DMA_HandleTypeDef hdma_spi1_tx;

TIM_HandleTypeDef htim1;
TIM_HandleTypeDef htim14;
TIM_HandleTypeDef htim16;

UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC_Init(void);
static void MX_SPI1_Init(void);
static void MX_TIM14_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_TIM1_Init(void);
static void MX_TIM16_Init(void);
static void MX_NVIC_Init(void);
/* USER CODE BEGIN PFP */
static void RPi_Power_Up();
static void RPi_Power_Down();

static void RGB_RPi();
static void RGB_MCU();

static void WS2812_ChangeColor(ws28xx_Color_TypeDef Color);

static void flashConfig(void);

static void flashValue(uint32_t address, uint32_t data);

static void deactivateIR(void);
static void activateIR(void);

static void learningmode(void);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

	/*** Definition of the shutdown message, which is send via the serial interface ***/
	uint8_t shutdownMessage[] = "xxxShutdownRaspberryPixxx\n\r";

	/*** Definition of LED status message ***/
	uint8_t ledStatus[] = "0\n\r";

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC_Init();
  MX_SPI1_Init();
  MX_TIM14_Init();
  MX_USART1_UART_Init();
  MX_TIM1_Init();
  MX_TIM16_Init();

  /* Initialize interrupts */
  MX_NVIC_Init();
  /* USER CODE BEGIN 2 */

  /*** Loading IRMP configuration from flash***/
  irmp_data.protocol = *(uint8_t *)irmp_protocol_FlashAdress;
  irmp_data.address = *(uint16_t *)irmp_address_FlashAdress;
  irmp_data.command = *(uint16_t *)irmp_command_FlashAdress;

  /*** Loading LED configuration from flash***/
  ledMode = *(uint8_t *)led_mode_FlashAdress;

  if (ledMode == 0xFF)
  	{
	  ledMode = 0;
  	}

  /*** Initialization of IRMP ***/
  irmp_init();

  /*** STM32 taking the control over WS2812b LEDs and set these to red***/
  RGB_MCU();


  	  //WS2812_ChangeColor(ws28xx_Color_Red);
	  //HAL_Delay(100);
	  WS2812_ChangeColor(ws28xx_Color_Red);

	  if (!(ledMode == 0))
	  {
		  HAL_Delay(100);
		  WS2812_ChangeColor(ws28xx_Color_Black);
	  }

  /*** Making sure, that the Raspberry Pi is powered down ***/
  RPi_Power_Down();

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

  /*** Here starts the infinite loop. This loop manages the power status via button and IR-remote and the learning mode. ***/
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	  /*** learning mode check ***/
	  if(!strcmp(Rx_data,"X04\r"))
	  	  {
		  	  strcpy(Rx_data, "    ");
		  	  learningmode();
		  	  activateIR();
	  	  }

	  /*** ledMode: "LM0\r" = normal Mode, "LM1\r" = only startup and shutdown LED, "LM2\r" = no LED (except learning mode)***/
	  if(!strncmp(Rx_data, "LM", 2) && Rx_data[2] >= '0' && Rx_data[2] <= '3' && Rx_data[3] == 13)
	  {
		  RGB_MCU();

		  if(Rx_data[2] == '0')
		  {
			  ledMode = 0;
			  ledStatus[0] = '0';
			  HAL_Delay(100);
			  WS2812_ChangeColor(ws28xx_Color_Green);
		  }

		  else if(Rx_data[2] == '1')
		  {
			  ledMode = 1;
			  ledStatus[0] = '1';
			  HAL_Delay(100);
			  WS2812_ChangeColor(ws28xx_Color_Black);
		  }

		  else if(Rx_data[2] == '2')
		  {
			  ledMode = 2;
			  ledStatus[0] = '2';
			  HAL_Delay(100);
			  WS2812_ChangeColor(ws28xx_Color_Black);
		  }

		  else if(Rx_data[2] == '3')
		  {
			  HAL_UART_Transmit(&huart1, (uint8_t *)ledStatus, sizeof(ledStatus), sizeof(ledStatus));
		  }
		  flashConfig();
		  strcpy(Rx_data, "    ");
		  RGB_RPi();
	  }


	  	  /*** checking for IRMP data or button press ***/
	  	  if (irmp_get_data (&irmp_temp_data) || button > 0)
	  	  	{
	  		  	  __HAL_TIM_DISABLE_IT(&htim14, TIM_IT_UPDATE);
	  		  	  HAL_NVIC_DisableIRQ(EXTI0_1_IRQn);
	  		  	  HAL_Delay(50);

	  		  	  /*** shutdown routine ***/

	  		  	  if (powerUP == 1)
	  		  	  {

		  		  	  if ((((irmp_temp_data.command == irmp_data.command) && (irmp_temp_data.address == irmp_data.address) && (irmp_temp_data.protocol == irmp_data.protocol) )|| (((button > 0)))))
		  		  	  {
		  		  		  memset(&irmp_temp_data, 0, sizeof(IRMP_DATA));
		  		  		  RGB_MCU();
		  		  		  HAL_UART_Transmit(&huart1, (uint8_t *)shutdownMessage, sizeof(shutdownMessage), sizeof(shutdownMessage));
		  		    	  if (ledMode == 2)
		  		    	  {
		  		    		  WS2812_ChangeColor(ws28xx_Color_Red);
		  		    		  HAL_Delay(100);
		  		    	  }

		  		  		  WS2812_ChangeColor(ws28xx_Color_Black);
		  		    	  HAL_Delay(100);
		  		    	  __HAL_TIM_CLEAR_IT(&htim16 ,TIM_IT_UPDATE);
		  		    	  __HAL_TIM_SET_COUNTER(&htim16, 0);
		  		    	  HAL_TIM_Base_Start_IT(&htim16);
		  		    	  timer = shutDownTime;
		  		    	  while(timer > 0)
		  		    		  {
							  	  if (!(ledMode == 2))
							  	  {
							  		  ws28xx_fade(ws28xx_Color_Red);
							  	  }

		  		    		  }

		  		    	  if (ledMode == 0)
		  		    	  {
			  		    	  WS2812_ChangeColor(ws28xx_Color_Red);
		  		    	  }

		  		    	  else
		  		    	  {
		  		    		  ws28xx_fade(ws28xx_Color_Red);
		  		    	  }

		  		  		  HAL_Delay(50);
		  		  		  RPi_Power_Down();
		  		  		  powerUP = 0;
		  		  		  button = 0;

		  		  	  }

					}

	  		  	  else if (powerUP == 0)
					{

						/*** powerup routine ***/

						if ((((irmp_temp_data.command == irmp_data.command) && (irmp_temp_data.address == irmp_data.address) && (irmp_temp_data.protocol == irmp_data.protocol) )||(( (button > 0)))))
						{
							  memset(&irmp_temp_data, 0, sizeof(IRMP_DATA));

							  RPi_Power_Up();
			  		    	  if (ledMode == 2)
			  		    	  {
			  		    		  WS2812_ChangeColor(ws28xx_Color_Green);
			  		    		  HAL_Delay(100);
			  		    	  }
							  WS2812_ChangeColor(ws28xx_Color_Black);
							  HAL_Delay(100);
							  __HAL_TIM_CLEAR_IT(&htim16 ,TIM_IT_UPDATE);
							  __HAL_TIM_SET_COUNTER(&htim16, 0);
							  HAL_TIM_Base_Start_IT(&htim16);
							  timer = bootUpTime;

							  /*** if startup complete "X05/r" is sent via serial interface, the timer is reseted ***/
							  while(timer > 0)
								  {
									  if (!(ledMode == 2))
									  	  {
										  	  ws28xx_fade(ws28xx_Color_Green);
									  	  }

									  if(!strcmp(Rx_data,"X05\r"))
										  {
										  	  strcpy(Rx_data, "    ");
											  timer = 0;
										  }
								  }

							  if (ledMode == 0)
							  {
								  WS2812_ChangeColor(ws28xx_Color_Green);
							  }

							  else
							  {
								  ws28xx_fade(ws28xx_Color_Green);
							  }

							  HAL_Delay(50);

							  RGB_RPi();
							  powerUP = 1;
							  button = 0;

					}
					}

	  		  	__HAL_TIM_ENABLE_IT(&htim14, TIM_IT_UPDATE);

	  		  	__HAL_GPIO_EXTI_CLEAR_FLAG(BUTTON_IN_Pin);
	  		  	__HAL_GPIO_EXTI_CLEAR_IT(BUTTON_IN_Pin);
	  		  	  HAL_NVIC_ClearPendingIRQ(EXTI0_1_IRQn);
	  		  	  HAL_NVIC_EnableIRQ(EXTI0_1_IRQn);
	  		  	  HAL_Delay(50);
	  	  	}

	    }

  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_HSI14;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSI14State = RCC_HSI14_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.HSI14CalibrationValue = 16;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL5;
  RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART1;
  PeriphClkInit.Usart1ClockSelection = RCC_USART1CLKSOURCE_PCLK1;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief NVIC Configuration.
  * @retval None
  */
static void MX_NVIC_Init(void)
{
  /* TIM14_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(TIM14_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(TIM14_IRQn);
  /* USART1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(USART1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(USART1_IRQn);
  /* EXTI0_1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(EXTI0_1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI0_1_IRQn);
  /* TIM1_CC_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(TIM1_CC_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(TIM1_CC_IRQn);
}

/**
  * @brief ADC Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC_Init(void)
{

  /* USER CODE BEGIN ADC_Init 0 */

  /* USER CODE END ADC_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC_Init 1 */

  /* USER CODE END ADC_Init 1 */
  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion) 
  */
  hadc.Instance = ADC1;
  hadc.Init.ClockPrescaler = ADC_CLOCK_ASYNC_DIV1;
  hadc.Init.Resolution = ADC_RESOLUTION_12B;
  hadc.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc.Init.ScanConvMode = ADC_SCAN_DIRECTION_FORWARD;
  hadc.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  hadc.Init.LowPowerAutoWait = DISABLE;
  hadc.Init.LowPowerAutoPowerOff = DISABLE;
  hadc.Init.ContinuousConvMode = DISABLE;
  hadc.Init.DiscontinuousConvMode = DISABLE;
  hadc.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc.Init.DMAContinuousRequests = DISABLE;
  hadc.Init.Overrun = ADC_OVR_DATA_PRESERVED;
  if (HAL_ADC_Init(&hadc) != HAL_OK)
  {
    Error_Handler();
  }
  /** Configure for the selected ADC regular channel to be converted. 
  */
  sConfig.Channel = ADC_CHANNEL_9;
  sConfig.Rank = ADC_RANK_CHANNEL_NUMBER;
  sConfig.SamplingTime = ADC_SAMPLETIME_1CYCLE_5;
  if (HAL_ADC_ConfigChannel(&hadc, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC_Init 2 */

  /* USER CODE END ADC_Init 2 */

}

/**
  * @brief SPI1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI1_Init(void)
{

  /* USER CODE BEGIN SPI1_Init 0 */

  /* USER CODE END SPI1_Init 0 */

  /* USER CODE BEGIN SPI1_Init 1 */

  /* USER CODE END SPI1_Init 1 */
  /* SPI1 parameter configuration*/
  hspi1.Instance = SPI1;
  hspi1.Init.Mode = SPI_MODE_MASTER;
  hspi1.Init.Direction = SPI_DIRECTION_2LINES;
  hspi1.Init.DataSize = SPI_DATASIZE_7BIT;
  hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi1.Init.NSS = SPI_NSS_SOFT;
  hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
  hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi1.Init.CRCPolynomial = 7;
  hspi1.Init.CRCLength = SPI_CRC_LENGTH_DATASIZE;
  hspi1.Init.NSSPMode = SPI_NSS_PULSE_ENABLE;
  if (HAL_SPI_Init(&hspi1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI1_Init 2 */

  /* USER CODE END SPI1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 32000;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 50;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}

/**
  * @brief TIM14 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM14_Init(void)
{

  /* USER CODE BEGIN TIM14_Init 0 */

  /* USER CODE END TIM14_Init 0 */

  /* USER CODE BEGIN TIM14_Init 1 */

  /* USER CODE END TIM14_Init 1 */
  htim14.Instance = TIM14;
  htim14.Init.Prescaler = 0;
  htim14.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim14.Init.Period = 1599;
  htim14.Init.ClockDivision = TIM_CLOCKDIVISION_DIV2;
  htim14.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim14) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM14_Init 2 */
  HAL_TIM_Base_Start_IT(&htim14);
  /* USER CODE END TIM14_Init 2 */

}

/**
  * @brief TIM16 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM16_Init(void)
{

  /* USER CODE BEGIN TIM16_Init 0 */

  /* USER CODE END TIM16_Init 0 */

  /* USER CODE BEGIN TIM16_Init 1 */

  /* USER CODE END TIM16_Init 1 */
  htim16.Instance = TIM16;
  htim16.Init.Prescaler = 3124;
  htim16.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim16.Init.Period = 63999;
  htim16.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim16.Init.RepetitionCounter = 0;
  htim16.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim16) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM16_Init 2 */

  /* USER CODE END TIM16_Init 2 */

}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 38400;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  huart1.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart1.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */
  HAL_UART_Receive_IT(&huart1, &RxBuffer, 1);
  /* USER CODE END USART1_Init 2 */

}

/** 
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void) 
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA1_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA1_Channel2_3_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA1_Channel2_3_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA1_Channel2_3_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, CTRL_VUSB_Pin|RGB_MCU_EN_Pin|RGB_RPi_EN_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pins : CTRL_VUSB_Pin RGB_MCU_EN_Pin RGB_RPi_EN_Pin */
  GPIO_InitStruct.Pin = CTRL_VUSB_Pin|RGB_MCU_EN_Pin|RGB_RPi_EN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : BUTTON_IN_Pin */
  GPIO_InitStruct.Pin = BUTTON_IN_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(BUTTON_IN_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : IRMP_Receive_Pin */
  GPIO_InitStruct.Pin = IRMP_Receive_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(IRMP_Receive_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

/*** Powering the Raspberry Pi with 5 V ***/

static void RPi_Power_Up()
{
	HAL_GPIO_WritePin(CTRL_VUSB_GPIO_Port, CTRL_VUSB_Pin, GPIO_PIN_SET);
}

/*** Cutting 5 V supply of Rasperry Pi***/

static void RPi_Power_Down()
{
	HAL_GPIO_WritePin(CTRL_VUSB_GPIO_Port, CTRL_VUSB_Pin, GPIO_PIN_RESET);
}

/*** Raspberry Pi has control over RGB LEDs ***/

static void RGB_RPi()
{
	HAL_GPIO_WritePin(RGB_MCU_EN_GPIO_Port, RGB_MCU_EN_Pin, GPIO_PIN_SET);
	HAL_GPIO_WritePin(RGB_RPi_EN_GPIO_Port, RGB_RPi_EN_Pin, GPIO_PIN_RESET);
}

/*** STM32 takes the control of the RGB LEDs ***/

static void RGB_MCU()
{
	HAL_GPIO_WritePin(RGB_MCU_EN_GPIO_Port, RGB_MCU_EN_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(RGB_RPi_EN_GPIO_Port, RGB_RPi_EN_Pin, GPIO_PIN_SET);
}

/*** Controls all LEDs at once ***/

static void WS2812_ChangeColor(ws28xx_Color_TypeDef Color)
{
	  ws28xx_SetColor(0, Color);
	  ws28xx_SetColor(1, Color);
	  ws28xx_SetColor(2, Color);
	  ws28xx_SetColor(3, Color);
	  ws28xx_Update();
}

/*** Writes the IRMP config into flash ***/

static void flashConfig(void)
{
	FLASH_EraseInitTypeDef EraseInitStruct;

	HAL_FLASH_Unlock();
	EraseInitStruct.TypeErase   = FLASH_TYPEERASE_PAGES;
	EraseInitStruct.PageAddress = 0x8007C00;
	EraseInitStruct.NbPages     = 1;


	 if (HAL_FLASHEx_Erase(&EraseInitStruct, &PAGEError) != HAL_OK)
	  {
	    /*
	      Error occurred while page erase.
	      User can add here some code to deal with this error.
	      PAGEError will contain the faulty page and then to know the code error on this page,
	      user can call function 'HAL_FLASH_GetError()'
	    */
	    /* Infinite loop */
	  }

	  flashValue(irmp_protocol_FlashAdress,irmp_new_data.protocol);
	  flashValue(irmp_address_FlashAdress,irmp_new_data.address);
	  flashValue(irmp_command_FlashAdress,irmp_new_data.command);

	  flashValue(led_mode_FlashAdress,ledMode);

	HAL_FLASH_Lock();

}

static void flashValue(uint32_t address, uint32_t data)
{
	 if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, address , data) != HAL_OK)
	  {
	    /*
	      Error occurred while page erase.
	      User can add here some code to deal with this error.
	      PAGEError will contain the faulty page and then to know the code error on this page,
	      user can call function 'HAL_FLASH_GetError()'
	    */
	  }
}


/*** Function to deactivate the timer of the IR sensor ***/

static void deactivateIR()
{
	HAL_TIM_Base_Stop(&htim14);
}

/*** Function to activate the timer of the IR sensor ***/

static void activateIR()
{
	__HAL_TIM_CLEAR_IT(&htim14, TIM_IT_UPDATE);
	HAL_TIM_Base_Start_IT(&htim14);
	__HAL_TIM_SET_COUNTER(&htim14, 0);
}

/*** Function for learning a new IR-remote ***/

static void learningmode()
{
	  uint8_t learningMode_on;

	  learningMode_on = 0;
	  RGB_MCU();
	  while (learningMode_on < 3)
	  {

		WS2812_ChangeColor(ws28xx_Color_Blue);
		HAL_Delay(300);
	  	WS2812_ChangeColor(ws28xx_Color_Orange);
		HAL_Delay(300);

		  /*** fetching IR data ***/
		  if(irmp_get_data (&irmp_temp_data))
	  	  	{
			  deactivateIR();
			  /*** checking IR repetition ***/
			  if(!(irmp_temp_data.flags & IRMP_FLAG_REPETITION))
			  {
	  		  	  WS2812_ChangeColor(ws28xx_Color_Black);
	  		  	  HAL_Delay(500);
	  		  	  if (learningMode_on == 0)
	  		  	  {
	  		  		  irmp_new_data = irmp_temp_data;
	  		  		  learningMode_on++;
	  		  		  WS2812_ChangeColor(ws28xx_Color_White);

		  			  HAL_Delay(350);
		  			  WS2812_ChangeColor(ws28xx_Color_Black);

		  			  HAL_Delay(350);
	  		  	  }
	  		  	  else
	  		  	  {
	  		  		  if (irmp_new_data.command == irmp_temp_data.command)
	  		  		  {
	  		  			irmp_new_data = irmp_temp_data;
	  		  			learningMode_on++;
	  		  			  WS2812_ChangeColor(ws28xx_Color_White);

	  		  			  HAL_Delay(350);
	  		  			  WS2812_ChangeColor(ws28xx_Color_Black);

	  		  			  HAL_Delay(350);
	  		  		  }
	  		  		  else
	  		  		  {
	  		  			WS2812_ChangeColor(ws28xx_Color_Red);

	  		  			  HAL_Delay(500);
	  		  			WS2812_ChangeColor(ws28xx_Color_Black);

	  		  			  HAL_Delay(350);
	  		  			  learningMode_on = 0;
	  		  		  }
	  		  	  }

	  		  	if (ledMode == 0)
	  		  	{
	  		  		WS2812_ChangeColor(ws28xx_Color_Green);
	  		  	}

	  		  	else
	  		  	{
	  		  	WS2812_ChangeColor(ws28xx_Color_Green);
	  		  	HAL_Delay(500);
	  		  	WS2812_ChangeColor(ws28xx_Color_Black);
	  		  	}
	  		  	irmp_data = irmp_temp_data;
	  		  	memset(&irmp_temp_data, 0, sizeof(IRMP_DATA));
	  	  	}
			activateIR();
	  	  }
	  }
	deactivateIR();
	flashConfig();
	HAL_Delay(2000);
	RGB_RPi();
	memset(&irmp_temp_data, 0, sizeof(IRMP_DATA));
}



void setButtonPressed()
{
	button = 1;
}

void setTimerReset()
{
	if (timer <= 0)
	{
		HAL_TIM_Base_Stop_IT(&htim16);
	}

	timer--;
}


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
