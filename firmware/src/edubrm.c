#include "config.h"
#include "LPC13xx.h"
#include "ssp.h"
#include "adc.h"

void GetInReport (uint8_t src[], uint32_t length)
{
	uint8_t i;
	uint32_t volatile reg = LPC_USB->CmdCode;
	if (reg & (5<<8)) return;

	for (i=0; i<6; ++i) {
		uint32_t v = ADCRead(i);
		src[i*2  ] = v & 0xff;
		src[i*2+1] = (v>>8) & 0xff;
	}
	// TODO: fix the following - replace IP[i] with real value of input pin (I)
	// src[12] = IP[0] + (IP[1]<<1) + (IP[2]<<2);
}

void SetOutReport (uint8_t dst[], uint32_t length)
{
	uint8_t which, wavetype, chan, states;
	uint16_t duty, mult;
	uint32_t freq;

	switch (dst[0]) {
		case 'p':
			which = dst[1];
			duty = dst[2] + (dst[3]<<8);
			// TODO: set PWM (which) to (duty)
			// PWM_1 is PIN_9
			// PWM_2 is PIN_17
			break;
		case 'd':
			wavetype = dst[1];
			// TODO: set DDS to (wavetype) using SPI (set PIN_10 to 0, send SPI commands, set PIN_10 to 1)
			break;
		case 'D':
			freq = dst[1] + (dst[2]<<8) + (dst[3]<<16) + (dst[4]<<24);
			// TODO: set DDS to (freq) Hz using SPI (set PIN_10 to 0, send SPI commands, set PIN_10 to 1)
			break;
		case 'm':
			which = dst[1];
			chan = dst[2];
			gain = dst[3];
			// TODO: set opamp (which) on channel (chan) with gain (gain)
			// for opamp1: set PIN_48 to 0, send SPI commands, set PIN_48 to 1
			// for opamp2: set PIN_43 to 0, send SPI commands, set PIN_43 to 1
			break;
		case 's':
			states = dst[1];
			// TODO: set switches to states
			// switch1: PIN_12
			// switch2: PIN_24
			// switch3: PIN_25
			// switch4: PIN_31
			// switch5: PIN_36
			// switch6: PIN_37
			break;
		case 'P':
			states = dst[1];
			// TODO: set pins to states (1 is INPUT, 0 is OUTPUT)
			// pin1 is PIN_1
			// pin2 is PIN_2
			// pin3 is PIN_11
			break;
		case 'o':
			which = dst[1] >> 1;
			state = dst[1] & 0x01;
			// TODO: set output pins (which) to state (state)
			// pin1 is PIN_1
			// pin2 is PIN_2
			// pin3 is PIN_11
			break;
	}
}

//static uint8_t x = 0;
void TIMER32_0_IRQHandler(void) {
	LPC_TMR32B0->IR = 0xff; // clear interrupt

	/*
	uint32_t x = LPC_TMR32B0->EMR & 1 ? 0xff : 0;
	SSPSend((uint8_t*)&x, 1);
	*/

	/*
	uint32_t x = ADCRead(0);
	uint8_t z = 0;
	if (x >= 0)		z = 0x01;
	if (x >= 32)	z = 0x02;
	if (x >= 64)	z = 0x04;
	if (x >= 96)	z = 0x08;
	if (x >= 128)	z = 0x10;
	if (x >= 160)	z = 0x20;
	if (x >= 192)	z = 0x40;
	if (x >= 256)	z = 0x80;
	z |= 0x80;
	SSPSend(&z, 1);
	*/


	// read PIO3_3
	uint8_t x = LPC_GPIO3->MASKED_ACCESS[1<<3];
	x = (x&(1<<3)) ? 0xff : 0;
	SSPSend(&x, 1);

}

void PWMRun(void) {

	LPC_SYSCON->SYSAHBCLKCTRL |= 1<<9; // Enables clock for 32-bit counter/timer 0.

	LPC_IOCON->PIO1_6 &= ~0x07;
	LPC_IOCON->PIO1_6 |= 0x02; // Selects function CT32B0_MAT0

	LPC_TMR32B0->MR3 = 4294967; // period
	LPC_TMR32B0->MR0 = 4294967/2; // duty

	LPC_TMR32B0->MCR = 1<<10; // Reset on MR3: the TC will be reset if MR3 matches it.

	LPC_TMR32B0->EMR = 3<<4; // Toggle the corresponding External Match bit/output.

	LPC_TMR32B0->PWMC = 1<<0 | 1<<3; // enable pwn

//	LPC_TMR32B0->MCR |=  1<<9| 1<<0; NVIC_EnableIRQ(TIMER_32_0_IRQn);

	LPC_TMR32B0->TCR = 1;
}

