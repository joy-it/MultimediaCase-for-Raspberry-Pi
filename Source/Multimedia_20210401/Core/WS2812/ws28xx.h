#ifndef	_WS28XX_H
#define	_WS28XX_H


#include "stm32f0xx_hal.h"
#include "main.h"


// init SPI @ 10.0 MHZ				SPI mode:MSB first				enable DMA:Normal mode    data width:Byte
//	output @ MOSI 
//	test with WS2811S

SPI_HandleTypeDef hspi1;

#define			WS28XX_MAX_PIXEL								4
#define			WS28XX_SPI											&hspi1


typedef	struct
{
	uint8_t			R	:	8	;
	uint8_t			G	:	8	;
	uint8_t			B	:	8	;
	
}ws28xx_Data_TypeDef;


typedef	enum
{
	ws28xx_Color_Black	=	0  	,
	ws28xx_Color_Red				 	,
	ws28xx_Color_Green			 	,
	ws28xx_Color_Blue					,	
	ws28xx_Color_Orange				,	
	ws28xx_Color_White	 			,
	
}ws28xx_Color_TypeDef;




extern ws28xx_Data_TypeDef	ws28xxLEDs[WS28XX_MAX_PIXEL];

void	ws28xx_Put_Pixels(ws28xx_Data_TypeDef	*LED_Pixel,uint8_t len);
void	ws28xx_Update(void);



// execute  ws28xx_Update() to see														
void	ws28xx_SetColor(uint16_t Pixel,ws28xx_Color_TypeDef Color);
void	ws28xx_fade(ws28xx_Color_TypeDef Color);
#endif
