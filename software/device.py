import usb

class Device:

    VENDORID  = 0x1fc9
    PRODUCTID = 0x1337
    INSIZE    = 64
    OUTSIZE   = 2

    def __init__(self):
        usbdev = usb.core.find(idVendor = self.VENDORID, idProduct = self.PRODUCTID)
        if usbdev == None:
            raise Exception('EduBRM device not found')
        try:
            usbdev.detach_kernel_driver(0)
        except:
            pass
        usbdev.set_configuration()
        self.epo = usb.util.find_descriptor(usbdev.get_interface_altsetting(),
                       custom_match = lambda e: \
                           usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        self.epi = usb.util.find_descriptor(usbdev.get_interface_altsetting(),
                       custom_match = lambda e: \
                           usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

# TODO: PWM
# TODO: SPI
# TODO: SET/CLEAR PINS

    def state(self):
        # TODO: format?
        return self.epi.read(self.INSIZE)
