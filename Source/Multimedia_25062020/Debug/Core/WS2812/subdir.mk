################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/WS2812/ws28xx.c 

OBJS += \
./Core/WS2812/ws28xx.o 

C_DEPS += \
./Core/WS2812/ws28xx.d 


# Each subdirectory must supply rules for building sources it contributes
Core/WS2812/ws28xx.o: ../Core/WS2812/ws28xx.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F030x6 -DDEBUG -c -I"Y:/Produkte/#RB-MultimediaCase01/Software/Multimedia_30062020/Source/Multimedia_25062020/Core/IRMP" -I../Drivers/STM32F0xx_HAL_Driver/Inc -I../Drivers/CMSIS/Include -I../Core/Inc -I../Drivers/STM32F0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F0xx/Include -I"Y:/Produkte/#RB-MultimediaCase01/Software/Multimedia_30062020/Source/Multimedia_25062020/Core/WS2812" -Os -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"Core/WS2812/ws28xx.d" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

