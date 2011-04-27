#include "config.h"
#include "LPC13xx.h"
#include "ssp.h"
#include "adc.h"
#include "edubrm.h"

void GetInReport (uint8_t src[], uint32_t length)
{
	uint8_t i;
	uint32_t volatile reg = LPC_USB->CmdCode;
	if (reg & (5<<8)) return;

	for (i=0; i<7; ++i) {
		uint32_t v = ADCRead(i);
		src[i*2  ] = v & 0xff;
		src[i*2+1] = (v>>8) & 0xff;
	}
	src[14] = 0;
	src[14] |= (LPC_GPIO2->MASKED_ACCESS[1<<6] & (1<<6)) >> 6;
	src[14] |= (LPC_GPIO2->MASKED_ACCESS[1<<0] & (1<<0)) << 1;
	src[14] |= (LPC_GPIO2->MASKED_ACCESS[1<<7] & (1<<7)) >> 5;
}

void SetOutReport (uint8_t dst[], uint32_t length)
{
	uint8_t which, wavetype, chan, states, gain, state;
	uint16_t duty;
	uint32_t freq;

	switch (dst[0]) {
		case 'p':
			which = dst[1];
			duty = dst[2] + (dst[3]<<8);
			if (which == 1) {
				EnablePWM1(65535, duty);
			} else {
				EnablePWM2(65535, duty);
			}
			break;
		case 'd':
			wavetype = dst[1];
			LPC_GPIO0->MASKED_ACCESS[1<<2] &= ((0<<2) | ~(1<<2));		// set chipselect to 0
			// TODO: set SPI commands
			LPC_GPIO0->MASKED_ACCESS[1<<2] |= (1<<2);					// set chipselect to 1
			break;
		case 'D':
			freq = dst[1] + (dst[2]<<8) + (dst[3]<<16) + (dst[4]<<24);
			LPC_GPIO0->MASKED_ACCESS[1<<2] &= ((0<<2) | ~(1<<2));		// set chipselect to 0
			freq = 0xFFFFFFFF/50000000*freq;
			SSPSend2(0xF8, 0x00);
			SSPSend2(0x33, ((freq & 0xFF000000) >> 24));
			SSPSend2(0x22, ((freq & 0x00FF0000) >> 16));
			SSPSend2(0x31, ((freq & 0x0000FF00) >> 8));
			SSPSend2(0x20, ((freq & 0x000000FF)));
			SSPSend2(0xC0, 0x00);
			LPC_GPIO0->MASKED_ACCESS[1<<2] |= (1<<2);					// set chipselect to 1
			break;
		case 'm':
			which = dst[1];
			chan = dst[2];
			gain = dst[3];
			if (which == 1) {
				LPC_GPIO3->MASKED_ACCESS[1<<3] &= ((0<<3) | ~(1<<3));		// set chipselect to 0
				SSPSend2(0x40, gain); // gain: 000 - 1, 111 - 32
				LPC_GPIO3->MASKED_ACCESS[1<<3] |= (1<<3);					// set chipselect to 1
			} else {
				LPC_GPIO3->MASKED_ACCESS[1<<2] &= ((0<<2) | ~(1<<2));		// set chipselect to 0
				SSPSend2(0x41, chan); // chan: 000 - ch#1, 101 - ch#6
				LPC_GPIO3->MASKED_ACCESS[1<<2] |= (1<<2);					// set chipselect to 1
				for (which = 0; which < 75; which++) {}
				LPC_GPIO3->MASKED_ACCESS[1<<2] &= ((0<<2) | ~(1<<2));		// set chipselect to 0
				SSPSend2(0x40, gain); // gain: 000 - 1, 111 - 32
				LPC_GPIO3->MASKED_ACCESS[1<<2] |= (1<<2);					// set chipselect to 1
			}
			break;
		case 's':
			states = dst[1];
			SwitchesSetup(states);
			break;
		case 'P':
			states = dst[1];
			PinDir(states);
			break;
		case 'o':
			which = dst[1] >> 1;
			state = dst[1] & 0x01;
			PinState(which, state);
			break;
	}
}

void SwitchesSetup(uint8_t states) {
	LPC_GPIO2->MASKED_ACCESS[1<<8] |= ((( states & 0x01) >> 0)<<8);
	LPC_GPIO2->MASKED_ACCESS[1<<8] &= ((((states & 0x01) >> 0)<<8) | ~(1<<8));
	LPC_GPIO2->MASKED_ACCESS[1<<9] |= ((( states & 0x02) >> 1)<<9);
	LPC_GPIO2->MASKED_ACCESS[1<<9] &= ((((states & 0x02) >> 1)<<9) | ~(1<<9));
	LPC_GPIO2->MASKED_ACCESS[1<<10] |= ((( states & 0x04) >> 2)<<10);
	LPC_GPIO2->MASKED_ACCESS[1<<10] &= ((((states & 0x04) >> 2)<<10) | ~(1<<10));
	LPC_GPIO2->MASKED_ACCESS[1<<11] |= ((( states & 0x08) >> 3)<<11);
	LPC_GPIO2->MASKED_ACCESS[1<<11] &= ((((states & 0x08) >> 3)<<11) | ~(1<<11));
	LPC_GPIO3->MASKED_ACCESS[1<<0] |= ((( states & 0x10) >> 4)<<0);
	LPC_GPIO3->MASKED_ACCESS[1<<0] &= ((((states & 0x10) >> 4)<<0) | ~(1<<0));
	LPC_GPIO3->MASKED_ACCESS[1<<1] |= ((( states & 0x20) >> 5)<<1);
	LPC_GPIO3->MASKED_ACCESS[1<<1] &= ((((states & 0x20) >> 5)<<1) | ~(1<<1));
}

