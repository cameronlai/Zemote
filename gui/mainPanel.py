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
        self.TVModeButtonNames = [
            'Power',
            'Volume +',
            'Volume -',
            'Channel 1 (Home)',
            'Channel 2',
            'Channel 3',
            'Channel 4',
            'Channel 5',
            'Channel 6',
            ]
        self.SimpleModeButtonNames = [
            'Power',
            'Volume +',
            'Volume -',
            'Home',
            'Channel +',
            'Channel -',
            ]
        self.modeButtonNumDiff = len(self.TVModeButtonNames) - len(self.SimpleModeButtonNames)    

        # Layout
        self.__DoLayout() 

    def LayoutButtonList(self, buttonNames):
        self.buttonList.ClearAll()
        self.buttonList.InsertColumn(0,'Buttons or channels', width=150)
        self.buttonList.InsertColumn(1,'No. of commands', width=150)
        for i in reversed(range(len(buttonNames))):
            self.buttonList.InsertStringItem(0, buttonNames[i])
            self.buttonList.SetStringItem(0, 1, self.core.buttonLengthList[i])
        self.buttonList.Select(0) 

    def __DoLayout(self):
        # Button list
        self.buttonList = wx.ListCtrl(self, size=(300,250),
                                      style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        # Default to TV Mode
        self.LayoutButtonList(self.TVModeButtonNames)

        # Buttons in host software
        self.buttonPanel = wx.Panel(self)
        self.programButton = self.MakeButton('Program')
        self.getInfoButton = self.MakeButton('Get Commands')
        self.testButton = self.MakeButton('Test Button')
        self.saveToEEPROMButton = self.MakeButton('Save All')
        self.resetAllButton = self.MakeButton('Reset All')
        self.switchModeButton = self.MakeButton('Switch mode')

        # Static text
        self.modeText = wx.TextCtrl(self.buttonPanel, -1, 'Mode: TV', 
                                    size=(125,-1), style=wx.TE_READONLY)

        # Binding
        self.getInfoButton.Bind(wx.EVT_BUTTON, self.OnGetInfo)
        self.testButton.Bind(wx.EVT_BUTTON, self.OnTest)        
        self.programButton.Bind(wx.EVT_BUTTON, self.OnProgram)        
        self.saveToEEPROMButton.Bind(wx.EVT_BUTTON, self.OnSave)        
        self.resetAllButton.Bind(wx.EVT_BUTTON, self.OnResetAll)
        self.switchModeButton.Bind(wx.EVT_BUTTON, self.OnSwitchMode)

        # Button list sizer
        buttonSizer = wx.GridBagSizer(hgap=15, vgap=3)
        buttonSizer.AddMany([
                (self.programButton, (0,0)),
                (self.testButton, (1,0)),
                (self.getInfoButton, (1,1)),
                (self.saveToEEPROMButton, (2,0)),
                (self.resetAllButton, (2,1)),
                (self.switchModeButton, (3,0)),
                (self.modeText, (3,1)),
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

    def UpdateCmdLength(self, btnIdx, value):
        self.buttonList.SetStringItem(btnIdx, 1, value)

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

    def OnSwitchMode(self, e):
        self.core.switchMode()
    
    def UpdateModeText(self):
        if self.core.simpleModeEnabled:
            self.modeText.SetValue('Mode: Simple')
            self.LayoutButtonList(self.SimpleModeButtonNames)
        else:
            self.modeText.SetValue('Mode: TV')
            self.LayoutButtonList(self.TVModeButtonNames)
