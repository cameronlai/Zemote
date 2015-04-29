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
import time
import threading
import Queue
from zemote_gui_panels import *
from ZemoteCore import *

class zemote_gui():
    def __init__(self):
        print 'Zemote Host Initialized'
        APP = wx.App(False)
        FRAME = _zemote_gui_frame(None)
        FRAME.Show()
        APP.MainLoop()

class _zemote_gui_frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Zemote", size=(600, 400))      
        
        # Initiate ZemoteCore
        self.core = ZemoteCore()

        # tmp 
        snd_queue = Queue.Queue() # Queue to send from USB
        rcv_queue = Queue.Queue() # Queue to receive from USB
        # The flag connected is not protected. May need protection in the future
        serial_queue = {'connected': False, 'snd': snd_queue, 'rcv': rcv_queue}

        # Menu bar
        self.menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.menubar.Append(fileMenu, '&File')
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        # Status bar
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetMinHeight(200)

        # Panels
        self.button_panel = button_panel(self, serial_queue)
        self.serialToolBar = serialToolBar(self)      
        self.serialTerminal = serialTerminal(self)

        # ZemoteCore - assign call backs
        self.core.read_thread_cb = self.serialTerminal.updateTerminal

        # Layout
        botSizer = wx.BoxSizer(wx.HORIZONTAL)
        botSizer.AddMany([
            (self.button_panel, 1, wx.EXPAND),
            (self.serialTerminal, 1, wx.EXPAND),
            ((15, 15), 0),
        ])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
            (self.serialToolBar, 0),
            (botSizer, 1, wx.EXPAND),
        ])
        self.SetSizer(sizer)
        self.SetMinSize((600, 400))

    def OnQuit(self, e):
        self.Close()

