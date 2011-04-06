#!/usr/bin/python

import usb
import time

usbdev = usb.core.find(idVendor = 0x1fc9, idProduct = 0x1337)

try:
    usbdev.detach_kernel_driver(0)
except:
    pass

usbdev.set_configuration()

epo = usb.util.find_descriptor(
          usbdev.get_interface_altsetting(),
          custom_match = lambda e: \
              usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

epi = usb.util.find_descriptor(
          usbdev.get_interface_altsetting(),
          custom_match = lambda e: \
              usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

# print epi.read(64)

epo.write('\x00              \x00')
epo.write('\x00 Hackerspace  \x00')
epo.write('\x00   brmlab     \x00')
epo.write('\x00              \x00')
epo.write('\x00   PRESENTS   \x00')
epo.write('\x00              \x00')

time.sleep(1.5)

epo.write('\x00              \x00')
epo.write('\x00 PEANUT       \x00')
epo.write('\x00       BUTTER \x00')
epo.write('\x00 JELLY        \x00')
epo.write('\x00        TIME! \x00')
epo.write('\x00              \x00')

time.sleep(1.7)

epo.write('\x00              \x00')
epo.write('\x00       PEANUT \x00')
epo.write('\x00 BUTTER       \x00')
epo.write('\x00        JELLY \x00')
epo.write('\x00 TIME!        \x00')
epo.write('\x00              \x00')

time.sleep(1.7)

epo.write('\x00              \x00')
epo.write('\x00 PEANUT       \x00')
epo.write('\x00       BUTTER \x00')
epo.write('\x00 JELLY        \x00')
epo.write('\x00        TIME! \x00')
epo.write('\x00              \x00')

time.sleep(1.45)

# for i in xrange(100):
#    epo.write('\x01')
#    epo.write('\x02')

while 1:
    for i in xrange(8):
        time.sleep(0.1)
        epo.write('\x03'+chr(i))
