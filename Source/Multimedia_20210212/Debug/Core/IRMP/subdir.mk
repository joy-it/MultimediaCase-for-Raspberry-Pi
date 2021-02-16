################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/IRMP/irmp.c 

OBJS += \
./Core/IRMP/irmp.o 

C_DEPS += \
./Core/IRMP/irmp.d 


# Each subdirectory must supply rules for building sources it contributes
Core/IRMP/irmp.o: ../Core/IRMP/irmp.c
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0 -std=gnu11 -g3 -DUSE_HAL_DRIVER -DSTM32F030x6 -DDEBUG -c -I"C:/Users/Nils Hoever/Downloads/RB-MultimediaCase01 GitHub/edited/Source/Multimedia_25062020_edited/Core/IRMP" -I../Drivers/STM32F0xx_HAL_Driver/Inc -I../Drivers/CMSIS/Include -I../Core/Inc -I../Drivers/STM32F0xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F0xx/Include -I"C:/Users/Nils Hoever/Downloads/RB-MultimediaCase01 GitHub/edited/Source/Multimedia_25062020_edited/Core/WS2812" -Os -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"Core/IRMP/irmp.d" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

