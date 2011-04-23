class Device:

    VENDORID  = 0x1fc9
    PRODUCTID = 0x1337
    INSIZE    = 64
    OUTSIZE   = 64

    def __init__(self, fake = False):
        self.fake = fake
        if not fake:
            import usb
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
        else:
            print 'device init'

    # sets pwm (which=1,2), (duty=16bit)
    def pwm(self, which, duty):
        if self.fake:
            print 'pwm', which, duty
        else:
            duty = 65535 - duty
            self.epo.write('p' + chr(which) + chr(duty & 0xff) + chr(duty >> 8))

    # sets ddswave (wave=square,sine,saw1,saw2)
    def ddswave(self, wavetype):
        if self.fake:
            print 'dds wave', wavetype
        else:
            self.epo.write('d' + chr(wavetype))

    # sets ddsfreq (freq=32bit)
    def ddsfreq(self, freq):
        if self.fake:
            print 'dds freq', freq
        else:
            self.epo.write('D' + chr(freq & 0xff) + chr((freq >> 8) & 0xff) + chr((freq >> 16) & 0xff) + chr(freq >> 24))

    # set opamp (which=1,2), (chan=1..6), (gain=1, 2, 4, 5, 8, 10, 16, 32)
    def opamp(self, which, chan, gain):
        if self.fake:
            print 'opamp', which, chan, gain
        else:
            self.epo.write('m' + chr(which) + chr(chan) + chr(gain))

    # set all switches (states=6bit)
    def switches(self, states):
        if self.fake:
            print 'switches', states
        else:
            self.epo.write('s' + chr(states))

    # set pins state (states=3bit) (1 = input, 0 = output)
    def setpins(self, states):
        if self.fake:
            print 'setpins', states
        else:
            self.epo.write('P' + chr(states))

    # set output (which=1,2,3), (state=0,1)
    def setout(self, which, state):
        if self.fake:
            print 'setout', which, state
        else:
            self.epo.write('o' + chr(which<<1 + state))

    # 7x AD (16 bits) + 3 x I
    def read(self):
        if self.fake:
            from random import randint
            return (randint(0,65535),                                       # AD0
                    randint(0,65535), randint(0,65535), randint(0,65535),   # AD1 .. AD3
                    randint(0,65535), randint(0,65535), randint(0,65535),   # AD4 .. AD6
                    randint(0,7))                                           # IO1 .. IO3
        else:
            i = self.epi.read(self.INSIZE)
            return (i[0] + i[1]<<8,                                         # AD0
                    i[2] + i[3]<<8, i[4] + i[5]<<8, i[6] + i[7]<<8,         # AD1 .. AD3
                    i[9] + i[9]<<8, i[10] + i[11]<<8, i[12] + i[13]<<8,     # AD4 .. AD6
                    i[14] & 0x01, (i[14] & 0x02) >> 1, (i[14] & 0x04) >> 2) # IO1 .. IO3
