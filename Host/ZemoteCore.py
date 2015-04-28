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

import serial
import glob
import threading
import wx

class ZemoteCore():
    def __init__(self):
        self.s = None
        self.read_thread = None
        self.debug = True
        self.connected = False
        self.port = None
        self.baudrate = None

        self.read_thread = None
        self.read_thread_cb = None # Call back function for line read from serial port
        self.continue_read_thread = False
        self.read_thread_buffer = None

    def connect(self, port = None, baudrate = None):
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate
        if self.port is not None and self.baudrate is not None:
            try:                
                self.s = serial.Serial(self.port, self.baudrate, timeout=1)
                self.connected = True
                # Set up read thread
                self.read_thread = threading.Thread(target = self._listen)
                self.read_thread.start()

                if self.debug:
                    print('Serial device is connected!')                
                return True
            except:
                if self.debug:
                    print('Serial device cannot be connected!')
                return False
        return False
    
    def disconnect(self):
        try:
            self.s.close()
            self.connected = False
            if self.read_thread:
                self.continue_read_thread = False
                if threading.current_thread() != self.read_thread:
                    self.read_thread.join()
            if self.debug:
                print('Serial device is disconnected!')
            return True
        except:
            if self.debug:
                print('Serial device cannot be disconnected!')     
            return False
        
    def scanSerialPort(self):
        portList = []
        for g in ['/dev/ttyUSB*', '/dev/ttyACM*', "/dev/tty.*", "/dev/cu.*", "/dev/rfcomm*"]:
            portList += glob.glob(g)
        if self.debug:
            print portList
        return portList
    
    def send(self, cmd):
        sendCmd = cmd + '\n'
        returnString =''
        try:
            self.s.write(sendCmd.encode())
            displayCmd = 'SND:' + sendCmd
            if self.debug:
                print 'SND:' + cmd
            return displayCmd
        except:
            if self.debug:
                print('Failed to write to the serial device')
            return None

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

    def _listen(self):
        self.continue_read_thread = True
        while self.continue_read_thread:
            try:
                line = self.s.readline()
                if line is not '':
                    print 'RCV:' + line
                    wx.CallAfter(self.read_thread_cb, line)                    
            except:
                continue               
                
        

