# This file is part of ZemoteHost.
# 
# ZemoteHost is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ZemoteHost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ZemoteHost.  If not, see <http://www.gnu.org/licenses/>.

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
        self.OnRefresh(None)
        self.baudRatesComboBox = wx.ComboBox(self, -1, size=(150, -1), choices=self.baudRates, style=wx.CB_READONLY)
        self.baudRatesComboBox.SetValue(self.baudRates[1]) # 9600
        self.connectButton = wx.Button(self, name='Connect', label='Connect')      

        # Binding
        self.connectButton.Bind(wx.EVT_BUTTON, self.OnConnect)
        self.refreshButton.Bind(wx.EVT_BUTTON, self.OnRefresh)

        # Sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([
            (self.refreshButton, 0),
            (self.serialPortsComboBox, 0),
            (self.baudRatesComboBox, 0),
            (self.connectButton, 0),
        ])
        self.SetSizer(sizer)        
    
    def OnRefresh(self, e):
        self.serialPortsComboBox.Clear()
        self.serialPorts = self.core.scanSerialPort()
        if len(self.serialPorts) > 0:
            for i in range(len(self.serialPorts)):
                self.serialPortsComboBox.Append(self.serialPorts[i])
            self.serialPortsComboBox.SetValue(self.serialPorts[0]) # First serial port     
        else:
            self.serialPortsComboBox.Clear()
            self.serialPortsComboBox.SetValue('')

    def OnConnect(self, e):
        if self.core.connected:
            self.core.disconnect()
        else:
            port = self.serialPortsComboBox.GetValue()
            baudRate = self.baudRatesComboBox.GetValue()
            self.core.connect(port, baudRate)

    def updateConnectionAction(self, label):
        self.connectButton.SetLabel(label)
