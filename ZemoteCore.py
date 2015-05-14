#!/usr/bin/env python
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
import time
import wx

class ZemoteCore():
    def __init__(self):
        self.title = 'Zemote'
        self.s = None
        self.read_thread = None
        self.debug = True
        self.connected = False
        self.port = None
        self.baudrate = None

        self.read_thread = None
        self.continue_read_thread = False
        self.read_thread_buffer = None

        self.programMode = False

        self.SerialBuffer = []
        self.SerialBufferTargetLen = 0

        # Call back functions for UI
        self.display_msg_cb = None # Call back function for line read from serial port        
        self.display_connection_action_cb = None # Call back for connection action
        self.display_status_cb = None # Call back for status bar update
        self.display_program_mode_cb = None # Call back for program button

    def connect(self, port = None, baudrate = None):
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate
        if self.port is not None and self.baudrate is not None:
            try:                
                self.s = serial.Serial(self.port, self.baudrate, timeout=1)
                self.connected = True
                # Read thread
                self.continue_read_thread = True        
                self.read_thread = threading.Thread(target = self._listen)
                self.read_thread.start()
                time.sleep(1)
                # UI
                wx.CallAfter(self.display_connection_action_cb, 'Disconnect')
                wx.CallAfter(self.display_status_cb, self.title + ' is connected!')
                if self.debug:
                    print('Serial device is connected!')                
                return True
            except:
                if self.debug:
                    print('Serial device cannot be connected!')
                return False
    
    def disconnect(self):
        try:
            self.s.close()
            self.connected = False
            # Read thread
            self.continue_read_thread = False
            if self.read_thread:
                if threading.current_thread() != self.read_thread:
                    self.read_thread.join()
            # UI
            wx.CallAfter(self.display_connection_action_cb, 'Connect')
            wx.CallAfter(self.display_status_cb, self.title + ' is disconnected!')
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
            wx.CallAfter(self.display_msg_cb, '>>> ' + sendCmd)
            if self.debug:
                print 'SND:' + cmd
            return True
        except:
            if not self.connected:
                wx.CallAfter(self.display_status_cb, self.title + ' is not connected')
            else:
                wx.CallAfter(self.display_status_cb, 'Fail to write to ' + self.title)            
            return False

    def _listen(self):
        while self.continue_read_thread:
            try:
                line = self.s.readline()
                if line is not '':     
                    if self.SerialBufferTargetLen > 0:
                        self.SerialBuffer.append(line)
                        self.SerialBufferTargetLen -= 1
                    wx.CallAfter(self.display_msg_cb, line)
                    if 'ok - F' in line: # end of program mode
                        self.programMode = False
                        wx.CallAfter(self.display_program_mode_cb, 'Program')
                    if self.debug:
                        print 'RCV:' + line
            except:                
                self.disconnect()
                if self.debug:
                    print('Failed to receive from serial device. Disconnected.')
                continue               

    # Centralized UI Call back functions

    def setDisplayMsgCallBack(self, function):
        self.display_msg_cb = function

    def setDisplayActionCallBack(self, function):
        self.display_connection_action_cb = function

    def setDisplayStatusCallBack(self, function):
        self.display_status_cb = function

    def setDisplayProgramModeCallBack(self, function):
        self.display_program_mode_cb = function

    # All functions below are based on pre-defined protocols

    def startProgramMode(self, btnIndex):
        ret = self.send('P'+str(btnIndex))
        if ret:
            self.programMode = True
        return ret

    def endProgramMode(self):        
        ret = self.send('F')
        if ret:
            self.programMode = False
        return ret
            
    def getAllButtonLength(self):
        self.SerialBufferTargetLen = 9 # number of soft buttons
        self.SerialBuffer = []
        ret = self.send('L')
        if ret:
            while(self.SerialBufferTargetLen > 0):
                pass
        return ret

    def getButtonInfo(self, btnIndex):
        return self.send('G' + str(btnIndex))

    def testButton(self, btnIndex):
        return self.send('T'+str(btnIndex))

    def saveToEEPROM(self):
        return self.send('S')
    
    def resetAllToEEPROM(self):
        return self.send('R')



