/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
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
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f0xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define CTRL_VUSB_Pin GPIO_PIN_0
#define CTRL_VUSB_GPIO_Port GPIOA
#define BUTTON_IN_Pin GPIO_PIN_1
#define BUTTON_IN_GPIO_Port GPIOA
#define BUTTON_IN_EXTI_IRQn EXTI0_1_IRQn
#define RGB_MCU_EN_Pin GPIO_PIN_2
#define RGB_MCU_EN_GPIO_Port GPIOA
#define RGB_RPi_EN_Pin GPIO_PIN_3
#define RGB_RPi_EN_GPIO_Port GPIOA
#define IRMP_Receive_Pin GPIO_PIN_6
#define IRMP_Receive_GPIO_Port GPIOA
#define RGB_MCU_OUT_Pin GPIO_PIN_7
#define RGB_MCU_OUT_GPIO_Port GPIOA
#define ADC_IN_Pin GPIO_PIN_1
#define ADC_IN_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */
char Rx_data[5];
uint8_t RxBuffer;
uint8_t RxCounter;
uint8_t RxComplete;

volatile uint8_t button;
volatile uint8_t timer;
uint8_t powerUP;
intptr_t ledMode;


void setButtonPressed(void);
void setTimerReset(void);

#define irmp_protocol_FlashAdress 0x8007C00
#define irmp_address_FlashAdress 0x8007C10
#define irmp_command_FlashAdress 0x8007C20
#define led_mode_FlashAdress 0x8007C30

#define bootUpTime 5; //in 10sec
#define shutDownTime 1;


/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
