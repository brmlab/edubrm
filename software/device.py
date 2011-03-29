from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineOnlyReceiver

class EduBrmSerial(LineOnlyReceiver):

    def dataReceived(self, data):
        print 'dataReceived', data

    def lineReceived(self, line):
        print 'lineReceived', data

    def sendLine(self, line):
        pass

class Device:

    def __init__(self, port, baud = 9600):
        SerialPort(EduBrmSerial(), port, reactor, baud)
        reactor.run()

    def send(self, *args):
        if not self.ser.isOpen():
            return -1
        return self.ser.write(' '.join(map(str,args)) + '\n')

    def recv(self):
        if not self.ser.isOpen():
            return None
        return self.ser.readline().strip().split(' ')

    """
    Ping the device

    C> PING
    E> PONG
    """
    def ping(self):
        return self.send('PING') == 'PONG'

    """
    Read version

    C> VERSION
    E> VERSION EDUBRM 1.0.0
    """
    def version(self):
        r = self.send('VERSION')
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
        r = self.send('CFGIO')
        if r and r.startswith('CFGIO '):
            return r[6:]
        return None

    """
    Configure GPIO

    C> CFGIO iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
    E> CFGIO OK
    """
    def cfgio(self, state):
        r = self.send('CFGIO', state)
        return r == 'CFGIO OK'

    """
    Read all inputs

    C> GETIO
    E> GETIO 10011111111111110111111111111101
    """
    def getio(self):
        r = self.send('GETIO')
        if r and r.startswith('GETIO '):
            return r[6:]
        return None

    """
    Set all outputs to logical 1

    C> SETIO 11111111111111111111111111111111
    E> SETIO OK
    """
    def setio(self, state):
        r = self.send('SETIO', state)
        return r == 'SETIO OK'

    """
    Set all outputs to logical 0

    C> CLRIO 11111111111111111111111111111111
    E> CLRIO OK
    """
    def clrio(self, state):
        r = self.send('CLRIO', state)
        return r == 'CLRIO OK'

    """
    Sending pulse on specified pin of specified duration

    C> PULSE 8 100
    E> PULSE OK
    """
    def pulse(self, pin, duration):
        r = self.send('PULSE', pin, duration)
        return r == 'PULSE OK'