void PinInit() {
	// set pins function
	LPC_IOCON->PIO2_0 &= ~0x07;
	LPC_IOCON->PIO2_0 |= 0x00;
	LPC_IOCON->PIO2_6 &= ~0x07;
	LPC_IOCON->PIO2_6 |= 0x00;
	LPC_IOCON->PIO2_7 &= ~0x07;
	LPC_IOCON->PIO2_7 |= 0x00;
	// set switches function
	LPC_IOCON->PIO2_8 &= ~0x07;
	LPC_IOCON->PIO2_8 |= 0x00;
	LPC_IOCON->PIO2_9 &= ~0x07;
	LPC_IOCON->PIO2_9 |= 0x00;
	LPC_IOCON->PIO2_10 &= ~0x07;
	LPC_IOCON->PIO2_10 |= 0x00;
	LPC_IOCON->PIO2_11 &= ~0x07;
	LPC_IOCON->PIO2_11 |= 0x00;
	LPC_IOCON->PIO3_0 &= ~0x07;
	LPC_IOCON->PIO3_0 |= 0x00;
	LPC_IOCON->PIO3_1 &= ~0x07;
	LPC_IOCON->PIO3_1 |= 0x00;
	LPC_GPIO2->DIR |= (1<<8) | (1<<9) | (1<<10) | (1<<11);
	LPC_GPIO3->DIR |= (1<<0) | (1<<1);
	SwitchesSetup(0);

	//set chip select pins function
	LPC_IOCON->PIO0_2 &= ~0x07; // DDS
	LPC_IOCON->PIO0_2 |= 0x00;
	LPC_IOCON->PIO3_3 &= ~0x07; // OPAMP1
	LPC_IOCON->PIO3_3 |= 0x00;
	LPC_IOCON->PIO3_2 &= ~0x07; // OPAMP2
	LPC_IOCON->PIO3_2 |= 0x00;
	LPC_GPIO0->DIR |= (1<<2);
	LPC_GPIO3->DIR |= (1<<2) | (1<<3);

	PinDir(0); // all 3 pins are output 0
	PinState(1, 0);
	PinState(2, 0);
	PinState(3, 0);
}

void EduInit() {
	SSPInit();
	ADCInit(ADC_CLK);
	PinInit();
}

void PinDir(uint16_t mask) {
	mask &= 7;
	mask ^= 7;
	mask = ((mask & 4) << 5) | ((mask & 2) >> 1) | ((mask & 1)<<6);
	LPC_GPIO2->DIR |= mask;
	mask |= ~(1<<0 | 1<<6 | 1<<7);
	LPC_GPIO2->DIR &= mask;

	if (!(mask & (1<<6)))
		PinState(1, 0);

	if (!(mask & (1<<0)))
		PinState(2, 0);

	if (!(mask & (1<<7)))
		PinState(3, 0);

}

void PinState(uint8_t which, uint8_t state) {
	state &= 1;
	which -= 1;
	switch (which) {
		case 0: which = 6; break;
		case 1: which = 0; break;
		case 2: which = 7; break;
	}
	if (which < 0) return;
	LPC_GPIO2->MASKED_ACCESS[1<<which] |= (state<<which);
	LPC_GPIO2->MASKED_ACCESS[1<<which] &= ((state<<which) | ~(1<<which));
}

void TIMER16_1_IRQHandler(void) {
	LPC_TMR16B1->IR = 0xff;
	LPC_GPIO1->DIR ^= 1<<6;
	LPC_TMR16B1->MR0 -= 100;
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

void EnablePWM1(uint32_t period, uint32_t duty) {

	if (!duty) {
		LPC_SYSCON->SYSAHBCLKCTRL &= ~(1<<9); // disable
		return;
	}

	LPC_SYSCON->SYSAHBCLKCTRL |= 1<<9; // Enables clock for 32-bit counter/timer 0.

	LPC_IOCON->PIO1_6 &= ~0x07;
	LPC_IOCON->PIO1_6 |= 0x02; // Selects function CT32B0_MAT0

	LPC_TMR32B0->MR3 = period;
	LPC_TMR32B0->MR0 = duty;

	LPC_TMR32B0->MCR = 1<<10; // Reset on MR3: the TC will be reset if MR3 matches it.

	LPC_TMR32B0->EMR = 3<<4; // Toggle the corresponding External Match bit/output.

	LPC_TMR32B0->PWMC = 1<<0 | 1<<3; // enable PWM

	LPC_TMR32B0->TCR = 1;
}

void EnablePWM2(uint16_t period, uint16_t duty) {

	if (!duty) {
		LPC_SYSCON->SYSAHBCLKCTRL &= ~(1<<8); // disable
		return;
	}

	LPC_SYSCON->SYSAHBCLKCTRL |= 1<<8; // Enables clock for 16-bit counter/timer 1.

	LPC_IOCON->PIO1_9 &= ~0x07;
	LPC_IOCON->PIO1_9 |= 0x01; // Selects function CT16B1_MAT0

	LPC_TMR16B1->MR3 = period;
	LPC_TMR16B1->MR0 = duty;

	LPC_TMR16B1->MCR = 1<<10; // Reset on MR3: the TC will be reset if MR3 matches it.

	LPC_TMR16B1->EMR = 3<<4; // Toggle the corresponding External Match bit/output.

	LPC_TMR16B1->PWMC = 1<<0 | 1<<3; // enable PWM

	LPC_TMR16B1->TCR = 1;
}
