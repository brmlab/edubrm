################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/DiskImg.c \
../src/cdcuser.c \
../src/clkconfig.c \
../src/cr_startup_lpc13.c \
../src/edubrm.c \
../src/mscuser.c \
../src/serial.c \
../src/usbcomp.c \
../src/usbcore.c \
../src/usbdesc.c \
../src/usbhw.c \
../src/usbuser.c 

OBJS += \
./src/DiskImg.o \
./src/cdcuser.o \
./src/clkconfig.o \
./src/cr_startup_lpc13.o \
./src/edubrm.o \
./src/mscuser.o \
./src/serial.o \
./src/usbcomp.o \
./src/usbcore.o \
./src/usbdesc.o \
./src/usbhw.o \
./src/usbuser.o 

C_DEPS += \
./src/DiskImg.d \
./src/cdcuser.d \
./src/clkconfig.d \
./src/cr_startup_lpc13.d \
./src/edubrm.d \
./src/mscuser.d \
./src/serial.d \
./src/usbcomp.d \
./src/usbcore.d \
./src/usbdesc.d \
./src/usbhw.d \
./src/usbuser.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__REDLIB__ -DDEBUG -D__CODE_RED -D__USE_CMSIS=CMSISv1p30_LPC13xx -I"/home/btr/lpc_xpresso/CMSISv1p30_LPC13xx/inc" -I"/home/btr/lpc_xpresso/usbcomp_msd_cdc/inc" -O0 -g3 -Wall -c -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


