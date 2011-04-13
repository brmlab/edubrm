import usb

class Device:

    VENDORID  = 0x1fc9
    PRODUCTID = 0x1337
    INSIZE    = 64
    OUTSIZE   = 64

    polling = 0

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
        self.epo.write('p' + chr(which) + chr(duty & 0xff) + chr(duty >> 8))

    # sets dds (wave=square,sine,saw1,saw2), (freq=32bit)
    def dds(self, wavetype, freq):
        self.epo.write('d' + chr(wavetype) + chr(freq & 0xff) + chr((freq >> 8) & 0xff) + chr((freq >> 16) & 0xff) + chr(freq >> 24))

    # set opamp (which=1,2), (chan=6), (mult=16bit)
    def opamp(self, which, chan, mult):
        self.epo.write('m' + chr(which) + chr(chan) + chr(mult & 0xff) + chr(mult >> 8))

    # set switch (which=1..8), state=(0,1)
    def switch(self, which, state):
        self.epo.write('s' + chr(which) + (state and '\x01' or '\x00'))

    # set all switches (which=8bit)
    def switches(self, states):
        self.epo.write('S' + chr(states))

    # clear output (which=8bit)
    def clrout(self, which):
        self.epo.write('o' + chr(which))

    # set output (which=8bit)
    def setout(self, which):
        self.epo.write('O' + chr(which))

    def pollfreq(self, freq):
        self.polling = freq

    def state(self):
        # 4x AD (16 bits) + 8x I
        i = self.epi.read(self.INSIZE)
        return (i[0] + i[1]<<8, i[2] + i[3]<<8, i[4] + i[5]<<8, i[6] + i[7]<<8,
                i[8] & 0x01, i[8] & 0x02, i[8] & 0x04, i[8] & 0x08,
                i[8] & 0x10, i[8] & 0x20, i[8] & 0x40, i[8] & 0x80)
