#include "config.h"
#include "LPC13xx.h"
#include "ssp.h"

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
