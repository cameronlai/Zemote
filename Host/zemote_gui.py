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

class zemote_gui():
    def __init__(self, serial_queue):
        print 'Zemote Host Initialized'
        APP = wx.App(False)
        FRAME = _zemote_gui_frame(None, serial_queue)
        FRAME.Show()
        APP.MainLoop()

class _zemote_gui_frame(wx.Frame):
    def __init__(self, parent, serial_queue):
        wx.Frame.__init__(self, parent, title="Zemote", size=(300, 400))

        # Panels
        self.button_panel = button_panel(self, serial_queue)

        # Layout
        self.__DoLayout()
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetMinHeight(200)

    def __DoLayout(self):        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([
                ((15, 15), 0),
                (self.button_panel, 0, wx.ALIGN_CENTER),
                ])
        self.SetSizer(sizer)
        self.SetMinSize((300, 300))
