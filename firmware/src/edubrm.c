#include "LPC13xx.h"
#include "type.h"

#include "usb.h"
#include "usbcfg.h"
#include "usbhw.h"
#include "usbcore.h"
#include "cdc.h"
#include "cdcuser.h"
#include "serial.h"
#include "vcomdemo.h"
#include "mscuser.h"
#include "memory.h"
#include "stdio.h"
#include "string.h"

#include "edubrm.h"


#define mainLED_BIT 						( 7 )

void VCOM_Brm2Usb() {
/*
  static char serBuf [USB_CDC_BUFSIZE];
  int  numBytesRead, numAvailByte;


  serBuf[0] = 'A';
  numBytesRead = 1;

  ser_AvailChar (&numAvailByte);
  if (numAvailByte > 0) {
    if (CDC_DepInEmpty) {
      numBytesRead = ser_Read (&serBuf[0], &numAvailByte);

      CDC_DepInEmpty = 0;

	  USB_WriteEP (CDC_DEP_IN, (unsigned char *)&serBuf[0], numBytesRead);
    }
  }
*/

}

static char cmdInbuffer[256];
int cmdInbufferIndex = 0;

int checkForCommand() {
	int i=0;
    for (i=0;i<cmdInbufferIndex;i++) {
  	  if (cmdInbuffer[i] == '\n' ) {
  		  return i;
  	  }
    }
    return 0;
}


static unsigned long ulLEDState = 1;

void enableLED() {
	LPC_GPIO0->DIR |= ( 0x1 << mainLED_BIT );
}

void disableLED() {
	LPC_GPIO0->DIR |= ( 0x0 << mainLED_BIT );
}

void toggleLED() {
	  ulLEDState = !ulLEDState;
	  LPC_GPIO0->MASKED_ACCESS[ ( 1 << mainLED_BIT) ] = ( ulLEDState << mainLED_BIT );

}

void sendToUSB(char *string) {
	  USB_WriteEP (CDC_DEP_IN, (unsigned char *)string, strlen(string));
}


void commandReceived(char * receivedCommand) {

  if (strcmp("PING", receivedCommand) == 0) {
	  //echo back
	  sendToUSB("PONG\n");
	  toggleLED();
  } else if (strcmp("VERSION", receivedCommand) == 0) {
	  sendToUSB(VERSION);
	  toggleLED();
  }
}



void VCOM_Usb2Brm() {
  static char serBuf [32];
  int  numBytesToRead, numBytesRead, numAvailByte;
  int i=0;
  static char receivedCommand[128];

  CDC_OutBufAvailChar (&numAvailByte);
  if (numAvailByte > 0) {
      numBytesToRead = numAvailByte > 32 ? 32 : numAvailByte;
      numBytesRead = CDC_RdOutBuf (&serBuf[0], &numBytesToRead);
      for (i=0;i<numBytesRead;i++) { //TODO: replace with memcpy
    	  cmdInbuffer[cmdInbufferIndex++] = serBuf[i];
      }
      int command = checkForCommand();
      if (command != 0) {
    	  //there is some command
    	  cmdInbufferIndex = 0;
    	  memset(receivedCommand,sizeof(receivedCommand), 0);
    	  memcpy(receivedCommand, (unsigned char *)&cmdInbuffer[0], command);
    	  //USB_WriteEP (CDC_DEP_IN, (unsigned char *)&cmdInbuffer[0], command);
    	  commandReceived(receivedCommand);
      }
  }
}

