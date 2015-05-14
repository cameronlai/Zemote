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

class myMenuBar(wx.MenuBar):
    def __init__(self, parent):
        self.parent = parent
        self.menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        quitItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        aboutItem = helpMenu.Append(100, 'About', 'About Zemote')
        self.menubar.Append(fileMenu, '&File')
        self.menubar.Append(helpMenu, '&Help')

        # Menu binding
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, quitItem)
        self.parent.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnAbout(self, e):    
        description = """Zemote is a project to rethink the idea of a 
programmable remote control. It is designed to be simple to program and simple to use.
"""

        licence = """
Zemote
(C) Copyright 2014 Cameron Lai

All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU Lesser General Public License
(LGPL) version 3.0 which accompanies this distribution, and is available at
http://www.gnu.org/licenses/lgpl-3.0.html

Zemote is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.
"""
        info = wx.AboutDialogInfo()

        #info.SetIcon(wx.Icon('zemote.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Zemote')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 - 2015 Cameron Lai')
        info.SetWebSite('https://github.com/cameronlai/zemote')
        info.SetLicence(licence)
        info.AddDeveloper('Cameron Lai')
        #info.AddDocWriter('')
        #info.AddArtist('')
        #info.AddTranslator('')

        wx.AboutBox(info) 
