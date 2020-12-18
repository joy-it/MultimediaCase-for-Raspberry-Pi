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

BUILD_ARTIFACT_NAME := Multimedia_25062020
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX := 
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME).$(BUILD_ARTIFACT_EXTENSION)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
Multimedia_25062020.elf \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
Multimedia_25062020.list \

OBJCOPY_BIN += \
Multimedia_25062020.bin \


# All Target
all: main-build

# Main-build Target
main-build: Multimedia_25062020.elf secondary-outputs

# Tool invocations
Multimedia_25062020.elf: $(OBJS) $(USER_OBJS) Y:\Produkte\#RB-MultimediaCase01\Software\Multimedia_30062020\Source\Multimedia_25062020\STM32F030F4PX_FLASH.ld
	arm-none-eabi-gcc -o "Multimedia_25062020.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m0 -T"Y:\Produkte\#RB-MultimediaCase01\Software\Multimedia_30062020\Source\Multimedia_25062020\STM32F030F4PX_FLASH.ld" --specs=nosys.specs -Wl,-Map="Multimedia_25062020.map" -Wl,--gc-sections -static --specs=nano.specs -mfloat-abi=soft -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

Multimedia_25062020.list: $(EXECUTABLES)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "Multimedia_25062020.list"
	@echo 'Finished building: $@'
	@echo ' '

Multimedia_25062020.bin: $(EXECUTABLES)
	arm-none-eabi-objcopy  -O binary $(EXECUTABLES) "Multimedia_25062020.bin"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) *
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST) $(OBJCOPY_BIN)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents fail-specified-linker-script-missing warn-no-linker-script-specified
.SECONDARY:

-include ../makefile.targets
