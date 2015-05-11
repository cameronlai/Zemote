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

import wx

from zemoteCore import *

# gui
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
    print "hello"
    APP = wx.App(False)
    FRAME = zemoteGuiFrame(None)
    FRAME.Show()
    APP.MainLoop()
    

