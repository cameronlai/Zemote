# Zemote
# (C) Copyright 2014 Cameron Lai
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Lesser General Public License
# (LGPL) version 3.0 which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/lgpl-3.0.html
#
# Zemote is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

import time
import threading
import Queue
import serial
from serial.tools import list_ports

class serial_tool(threading.Thread):
    def __init__(self, vendorID, serial_queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.debug = False

        # Queues
        self.serial_queue = serial_queue

        # Serial set up
        self.vendorID = vendorID
        self.connected = False
        self.baudrate = 9600
        #self.port = '/dev/ttyACM0'
        self.port = ''

    def run(self):
        while True:
            if self.connected:
                serial_in = self.receive()
                if serial_in != '':
                    self.serial_queue['rcv'].put(serial_in)
                if not self.serial_queue['snd'].empty():
                    serial_out = self.serial_queue['snd'].get()
                    self.send(serial_out)
            else:
                self.connect()
                time.sleep(2)

    def searchPort(self):
        # Search serial port
        for tmpPort in list_ports.comports():
            if self.vendorID in tmpPort[2]:
                self.port = tmpPort[0]
                if self.debug:
                    print 'Found port at ' + self.port
                return True
        return False
        
    def connect(self):
        # Search serial port
        if not self.searchPort():
            return False
        try:
            self.s = serial.Serial(self.port, self.baudrate, timeout=1)
            if self.debug:
                print('Serial device is connected!')
            self.updateConnectionStatus(True)
            time.sleep(0.5)
            return True
        except:
            if self.debug:
                print('Serial device cannot be connected!')
            self.updateConnectionStatus(False)
            return False
                
    def disconnect(self):
        try:
            self.s.close()
            if self.debug:
                print('Serial device is disconnected!')
            self.updateConnectionStatus(False)
            return True
        except:
            if self.debug:
                print('Serial device cannot be disconnected!')     
            self.updateConnectionStatus(True)
            return False

    def updateConnectionStatus(self, status):
        self.connected = status
        self.serial_queue['connected'] = status

    def send(self, cmd):
        sendCmd = cmd + "\n"
        returnString =''
        try:
            self.s.write(sendCmd.encode())
            if self.debug:
                print 'SND:' + cmd
            return True
        except:
            self.disconnect()
            if self.debug:
                print('Failed to write to the serial device')
            return False

    def receive(self):
        try:
            returnStr = self.s.readline()
            if returnStr:
                if self.debug:
                    print 'RCV:'+ returnStr
                return returnStr
        except:
            self.disconnect()
            if self.debug:
                print('Failed to receive from serial device')            
        return ''
