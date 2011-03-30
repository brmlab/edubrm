import serial

class Device:

    def __init__(self):
        self.sctrl = serial.Serial()
        self.sdata = serial.Serial()

    def open(self, ttyctrl, ttydata):
        self.sctrl.port = ttyctrl
        self.sdata.port = ttydata
        self.sctrl.baudrate = 115200
        self.sdata.baudrate = 921600
        self.sctrl.open()
        self.sdata.open()

    def close(self):
        self.sdata.close()
        self.sctrl.close()

    def cmd(self, buf):
        if not self.sctrl.isOpen():
            return None
        self.sctrl.write(buf+'\n')
        return self.sctrl.readline().strip()

    def send(self, buf):
        if not self.sdata.isOpen():
            return -1
        return self.sdata.write(buf)

    def recv(self, size):
        if not self.sdata.isOpen():
            return None
        return self.sdata.read(size)


    """
    Ping the device

    C> PING
    E> PONG
    """
    def ping(self):
        return self.cmd('PING') == 'PONG'

    """
    Read version

    C> VERSION
    E> VERSION EDUBRM 1.0.0
    """
    def version(self):
        r = self.cmd('VERSION')
        if r and r.startswith('VERSION EDUBRM '):
            return r[15:]
        return None

# TODO: ANALOG PINS
# TODO: PWM
# TODO: SPI

    """
    Read current configuration

    * O = output
    * I = input
    * F = input with glitch filter
    * P = input with pull-up resistor(10kOhm)
    * A = input with pull-up resistor and glitch filter
    * Letter in uppercase means that pin is permitted
    * Letter in lowercase means pin is not permitted

    C> CFGIO
    E> CFGIO FOOOPPPPPPPPPPPPOPfPPPPPPIIioAOP
    """
    def cfgio(self):
        r = self.cmd('CFGIO')
        if r and r.startswith('CFGIO '):
            return r[6:]
        return None

    """
    Configure GPIO

    C> CFGIO iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    E> CFGIO OK
    """
    def cfgio(self, state):
        return self.cmd('CFGIO ' + state) == 'CFGIO OK'

    """
    Read all inputs

    C> GETIO
    E> GETIO 10011111111111110111111111111101
    """
    def getio(self):
        r = self.cmd('GETIO')
        if r and r.startswith('GETIO '):
            return r[6:]
        return None

    """
    Set all outputs to logical 1

    C> SETIO 11111111111111111111111111111111
    E> SETIO OK
    """
    def setio(self, state):
        return self.cmd('SETIO ' + state) == 'SETIO OK'

    """
    Set all outputs to logical 0

    C> CLRIO 11111111111111111111111111111111
    E> CLRIO OK
    """
    def clrio(self, state):
        return self.cmd('CLRIO ' + state) == 'CLRIO OK'

    """
    Set oposite state on specified pin for specified duration

    C> PULSE 8 100
    E> PULSE OK
    """
    def pulse(self, pin, duration):
        return self.cmd('PULSE ' + str(pin) + ' ' + str(duration)) == 'PULSE OK'

    """
    Set data transmission (from PC to mainboard)

    C> DATAUP 10011111111111110111111111111101
    E> DATAUP OK
    """
    def dataup(self, state):
        return self.cmd('DATAUP ' + state) == 'DATAUP OK'

    """
    Set data transmission (from mainboard to PC)

    C> DATADOWN 10011111111111110111111111111101
    E> DATADOWN OK
    """
    def datadown(self, state):
        return self.cmd('DATADOWN ' + state) == 'DATADOWN OK'

    """
    Stop data transmission in both directions

    C> DATASTOP
    E> DATASTOP OK
    """
    def datastop(self):
        return self.cmd('DATASTOP') == 'DATASTOP OK'
