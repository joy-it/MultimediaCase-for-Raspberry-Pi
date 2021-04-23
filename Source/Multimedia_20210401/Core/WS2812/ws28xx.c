
#include "ws28xx.h"
#include "stm32f0xx_hal.h"
#include <string.h>



//0xE0,0...			// low speed 0				3  bit=1		21 bit=0				
//0xFC,0...			// low speed 1				6 bit=1     18 bit=0


uint8_t ws28xx_temp[WS28XX_MAX_PIXEL][72];				//72 byte for send a pixel 		( 576 bit)	(24 bit led data * 24 bit spi data)

ws28xx_Data_TypeDef	ws28xxLEDs[WS28XX_MAX_PIXEL];

///////////////////////////////////////////////////////////////////////////////////////////////////////
void	ws28xx_fill_a_bit(uint16_t bit_number,uint8_t bit_value,uint16_t buffer_nember)
{
	uint8_t		idx_bit = 0;
	uint16_t idx_buffer = 0;
	idx_buffer =  bit_number/8;
	idx_bit =	7-(bit_number % 8);
	if(bit_value == 0)
		ws28xx_temp[buffer_nember][idx_buffer] = 	ws28xx_temp[buffer_nember][idx_buffer] & (~(0x01<<idx_bit)) ;
	else	
		ws28xx_temp[buffer_nember][idx_buffer] = 	ws28xx_temp[buffer_nember][idx_buffer] | (0x01<<idx_bit) ;
}
///////////////////////////////////////////////////////////////////////////////////////////////////////
void	ws28xx_set_buffer(uint8_t RGB_bit_number_0_23,uint8_t bit_Value_0_1,uint16_t buffer_nember)
{
	uint16_t fill_bit=RGB_bit_number_0_23*24;
	if(bit_Value_0_1 == 0)
	{
		for(uint8_t i=0; i<3 ; i++)
			ws28xx_fill_a_bit(fill_bit+i,1,buffer_nember);
		for(uint8_t i=3; i<24 ; i++)
			ws28xx_fill_a_bit(fill_bit+i,0,buffer_nember);
	}
	else
	{
		for(uint8_t i=0; i<7 ; i++)
			ws28xx_fill_a_bit(fill_bit+i,1,buffer_nember);
		for(uint8_t i=7; i<24 ; i++)
			ws28xx_fill_a_bit(fill_bit+i,0,buffer_nember);
	}
}
/////////////////////////////////////////////////////////////////////////////////////////////////////// 
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
void	ws28xx_Put_Pixels(ws28xx_Data_TypeDef	*LED_Pixel,uint8_t len)
{
	
	for(uint8_t x=0 ; x<len ;x++)
	{
		for(int8_t i=0; i<8 ; i++){
			ws28xx_set_buffer( i+0 ,(LED_Pixel[x].G & (0x80>>i)) ,x);
			ws28xx_set_buffer( i+8 ,(LED_Pixel[x].R & (0x80>>i)) ,x );
			ws28xx_set_buffer( i+16 ,(LED_Pixel[x].B & (0x80>>i)) ,x);
		}

	}
	
	HAL_SPI_Transmit_DMA(WS28XX_SPI,&ws28xx_temp[0][0],(72)*len);
	
}
/////////////////////////////////////////////////////////////////////////////////////////////////////// 
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
void	ws28xx_Update(void)
{
	
	ws28xx_Put_Pixels(ws28xxLEDs,WS28XX_MAX_PIXEL);	
	
}

/////////////////////////////////////////////////////////////////////////////////////////////////////// 
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////
void	ws28xx_SetColor(uint16_t Pixel,ws28xx_Color_TypeDef Color)
{
	if(Pixel >= WS28XX_MAX_PIXEL )
		return;	

	switch(Color)
		{
			//---------------------
			case ws28xx_Color_Black:
				ws28xxLEDs[Pixel].R = 0;
				ws28xxLEDs[Pixel].G = 0;
				ws28xxLEDs[Pixel].B = 0;
			break;
			//---------------------
			case ws28xx_Color_White:
				ws28xxLEDs[Pixel].R = 255;
				ws28xxLEDs[Pixel].G = 255;
				ws28xxLEDs[Pixel].B = 255;
			break;
			//---------------------
			case ws28xx_Color_Red:
				ws28xxLEDs[Pixel].R = 80;
				ws28xxLEDs[Pixel].G = 0;
				ws28xxLEDs[Pixel].B = 0;
			break;
			//---------------------
			case ws28xx_Color_Green:
				ws28xxLEDs[Pixel].R = 0;
				ws28xxLEDs[Pixel].G = 128;
				ws28xxLEDs[Pixel].B = 0;
			break;
			//---------------------
			case ws28xx_Color_Blue:
				ws28xxLEDs[Pixel].R = 0;
				ws28xxLEDs[Pixel].G = 0;
				ws28xxLEDs[Pixel].B = 255;
			break;
			//---------------------
			case ws28xx_Color_Orange:
				ws28xxLEDs[Pixel].R = 255;
				ws28xxLEDs[Pixel].G = 165;
				ws28xxLEDs[Pixel].B = 0;
			break;
		}
	
}

/////////////////////////////////////////////////////////////////////////////////////////////////////// 
///////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////////

void	ws28xx_fade(ws28xx_Color_TypeDef Color)
{
	for(uint8_t i=0 ; i<=128 ; i++)
	{
		for(uint8_t j=0; j<4; j++)
		{
			if (Color == ws28xx_Color_Green)
			{
				ws28xxLEDs[j].R = 0;
				ws28xxLEDs[j].G = i;
			}
			else if (Color == ws28xx_Color_Red)
			{
				ws28xxLEDs[j].R = i;
				ws28xxLEDs[j].G = 0;
			}

			ws28xxLEDs[j].B = 0;
		}
		ws28xx_Update();
		HAL_Delay(5);
	}

	for(uint8_t i=128 ; i>0 ; i--)
	{
		for(uint8_t j=0; j<4; j++)
		{
			if (Color == ws28xx_Color_Green)
			{
				ws28xxLEDs[j].R = 0;
				ws28xxLEDs[j].G = i;
			}
			else if (Color == ws28xx_Color_Red)
			{
				ws28xxLEDs[j].R = i;
				ws28xxLEDs[j].G = 0;
			}

			ws28xxLEDs[j].B = 0;
		}
		ws28xx_Update();
		HAL_Delay(5);
	}
}
