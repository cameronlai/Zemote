#!/usr/bin/env python

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
# along with ZemoteHost. If not, see <http://www.gnu.org/licenses/>.

import wx
from ZemoteCore import *
from gui.myMenuBar import myMenuBar
from gui.serialTerminal import serialTerminal
from gui.serialToolBar import serialToolBar
from gui.mainPanel import mainPanel

class zemoteGuiFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Zemote", size=(600, 500))      
        self.SetMinSize((700, 500))
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        
        # Initiate ZemoteCore
        self.core = ZemoteCore()

        # Menu bar
        self.menubar = myMenuBar(self)  
        self.SetMenuBar(self.menubar.menubar)
 
        # Status bar
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetMinHeight(200)

        # Panels
        self.mainPanel = mainPanel(self)
        self.serialToolBar = serialToolBar(self)      
        self.serialTerminal = serialTerminal(self)

        # ZemoteCore - assign call backs
        self.core.setDisplayMsgCallBack(self.serialTerminal.updateTerminal)
        self.core.setDisplayActionCallBack(self.serialToolBar.updateConnectionAction)
        self.core.setDisplayStatusCallBack(self.statusBar.SetStatusText)        
        self.core.setDisplayProgramModeCallBack(self.mainPanel.programButton.SetLabel)
        self.core.setDisplayAllCmdLengthCallBack(self.mainPanel.UpdateAllCmdLength)
        
        # Layout
        botSizer = wx.BoxSizer(wx.HORIZONTAL)
        botSizer.AddMany([
            (self.mainPanel, 1, wx.EXPAND),
            (self.serialTerminal, 1, wx.EXPAND),
            ((15, 15), 0),
        ])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
            (self.serialToolBar, 0),
            (botSizer, 1, wx.EXPAND),
        ])
        self.SetSizer(sizer)

    def OnQuit(self, e):
        self.core.continue_read_thread = False
        self.Destroy()

if __name__ == '__main__':
    APP = wx.App(False)
    FRAME = zemoteGuiFrame(None)
    FRAME.Show()
    APP.MainLoop()
    

