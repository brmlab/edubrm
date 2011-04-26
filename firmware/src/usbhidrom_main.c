/*----------------------------------------------------------------------------
 *      Name:    DEMO.C
 *      Purpose: USB HID Demo
 *      Version: V1.20
 *----------------------------------------------------------------------------
 *      This software is supplied "AS IS" without any warranties, express,
 *      implied or statutory, including but not limited to the implied
 *      warranties of fitness for purpose, satisfactory quality and
 *      noninfringement. Keil extends you a royalty-free right to reproduce
 *      and distribute executable files created using this software for use
 *      on NXP Semiconductors LPC microcontroller devices only. Nothing else 
 *      gives you the right to use this software.
 *
 * Copyright (c) 2009 Keil - An ARM Company. All rights reserved.
 *---------------------------------------------------------------------------*/

#include "LPC13xx.h"                        /* LPC13xx definitions */

#include "usb.h"
#include "usbdesc.h"
#include "gpio.h"
#include "rom_drivers.h"
#include "config.h"
#include "ssp.h"
#include "adc.h"
#include "edubrm.h"

#define     EN_TIMER32_1    (1<<10)
#define     EN_IOCON        (1<<16)
#define     EN_USBREG       (1<<14)

USB_DEV_INFO DeviceInfo;
HID_DEVICE_INFO HidDevInfo;
ROM ** rom = (ROM **)0x1fff1ff8;

int main (void)
{
	/* for delay loop */
	volatile uint32_t n;
// Code Red Red Suite and LPCXpresso by Code Red both call SystemInit() in
// the C startup code
//#ifndef __CODERED__
  SystemInit();
//#endif

  // enable read on pin PIO3_3
  // LPC_GPIO3->DIR &= ~(1<<3);

  HidDevInfo.idVendor = USB_VENDOR_ID;
  HidDevInfo.idProduct = USB_PROD_ID;
  HidDevInfo.bcdDevice = USB_DEVICE; 
  HidDevInfo.StrDescPtr = (uint32_t)&USB_StringDescriptor[0];
  HidDevInfo.InReportCount = USB_INSIZE;
  HidDevInfo.OutReportCount = USB_OUTSIZE;
  HidDevInfo.SampleInterval = 1;
  HidDevInfo.InReport = GetInReport;
  HidDevInfo.OutReport = SetOutReport;

  DeviceInfo.DevType = USB_DEVICE_CLASS_HUMAN_INTERFACE;
  DeviceInfo.DevDetailPtr = (uint32_t)&HidDevInfo;

  /* Enable Timer32_1, IOCON, and USB blocks (for USB ROM driver) */
  LPC_SYSCON->SYSAHBCLKCTRL |= (EN_TIMER32_1 | EN_IOCON | EN_USBREG);

  /* Use pll and pin init function in rom */
  (*rom)->pUSBD->init_clk_pins();

  /* insert a delay between clk init and usb init */
  for (n = 0; n < 75; n++) {}

  (*rom)->pUSBD->init(&DeviceInfo); /* USB Initialization */
  (*rom)->pUSBD->connect(TRUE);     /* USB Connect */

  for (n = 0; n < 75; n++) {}

  LPC_GPIO2->DIR &= ~(1<<0); // pin2
  LPC_GPIO2->DIR &= ~(1<<6); // pin1
  LPC_GPIO2->DIR &= ~(1<<7); // pin3

  LPC_GPIO2->DIR |= (1<<0);
  LPC_GPIO2->DIR |= (1<<6);
  LPC_GPIO2->DIR |= (1<<7);

  LPC_GPIO2->MASKED_ACCESS[1<<0] |= 1<<0;
  LPC_GPIO2->MASKED_ACCESS[1<<6] |= 1<<6;
  LPC_GPIO2->MASKED_ACCESS[1<<7] |= 1<<7;

  EduInit();

  while (1)
	  __WFI();
}

#if defined(__IAR__)
void USBIRQ_IRQHandler()
#else
void USB_IRQHandler()
#endif
{
  (*rom)->pUSBD->isr();
}

void SSP_IRQHandler(void)
{
  while(1)
    {
    }
}
