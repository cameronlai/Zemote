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
       
        # Variables
        self.baudRates = ["2400", "9600", "19200", "38400", "57600", "115200", "250000"]
        self.serialPorts = ["COM1"]

        self.__DoLayout()        

    def __DoLayout(self):
        self.refreshButton = wx.Button(self, name='Refresh', label='Refresh')
        self.serialPortsComboBox = wx.ComboBox(self, -1, size=(150, -1), choices=self.serialPorts, style=wx.CB_READONLY)
        self.serialPortsComboBox.SetValue(self.serialPorts[0]) # First serial port
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
        #self.Bind(wx.EVT_COMBOBOX, self.OnSelec)

class button_panel(wx.Panel):
    def __init__(self, parent, serial_queue):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.serial_queue = serial_queue
        
        # Attributes
        self.timer = wx.Timer(self)
        self.timer.Start(300)
        self.channelNum = 6
        self.programMode = False
        self.programCounter = 0
        self.prevConnected = False
       
        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    def __DoLayout(self):
        # Button list
        self.buttonList = wx.ListCtrl(self, size=(200,200),
                                      style=wx.LC_REPORT | wx.BORDER_SUNKEN)    
        self.buttonList.InsertColumn(0, 'Select buttons or channels', width=200)
        for i in range(0, self.channelNum-1):           
            self.buttonList.InsertStringItem(0, 'Channel '+str(self.channelNum-i))
        self.buttonList.InsertStringItem(0, 'Channel 1 (Home)')
        self.buttonList.InsertStringItem(0, 'Volume up')
        self.buttonList.InsertStringItem(0, 'Volume down')
        self.buttonList.InsertStringItem(0, 'Power')

        # Buttons in host software
        buttonPanel = wx.Panel(self)
        self.programButton = wx.Button(buttonPanel, name='Program', label='Program')
        testButton = wx.Button(buttonPanel, -1, name='Test', label='Test Button')
        saveToEEPROMButton = wx.Button(buttonPanel, -1, name='Save', label='Save settings to EEPROM')
        readFromEEPROMButton = wx.Button(buttonPanel, -1, name='Reset', label='Reset settings to EEPROM')

        # Last action status report
        self.lastActionText = wx.StaticText(self, -1, label='Last Action:')
        self.lastActionStatus = wx.StaticText(self, -1, label='Status:')

        # Button list sizer
        buttonSizer = wx.FlexGridSizer(3,2,0,0)
        buttonSizer.AddMany([
                (self.programButton, 0, wx.ALIGN_CENTER),
                (saveToEEPROMButton, 0, wx.ALIGN_CENTER),
                (testButton, 0, wx.ALIGN_CENTER),
                (readFromEEPROMButton, 0, wx.ALIGN_CENTER),        
                ])
        buttonPanel.SetSizer(buttonSizer)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
                (self.buttonList, 0, wx.ALIGN_CENTER),
                ((15,15), 0),
                buttonPanel,
                ((15,15), 0),
                (self.lastActionText, 0, wx.ALIGN_LEFT),
                (self.lastActionStatus, 0, wx.ALIGN_LEFT),
                ])
        self.SetSizer(sizer)

    # Button event hanlder
    def OnButton(self, evt):
        lastActionText = 'Last Action: '
        lastActionStatus = 'Status: '

        if self.serial_queue['connected']:
            btn = evt.GetEventObject()
            btnName = btn.GetName()
            btnLabel = btn.GetLabel()
            lastActionText = lastActionText + btnLabel            
            buttonListIndex = self.buttonList.GetFocusedItem()
            if self.programMode and btnLabel == 'Finish':
                self.serial_queue['snd'].put('F')
                self.programMode = False
                self.programButton.SetLabel('Program')
            if not self.programMode:
                if btnName == 'Program':
                    if btnLabel == 'Program':
                        self.serial_queue['snd'].put('P'+str(buttonListIndex))
                        self.programMode = True
                        self.programButton.SetLabel('Finish')
                elif btnName == 'Test':
                    self.serial_queue['snd'].put('T'+str(buttonListIndex))
                elif btnName == 'Save':
                    self.serial_queue['snd'].put('S0')
                elif btnName == 'Reset':
                    self.serial_queue['snd'].put('R0')
                elif btnName == 'Version':
                    self.serial_queue['snd'].put('V0')
            else:
                lastActionStatus = lastActionStatus + 'Failed, you are in program mode'            
        else:
            lastActionStatus = lastActionStatus + 'Failed, Device is not connected'
            
        self.lastActionText.SetLabel(lastActionText)
        self.lastActionStatus.SetLabel(lastActionStatus)

   # Timer event handler
    def OnTimer(self, evt):
        if not self.prevConnected:
            if self.serial_queue['connected']:
                self.prevConnected = True
                self.serial_queue['snd'].put('V0')
                self.serial_queue['rcv'].get(timeout=5) # Zemote
                version = self.serial_queue['rcv'].get(timeout=5) # Version
                self.lastActionText.SetLabel('Last Action: Check version')
                self.parent.statusBar.SetStatusText('Zemote: Connected, Firmware version: ' + version)
        elif not self.serial_queue['connected']:
            self.prevConnected = False
            self.parent.statusBar.SetStatusText('Zemote: Disconnected')
        
        if not self.serial_queue['rcv'].empty():
            text = self.serial_queue['rcv'].get(timeout=0.1)
            lastActionStatus = 'Status: '
            if '0x' in text:
                    self.programCounter = self.programCounter + 1
                    lastActionStatus = lastActionStatus + str(self.programCounter) + ' / 8'
            elif 'ok' in text:
                if 'P' not in text:
                    lastActionStatus = lastActionStatus + 'Success'
                else:
                    lastActionStatus = lastActionStatus + '0 / 8'
                if 'B' in text:
                    self.lastActionText.SetLabel('Last Action: Finish')
                    lastActionStatus = lastActionStatus + ', Buffer filled'
                    self.programButton.SetLabel('Program')
                    self.programMode = False
                self.programCounter = 0
            elif 'error' in text:
                lastActionStatus = lastActionStatus + 'Failed'
                self.programCounter = 0

            self.lastActionStatus.SetLabel(lastActionStatus)
        
