CFLAGS  = -D__REDLIB__ -DDEBUG -D__CODE_RED -D__USE_CMSIS=CMSISv1p30_LPC13xx -Iinc -O0 -g3 -Wall -fmessage-length=0 -fno-builtin -ffunction-sections -fdata-sections -mcpu=cortex-m3 -mthumb
LDFLAGS = -nostdlib -Xlinker -Map=obj/edubrm.map --gc-sections -mcpu=cortex-m3 -mthumb -T obj/debug.ld
LIST = $(shell cd src/ ; ls *.c)
OBJS = $(addprefix obj/,$(LIST:.c=.o))
SRCS = $(addprefix src/,$(LIST))

obj/%.o: src/%.c
	arm-none-eabi-gcc $(CFLAGS) -c $< -o $@

obj/edubrm.axf: $(OBJS)
	arm-none-eabi-gcc $(LDFLAGS) -o obj/edubrm.axf $(OBJS)

obj/edubrm.bin: obj/edubrm.axf
	arm-none-eabi-size obj/edubrm.axf
	arm-none-eabi-objcopy -O binary obj/edubrm.axf obj/edubrm.bin
	checksum -v obj/edubrm.bin

clean:
	rm -f obj/*.o obj/edubrm.{axf,bin,map}
