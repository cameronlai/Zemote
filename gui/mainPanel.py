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

class mainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.core = self.parent.core
        self.channelNum = 6

        # Fixed strings
        self.buttonNames = [
            'Channel 6',
            'Channel 5',
            'Channel 4',
            'Channel 3',
            'Channel 2',
            'Channel 1 (Home)',
            'Volume down',
            'Volume up',
            'Power',
            ]
       
        # Layout
        self.__DoLayout() 

    def __DoLayout(self):
        # Button list
        self.buttonList = wx.ListCtrl(self, size=(300,250),
                                      style=wx.LC_REPORT | wx.BORDER_SUNKEN)    
        self.buttonList.InsertColumn(0,'Buttons or channels', width=150)
        self.buttonList.InsertColumn(1,'No. of commands', width=150)
        for i in range(len(self.buttonNames)):           
            self.buttonList.InsertStringItem(0, self.buttonNames[i])
            self.buttonList.SetStringItem(0, 1, '0')
        self.buttonList.Select(0)

        # Buttons in host software
        self.buttonPanel = wx.Panel(self)
        self.programButton = self.MakeButton('Program')
        self.getAllInfoButton = self.MakeButton('Get All Lengths')
        self.getInfoButton = self.MakeButton('Get Commands')
        self.testButton = self.MakeButton('Test Button')
        self.saveToEEPROMButton = self.MakeButton('Save All')
        self.resetAllButton = self.MakeButton('Reset All')

        # Binding
        self.getAllInfoButton.Bind(wx.EVT_BUTTON, self.OnGetAllInfo)
        self.getInfoButton.Bind(wx.EVT_BUTTON, self.OnGetInfo)
        self.testButton.Bind(wx.EVT_BUTTON, self.OnTest)        
        self.programButton.Bind(wx.EVT_BUTTON, self.OnProgram)        
        self.saveToEEPROMButton.Bind(wx.EVT_BUTTON, self.OnSave)        
        self.resetAllButton.Bind(wx.EVT_BUTTON, self.OnResetAll)

        # Button list sizer
        buttonSizer = wx.GridBagSizer(3,2)
        buttonSizer.AddMany([
            (self.programButton, (1,0)),
            (self.getAllInfoButton, (1,1)),
            (self.testButton, (2,0)),
            (self.getInfoButton, (2,1)),
            (self.saveToEEPROMButton, (3,0)),
            (self.resetAllButton, (3,1)),
        ])
        self.buttonPanel.SetSizer(buttonSizer)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
                ((15,15), 0),
                (self.buttonList, 0, wx.ALIGN_CENTER),
                ((15,15), 0),
                (self.buttonPanel, 0, wx.ALIGN_CENTER),
        ])
        self.SetSizer(sizer)

    def MakeButton(self, inputLabel):
        return wx.Button(self.buttonPanel, name=inputLabel, label=inputLabel, size=(150,30))

    def OnGetAllInfo(self, e):
        if self.core.getAllButtonLength():
            for i in range(len(self.buttonNames)):
                self.buttonList.SetStringItem(i, 1, self.core.SerialBuffer[i].rstrip())

    def UpdateAllCmdLength(self):
        for i in range(len(self.buttonNames)):
            self.buttonList.SetStringItem(i, 1, self.core.SerialBuffer[i].rstrip())

    def OnGetInfo(self, e):
        buttonListIndex = self.buttonList.GetFocusedItem()
        self.core.getButtonInfo(buttonListIndex)

    def OnTest(self, e):
        buttonListIndex = self.buttonList.GetFocusedItem()
        self.core.testButton(buttonListIndex)

    def OnProgram(self, e):
        if not self.core.programMode:            
            buttonListIndex = self.buttonList.GetFocusedItem()
            if self.core.startProgramMode(buttonListIndex):
                self.programButton.SetLabel('Finish')
        else:
            if self.core.endProgramMode():
                self.programButton.SetLabel('Program')

    def OnSave(self, e):
        self.core.saveToEEPROM()

    def OnResetAll(self, e):
        self.core.resetAllToEEPROM()
