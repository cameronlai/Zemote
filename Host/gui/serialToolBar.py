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

import wx

class serialToolBar(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.core = self.parent.core
        self.statusBar = self.parent.statusBar
       
        # Variables
        self.baudRates = ["2400", "9600", "19200", "38400", "57600", "115200", "250000"]
        self.serialPorts = []
        self.__DoLayout()        

    def __DoLayout(self):
        self.refreshButton = wx.Button(self, name='Refresh', label='Refresh')
        self.serialPortsComboBox = wx.ComboBox(self, -1, size=(150, -1), style=wx.CB_READONLY)
        self.rescanSerialPorts()
        self.baudRatesComboBox = wx.ComboBox(self, -1, size=(150, -1), choices=self.baudRates, style=wx.CB_READONLY)
        self.baudRatesComboBox.SetValue(self.baudRates[1]) # 9600
        self.connectButton = wx.Button(self, name='Connect', label='Connect')      

        # Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([
            (self.refreshButton, 0),
            (self.serialPortsComboBox, 0),
            (self.baudRatesComboBox, 0),
            (self.connectButton, 0),
        ])
        self.SetSizer(sizer)
        
        # Binding
        self.Bind(wx.EVT_BUTTON, self.OnButton)
    
    def rescanSerialPorts(self):
        self.serialPorts = self.core.scanSerialPort()
        if len(self.serialPorts) > 0:
            for i in range(len(self.serialPorts)):
                self.serialPortsComboBox.Append(self.serialPorts[i])
            self.serialPortsComboBox.SetValue(self.serialPorts[0]) # First serial port     
        else:
            self.serialPortsComboBox.Clear()
            self.serialPortsComboBox.SetValue('')

    def OnButton(self, evt):
        btn = evt.GetEventObject()
        btnName = btn.GetName()
        btnLabel = btn.GetLabel()

        if btnName == 'Connect':
            if self.core.connected:
                if self.core.disconnect():
                    self.connectButton.SetLabel('Connect')
                    self.statusBar.SetStatusText('Disconnected')
            else:
                port = self.serialPortsComboBox.GetValue()
                baudRate = self.baudRatesComboBox.GetValue()
                if self.core.connect(port, baudRate):
                    self.connectButton.SetLabel('Disconnect')
                    self.statusBar.SetStatusText('Connected')
        elif btnName == 'Refresh':
            self.rescanSerialPorts()
