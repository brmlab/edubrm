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
	// TODO: fix the following - replace IP[i] with real value of input pin (I)
	// src[14] = IP[0] + (IP[1]<<1) + (IP[2]<<2);
	src[14] = 0;
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
