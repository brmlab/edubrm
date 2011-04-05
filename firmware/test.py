#!/usr/bin/python

import usb
import time

usbdev = usb.core.find(idVendor = 0x1fc9, idProduct = 0x1337)

usbdev.detach_kernel_driver(0)

usbdev.set_configuration()

epo = usb.util.find_descriptor(
          usbdev.get_interface_altsetting(),
          custom_match = lambda e: \
              usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

epi = usb.util.find_descriptor(
          usbdev.get_interface_altsetting(),
          custom_match = lambda e: \
              usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

for i in xrange(1024):
    epo.write('@A')
    epi.read(64)
