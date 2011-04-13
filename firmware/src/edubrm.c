#include "config.h"
#include "LPC13xx.h"
#include "ssp.h"
#include "adc.h"

#include "chars.h"
#include "pbjt.h"

void GetInReport (uint8_t src[], uint32_t length)
{
	uint32_t volatile reg = LPC_USB->CmdCode;
	if (reg & (5<<8)) return;

	static int j = 0;
	int i;
	for (i = 0; i < USB_INSIZE; ++i) {
		src[i] = 'A' + i + j;
	}
	if (++j>32) j = 0;
}

void SetOutReport (uint8_t dst[], uint32_t length)
{
	uint32_t i;
	switch (dst[0]) {

		case 0x00: // send chars to display
			for (i = 1; dst[i] != 0; ++i) {
				if (dst[i] >= 0x20 && dst[i] <= 0x7F)
				SSPSend((uint8_t *)ASCII[dst[i]-0x20], 5);
				SSPSend((uint8_t *)"\x00", 1);
			}
			break;

		case 0x01: // clear screen (white)
			for (i = 0; i < 84*6; ++i) {
				SSPSend((uint8_t *)"\x00", 1);
			}
			break;

		case 0x02: // clear screen (black)
			for (i = 0; i < 84*6; ++i) {
				SSPSend((uint8_t *)"\xFF", 1);
			}
			break;

		case 0x03:
			switch (dst[1]) {
				case 0: SSPSend(pbjt1, 504); break;
				case 1: SSPSend(pbjt2, 504); break;
				case 2: SSPSend(pbjt3, 504); break;
				case 3: SSPSend(pbjt4, 504); break;
				case 4: SSPSend(pbjt5, 504); break;
				case 5: SSPSend(pbjt6, 504); break;
				case 6: SSPSend(pbjt7, 504); break;
				case 7: SSPSend(pbjt8, 504); break;
			}
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

