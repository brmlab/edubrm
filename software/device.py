import serial

class Device:

    def __init__(self):
        self.ser = serial.Serial()

    def open(self, tty):
        # (port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, writeTimeout=None, dsrdtr=False, interCharTimeout=None)
        self.ser.port = tty
        self.timeout = 1
        self.ser.open()

    def close(self):
        self.ser.close()

    def command(self, text):
        if not self.ser.isOpen():
            return None
        self.ser.write(text + '\n')
        return self.ser.readline().strip()

    """
    Ping the device

    C> PING
    E> PONG
    """
    def ping(self):
        return self.command('PING') == 'PONG'

    """
    Read version

    C> VERSION
    E> VERSION EDUBRM 1.0.0
    """
    def version(self):
        r = self.command('VERSION')
        if r:
            r = r.split(' ')
            if len(r) == 3 and r[0] == 'VERSION' and r[1] == 'EDUBRM':
                return r[2]
        return None

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
        r = self.command('CFGIO')
        if r and r.startswith('CFGIO '):
            return r[6:]
        return None

    """
    Configure GPIO

    C> CFGIO iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    E> CFGIO OK
    """
    def cfgio(self, state):
        r = self.command('CFGIO %s' % state)
        return r == 'CFGIO OK'

    """
    Read all inputs

    C> GETIO
    E> GETIO 10011111111111110111111111111101
    """
    def getio(self):
        r = self.command('GETIO')
        if r and r.startswith('GETIO '):
            return r[6:]
        return None

    """
    Set all outputs to logical 1

    C> SETIO 11111111111111111111111111111111
    E> SETIO OK
    """
    def setio(self, state):
        r = self.command('SETIO %s' % state)
        return r == 'SETIO OK'

    """
    Set all outputs to logical 0

    C> CLRIO 11111111111111111111111111111111
    E> CLRIO OK
    """
    def clrio(self, state):
        r = self.command('CLRIO %s' % state)
        return r == 'CLRIO OK'

    """
    Sending pulse on specified pin of specified duration

    C> PULSE 8 100
    E> PULSE OK
    """
    def pulse(self, pin, duration):
        r = self.command('PULSE %d %d' % (pin, duration))
        return r == 'PULSE OK'
