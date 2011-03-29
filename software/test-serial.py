#!/usr/bin/python

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

port = '/dev/ttyUSB0'
baud = 9600

SerialPort(EduBrmSerial(), port, reactor, baud)
reactor.run()
