NAME = edubrm
CFLAGS = -Wall -Werror -D__REDLIB__ -DDEBUG -D__CODE_RED -D__USE_CMSIS=CMSISv1p30_LPC13xx -O0 -g3 -Wall -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb
LDFLAGS = -nostdlib -Xlinker -Map=obj/$(NAME).map --gc-sections -mcpu=cortex-m3 -mthumb -T obj/usb_buffer.ld
LIST = $(shell cd src/ ; ls *.c)
OBJS = $(addprefix obj/,$(LIST:.c=.o))
SRCS = $(addprefix src/,$(LIST))

obj/%.o: src/%.c
	arm-none-eabi-gcc $(CFLAGS) -c $< -o $@

obj/$(NAME).axf: $(OBJS)
	arm-none-eabi-gcc $(LDFLAGS) -o obj/$(NAME).axf $(OBJS)

obj/$(NAME).bin: obj/$(NAME).axf
	arm-none-eabi-size obj/$(NAME).axf
	arm-none-eabi-objcopy -O binary obj/$(NAME).axf obj/$(NAME).bin
	checksum -v obj/$(NAME).bin

clean:
	rm -f obj/*.axf
	rm -f obj/*.bin
	rm -f obj/*.map
	rm -f obj/*.o
	rm -f test

deploy:
	dfu-util -d 0471:df55 -c 0 -t 2048 -R -D /usr/local/LPCXpresso/bin/LPCXpressoWIN.enc || :
	sleep 1
	crt_emu_lpc11_13_nxp -g -2 -pLPC1343 -wire=winusb -info-target
	crt_emu_lpc11_13_nxp -g -2 -pLPC1343 -wire=winusb -flash-erase
	crt_emu_lpc11_13_nxp -g -2 -pLPC1343 -wire=winusb -flash-load=obj/$(NAME).axf

test: test.c
	gcc test.c -o test -lusb-1.0 -Wall -Werror
