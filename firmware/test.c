/*
 * generic_hid.c
 *
 *  Created on: Jan 30, 2011
 *  Author: Jan Axelson
 *
 * Demonstrates communicating with generic HID-class USB devices 
 * using libusb-1.0 (libusb.org).
 * Sends and receives 2-byte reports.
 * Requires: an attached HID-class device that supports 2-byte
 * Input, Output, and Feature reports.
 * The device firmware should respond to a received report by sending a report.
 * Change VENDOR_ID and PRODUCT_ID to match your device's Vendor ID and Product ID.
 * See Lvr.com/hidpage.htm for example device firmware.
 * This firmware is adapted from code provided by Xiaofan.
 * Note: libusb error codes are negative numbers.
 * Compile with the -lusb option.
 */

#include <errno.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <libusb-1.0/libusb.h>

// Change these as needed to match idVendor and idProduct in your device's device descriptor.

static const int VENDOR_ID = 0x1fc9;
static const int PRODUCT_ID = 0x0003;

// Values for bmRequestType in the Setup transaction's Data packet.

static const int INSIZE = 8;
static const int OUTSIZE = 2;
static const int INTERFACE_NUMBER = 0;

// Uses interrupt endpoint 1 IN and OUT:

static const int INTERRUPT_IN_ENDPOINT = 0x81;
static const int INTERRUPT_OUT_ENDPOINT = 0x01;
static const int TIMEOUT_MS = 5000;

int exchange_input_and_output_reports_via_interrupt_transfers(libusb_device_handle *devh);

int main(void)
{
	struct libusb_device_handle *devh = NULL;
	int hid_ready = 0;
	int result = 1;

	result = libusb_init(NULL);
	if (result >= 0)
	{
		devh = libusb_open_device_with_vid_pid(NULL, VENDOR_ID, PRODUCT_ID);

		if (devh != NULL)
		{
			// The HID has been detected.
			// Detach the hidusb driver from the HID to enable using libusb.

			libusb_detach_kernel_driver(devh, 0);
			result = libusb_set_configuration(devh, 1);
			if (result >= 0)
			{
				result = libusb_claim_interface(devh, 0);
				if (result >= 0)
				{
					hid_ready = 1;
				}
				else
				{
					fprintf(stderr, "libusb_claim_interface error %d\n", result);
				}
			}
			else
			{
				fprintf(stderr, "libusb_set_configuration error %d\n", result);
			}
		}
		else
		{
			fprintf(stderr, "Unable to find the HID.\n");
		}
	}
	else
	{
		fprintf(stderr, "Unable to initialize libusb.\n");
	}

	if (hid_ready)
	{
		// Send and receive reports.

		exchange_input_and_output_reports_via_interrupt_transfers(devh);

		// Finished using the HID.

		libusb_release_interface(devh, 0);
	}
	libusb_close(devh);
	libusb_exit(NULL);
	return 0;
}

// Uses interrupt transfers to write an Output report to the HID
// and receive an Input report from the HID.
// Returns - zero on success, libusb error code on failure.

int exchange_input_and_output_reports_via_interrupt_transfers(libusb_device_handle *devh)
{
	int bytes_transferred;
	unsigned char data_in[INSIZE-1];
	unsigned char data_out[OUTSIZE-1];
	int i = 0;;
	int result = 0;;

	// Store data in the output buffer for sending.

	for (i=0;i<OUTSIZE; i++)
	{
		data_out[i] = 0x40+i;
	}
	// Write an Output report to the device.

	result = libusb_interrupt_transfer(
			devh,
			INTERRUPT_OUT_ENDPOINT,
			data_out,
			OUTSIZE,
			&bytes_transferred,
			TIMEOUT_MS);

	if (result >= 0)
	{
	  	printf("Output report data sent via interrupt transfer:\n");
	  	for(i = 0; i < OUTSIZE; i++)
	  	{
	  		printf("%02x ",data_out[i]);
	  	}
	  	printf("\n");

		// Read an Input report from the device.

		result = libusb_interrupt_transfer(
				devh,
				INTERRUPT_IN_ENDPOINT,
				data_in,
				INSIZE,
				&bytes_transferred,
				TIMEOUT_MS);

		if (result >= 0)
		{
			if (bytes_transferred == INSIZE)
			{
			  	printf("Input report received via interrupt transfer:\n");
			  	for(i = 0; i < INSIZE; i++)
			  	{
			  		printf("%02x ",data_in[i]);
			  	}
			  	printf("\n");
			}
			else
			{
				fprintf(stderr, "Error: not all data received in interrupt transfer (%d)\n", result);
				return -1;
			}
		}
		else
		{
			fprintf(stderr, "Error receiving Input report via interrupt transfer %d\n", result);
			return result;
		}
	}
	else
	{
		fprintf(stderr, "Error sending Output report via interrupt transfer %d\n", result);
		return result;
	}
  	return 0;
 }


