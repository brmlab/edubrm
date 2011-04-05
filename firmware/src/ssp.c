#include "LPC13xx.h"
#include "ssp.h"

void SSPSend( char *buf, uint32_t Length )
{
  uint32_t i;
  uint8_t Dummy = Dummy;

  for ( i = 0; i < Length; i++ )
  {
	/* Move on only if NOT busy and TX FIFO not full. */
	while ( (LPC_SSP->SR & (SSPSR_TNF|SSPSR_BSY)) != SSPSR_TNF );
	LPC_SSP->DR = *buf;
	buf++;
#if !LOOPBACK_MODE
	while ( (LPC_SSP->SR & (SSPSR_BSY|SSPSR_RNE)) != SSPSR_RNE );
	/* Whenever a byte is written, MISO FIFO counter increments, Clear FIFO
	on MISO. Otherwise, when SSP0Receive() is called, previous data byte
	is left in the FIFO. */
	Dummy = LPC_SSP->DR;
#else
	/* Wait until the Busy bit is cleared. */
	while ( LPC_SSP->SR & SSPSR_BSY );
#endif
  }
  return;
}

void SSPInit() {
// reset peripherals
LPC_SYSCON->PRESETCTRL |= (0x01<<0); // SSP reset de-asserted
LPC_SYSCON->SYSAHBCLKCTRL |= (0x01<<11); // Enables clock for SSP.
LPC_SYSCON->SSPCLKDIV = 2; // div clock by 2

LPC_IOCON->PIO0_8 &= ~0x07; // ???
LPC_IOCON->PIO0_8 |= 0x01; // MISO

LPC_IOCON->PIO0_9 &= ~0x07; // ???
LPC_IOCON->PIO0_9 |= 0x01; // MOSI

#ifdef __JTAG_DISABLED
LPC_IOCON->SCKLOC = 0x00;
LPC_IOCON->SWCLK_PIO0_10 &= ~0x07;
LPC_IOCON->SWCLK_PIO0_10 |= 0x02;>/* SSP CLK */
#endif

// This register is used to select a pin among three possible choices for the SSP SCK function.
LPC_IOCON->SCKLOC = 1; // Selects SCK function for pin PIO2_11/SCK
LPC_IOCON->PIO2_11 = 1;

// set SSEL as GPIO that the master has total control of the sequence
LPC_IOCON->PIO0_2 &= ~0x07;
LPC_IOCON->PIO0_2 |= 0x01;

// TODO ?????????????????????????????????
LPC_SSP->CR0 = 0x0007;
LPC_SSP->CPSR = 0x02;



LPC_IOCON->PIO0_7 = 0x00; // D/C^
LPC_GPIO0->DIR |= 1 << 7;

LPC_IOCON->PIO2_0 = 0x00; // RES^
LPC_GPIO2->DIR |= 1 << 0;


// SSP Enable with Master mode
LPC_SSP->CR1 = (0x01<<1) | (0x00<<2);

NVIC_EnableIRQ(SSP_IRQn);

/* Set SSPINMS registers to enable interrupts */
/* enable all error related interrupts */
LPC_SSP->IMSC = (0x1<<0) | (0x1<<1);

int i;
// reset
//LPC_GPIO2->MASKED_ACCESS[0x01<<0] = 1 << 0;
//  for (i = 0; i < 100; i++);
//LPC_GPIO2->MASKED_ACCESS[0x01<<0] = 0 << 0;

// select
//LPC_GPIO0->MASKED_ACCESS[0x01<<2] = 0 << 2;
//  for (i = 0; i < 100; i++);

// command
LPC_GPIO0->MASKED_ACCESS[0x01<<7] = 0 << 7;
//  for (i = 0; i < 100; i++);
/*
SSPSend("\x21\xc8\x06\x13\x20\x0c", 6);
// x:0 y:0
SSPSend("\x20\x0c", 2);
SSPSend("\x80\x40", 2);

// data
LPC_GPIO0->MASKED_ACCESS[0x01<<7] = 0 << 7;
// for (i = 0; i < 100; i++);

SSPSend("\x21\xc8\x06\x13\x20\x0c", 6);
  // x:0 y:0
SSPSend("\x20\x0c", 2);


LPC_GPIO0->MASKED_ACCESS[0x01<<7] = 0 << 7;
*/
	  SSPSend("\x21\xc8\x06\x13\x20\x0c", 6);
	  SSPSend("\x80\x40", 2);
	  //SSPSend("\x20\x0c", 2);


LPC_GPIO0->MASKED_ACCESS[0x01<<7] = 1 << 7;

  for (i=0;i<84*48;i++)
	  SSPSend("\x00", 1);

  SSPSend("\x00", 1);
  SSPSend("\x00", 1);

while (1){
  SSPSend("\x7f\x49\x49\x49\x36\x00", 6); // B
  SSPSend("\x7f\x09\x19\x29\x46\x00", 6); // R
  SSPSend("\x7f\x02\x0c\x02\x7f\x00", 6); // M
  SSPSend("\x7f\x40\x40\x40\x40\x00", 6); // L
  SSPSend("\x7e\x11\x11\x11\x7e\x00", 6); // A
  SSPSend("\x7f\x49\x49\x49\x36\x00", 6); // B
  SSPSend("\x00\x00\x00\x00\x00\x00\x00", 7);
  for(i=0;i<100000;i++);
}

}
