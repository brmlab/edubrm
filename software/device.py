import usb

class Device:

    VENDORID  = 0x1fc9
    PRODUCTID = 0x1337
    INSIZE    = 64
    OUTSIZE   = 64

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

    # sets pwm (which=1,2), (duty=16bit)
    def pwm(self, which, duty):
        duty = 65535 - duty
        self.epo.write('p' + chr(which) + chr(duty & 0xff) + chr(duty >> 8))

    # sets ddswave (wave=square,sine,saw1,saw2)
    def ddswave(self, wavetype):
        self.epo.write('d' + chr(wavetype))

    # sets ddsfreq (freq=32bit)
    def ddsfreq(self, freq):
        self.epo.write('D' + chr(freq & 0xff) + chr((freq >> 8) & 0xff) + chr((freq >> 16) & 0xff) + chr(freq >> 24))

    # set opamp (which=1,2), (chan=1..6), (gain=1, 2, 4, 5, 8, 10, 16, 32)
    def opamp(self, which, chan, gain):
        self.epo.write('m' + chr(which) + chr(chan) + chr(gain))

    # set all switches (states=6bit)
    def switches(self, states):
        self.epo.write('s' + chr(states))

    # set pins state (states=3bit) (1 = input, 0 = output)
    def setpins(self, states):
        self.epo.write('P' + chr(states))

    # set output (which=1,2,3), (state=0,1)
    def setout(self, which, state):
        self.epo.write('o' + chr(which<<1 + state))

    def read(self):
        # 6x AD (16 bits) + 3 x I
        i = self.epi.read(self.INSIZE)
        return (i[0] + i[1]<<8, i[2] + i[3]<<8, i[4] + i[5]<<8,
                i[6] + i[7]<<8, i[9] + i[9]<<8, i[10] + i[11]<<8,
                i[12] & 0x01, (i[12] & 0x02) >> 1, (i[12] & 0x04) >> 2)
