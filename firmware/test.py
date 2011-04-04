#!/usr/bin/python

import usb

usbdev = usb.core.find(idVendor=0x1fc9, idProduct=0x0003)

usbdev.set_configuration()

epo = usb.util.find_descriptor(
          usbdev.get_interface_altsetting(),
          custom_match = lambda e: \
              usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

epi = usb.util.find_descriptor(
          usbdev.get_interface_altsetting(),
          custom_match = lambda e: \
              usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

print epo.write('@A')
print epi.read(8)
