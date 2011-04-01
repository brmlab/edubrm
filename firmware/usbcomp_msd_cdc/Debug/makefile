################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: usbcomp_msd_cdc.axf

# Tool invocations
usbcomp_msd_cdc.axf: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: MCU Linker'
	arm-none-eabi-gcc -nostdlib -L"/home/btr/lpc_xpresso/CMSISv1p30_LPC13xx/Debug" -Xlinker -Map=usbcomp_msd_cdc.map -Xlinker --gc-sections -mcpu=cortex-m3 -mthumb -T "usbcomp_msd_cdc_Debug.ld" -o"usbcomp_msd_cdc.axf" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '
	$(MAKE) --no-print-directory post-build

# Other Targets
clean:
	-$(RM) $(OBJS)$(C_DEPS)$(EXECUTABLES) usbcomp_msd_cdc.axf
	-@echo ' '

post-build:
	-@echo 'Performing post-build steps'
	-arm-none-eabi-size usbcomp_msd_cdc.axf; arm-none-eabi-objcopy -O binary usbcomp_msd_cdc.axf usbcomp_msd_cdc.bin; checksum -v usbcomp_msd_cdc.bin;
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY: post-build

-include ../makefile.targets
