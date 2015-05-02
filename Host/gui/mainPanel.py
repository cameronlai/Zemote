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

class mainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.core = self.parent.core
        self.channelNum = 6
       
        # Layout
        self.__DoLayout() 

    def __DoLayout(self):
        # Button list
        self.buttonList = wx.ListCtrl(self, size=(200,250),
                                      style=wx.LC_REPORT | wx.BORDER_SUNKEN)    
        self.buttonList.InsertColumn(0,'Select buttons or channels', width=200)
        for i in range(0, self.channelNum-1):           
            self.buttonList.InsertStringItem(0, 'Channel ' + str(self.channelNum-i))
        self.buttonList.InsertStringItem(0, 'Channel 1 (Home)')
        self.buttonList.InsertStringItem(0, 'Volume down')
        self.buttonList.InsertStringItem(0, 'Volume up')
        self.buttonList.InsertStringItem(0, 'Power')
        self.buttonList.Select(0)

        # Buttons in host software
        buttonPanel = wx.Panel(self)
        self.programButton = wx.Button(buttonPanel, name='Program', label='Program')
        self.finishButton = wx.Button(buttonPanel, name='Finish', label='Finish')
        self.getInfoButton = wx.Button(buttonPanel, name='Get Info', label='Get Info')
        self.testButton = wx.Button(buttonPanel, -1, name='Test', label='Test')
        self.saveToEEPROMButton = wx.Button(buttonPanel, -1, name='Save', label='Save all')
        self.readFromEEPROMButton = wx.Button(buttonPanel, -1, name='Reset', label='Reset all')

        # Binding
        self.getInfoButton.Bind(wx.EVT_BUTTON, self.OnGetInfo)
        self.testButton.Bind(wx.EVT_BUTTON, self.OnTest)        
        self.programButton.Bind(wx.EVT_BUTTON, self.OnProgram)        
        self.finishButton.Bind(wx.EVT_BUTTON, self.OnFinish)
        self.saveToEEPROMButton.Bind(wx.EVT_BUTTON, self.OnSaveToEEPROM)        
        self.readFromEEPROMButton.Bind(wx.EVT_BUTTON, self.OnReadFromEEPROM)        

        # Button list sizer
        buttonSizer = wx.GridSizer(3,2,10,10)
        buttonSizer.AddMany([
            (self.programButton, 0),
            (self.finishButton, 0),
            (self.testButton, 0),
            (self.getInfoButton, 0),
            (self.saveToEEPROMButton, 0),
            (self.readFromEEPROMButton, 0),
        ])
        buttonPanel.SetSizer(buttonSizer)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
                ((15,15), 0),
                (self.buttonList, 0, wx.ALIGN_CENTER),
                ((15,15), 0),
                (buttonPanel, 0, wx.ALIGN_CENTER),
        ])
        self.SetSizer(sizer)

    def OnGetInfo(self, e):
        buttonListIndex = self.buttonList.GetFocusedItem()
        if not self.core.getButtonInfo(buttonListIndex):
            self.setStatusBarNotConnected()

    def OnTest(self, e):
        buttonListIndex = self.buttonList.GetFocusedItem()
        if not self.core.testButton(buttonListIndex):
            self.setStatusBarNotConnected()

    def OnProgram(self, e):
        buttonListIndex = self.buttonList.GetFocusedItem()
        if not self.core.startProgramMode(buttonListIndex):
            self.setStatusBarNotConnected()

    def OnFinish(self, e):
        if not self.core.endProgramMode():
            self.setStatusBarNotConnected()

    def OnSaveToEEPROM(self, e):
        if not self.core.saveToEEPROM():
            self.setStatusBarNotConnected()

    def OnReadFromEEPROM(self, e):
        buttonListIndex = self.buttonList.GetFocusedItem()

    def setStatusBarNotConnected(self):
        self.parent.statusBar.SetStatusText('Serial device not connected!')
