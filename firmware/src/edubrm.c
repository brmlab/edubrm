#include "config.h"
#include "LPC13xx.h"
#include "ssp.h"
#include "adc.h"

void GetInReport (uint8_t src[], uint32_t length)
{
	uint8_t i;
	uint32_t volatile reg = LPC_USB->CmdCode;
	if (reg & (5<<8)) return;

	for (i=0; i<4; ++i) {
		uint32_t v = ADCRead(i);
		src[i*2  ] = v & 0xff;
		src[i*2+1] = (v>>8) & 0xff;
	}
	// TODO: fix the following - replace IP[i] with real value if input pin (I)
	// src[8] = IP[0] + (IP[1]<<1) + (IP[2]<<2) + (IP[3]<<3) + (IP[4]<<4) + (IP[5]<<5) + (IP[6]<<6) + (IP[7]<<7);
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
			break;
		case 'd':
			wavetype = dst[1];
			freq = dst[2] + (dst[3]<<8) + (dst[4]<<16) + (dst[5]<<24);
			// TODO: set DDS to (wavetype) of (freq) Hz
			break;
		case 'm':
			which = dst[1];
			chan = dst[2];
			mult = dst[3] + (dst[4]<<8);
			// TODO: set opamp (which) on channel (chan) with multiplicator (mult)
			break;
		case 's':
			which = dst[1];
			if (dst[2]) {
				// TODO: set switch (which) to on
			} else {
				// TODO: set switch (which) to off
			}
			break;
		case 'S':
			states = dst[1];
			// TODO: set switches to states
			break;
		case 'o':
			which = dst[1];
			// TODO: set output pins to 0 where indicated by (which)
			break;
		case 'O':
			which = dst[1];
			// TODO: set output pins to 1 where indicated by (which)
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

