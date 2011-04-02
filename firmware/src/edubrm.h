#ifndef EDUBRM_H
#define EDUBRM_H

#define VERSION "0.0000001 pre-alpha\n"


void VCOM_Brm2Usb();
int checkForCommand();
void enableLED();
void disableLED();
void toggleLED();
void sendToUSB(char *string);
void commandReceived(char * receivedCommand);
void VCOM_Usb2Brm();


#endif
