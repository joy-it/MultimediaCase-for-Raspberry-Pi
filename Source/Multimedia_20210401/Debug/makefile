################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Drivers/STM32F0xx_HAL_Driver/Src/subdir.mk
-include Core/WS2812/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include Core/IRMP/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
Multimedia_20210401.elf \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
Multimedia_20210401.list \

OBJCOPY_BIN += \
Multimedia_20210401.bin \


# All Target
all: Multimedia_20210401.elf secondary-outputs

# Tool invocations
Multimedia_20210401.elf: $(OBJS) $(USER_OBJS) C:\Users\Design1\Desktop\RB-MultimediaCase01\ Firmware\ fuer\ Kendra\Multimedia_20210401\STM32F030F4PX_FLASH.ld
	arm-none-eabi-gcc -o "Multimedia_20210401.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m0 -T"C:\Users\Design1\Desktop\RB-MultimediaCase01 Firmware fuer Kendra\Multimedia_20210401\STM32F030F4PX_FLASH.ld" --specs=nosys.specs -Wl,-Map="Multimedia_20210401.map" -Wl,--gc-sections -static --specs=nano.specs -mfloat-abi=soft -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

Multimedia_20210401.list: $(EXECUTABLES)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "Multimedia_20210401.list"
	@echo 'Finished building: $@'
	@echo ' '

Multimedia_20210401.bin: $(EXECUTABLES)
	arm-none-eabi-objcopy  -O binary $(EXECUTABLES) "Multimedia_20210401.bin"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) *
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST) $(OBJCOPY_BIN)

.PHONY: all clean dependents
.SECONDARY:

-include ../makefile.targets
