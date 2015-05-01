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

class serialTerminal(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.core = self.parent.core
        self.statusBar = self.parent.statusBar
        self.history = [] # 0: latest command
        self.historyIndex = 0;
       
        self.__DoLayout()   

    def __DoLayout(self):
        self.terminalTextCtrl = wx.TextCtrl(self, -1, "", size=(300, -1),
                                            style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.terminalTextCtrl.SetMinSize((100, -1))
        self.inputTextCtrl = wx.TextCtrl(self, -1, "", size=(200, -1),
                                         style=wx.TE_PROCESS_ENTER)
        self.sendButton = wx.Button(self, name='Send', label='Send')
        # Sizer
        botSizer = wx.BoxSizer(wx.HORIZONTAL)
        botSizer.AddMany([
            (self.inputTextCtrl, 1),
            (self.sendButton, 0),
        ])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
            (self.terminalTextCtrl, 1, wx.EXPAND),
            (botSizer, 0),
        ])
        self.SetSizerAndFit(sizer)

        # Binding 
        self.sendButton.Bind(wx.EVT_BUTTON, self.OnSend)
        self.inputTextCtrl.Bind(wx.EVT_CHAR, self.OnChar)

        self.core.read_thread_buffer = self.terminalTextCtrl

    def updateTerminal(self, line):
        self.terminalTextCtrl.AppendText(line)

    def setCommand(self, direction):
        print self.history
        print self.historyIndex
        if (len(self.history) == 0):
            return
        elif (direction == -1 and self.historyIndex==0):
            return
        elif (direction == 1 and self.historyIndex+1 == len(self.history)):
            return
        else:            
            self.historyIndex += direction
            self.inputTextCtrl.SetValue(self.history[self.historyIndex])

    def OnSend(self, evt):
        if self.core.connected:
            rawCmd = self.inputTextCtrl.GetValue()
            self.core.send(rawCmd)
            self.history.insert(0, rawCmd)
            self.inputTextCtrl.SetValue('')
        else:
            self.statusBar.SetStatusText('Serial port not connected')

    def OnChar(self, evt):      
        code = evt.GetKeyCode()
        if code == wx.WXK_RETURN:
            self.OnSend(None)
        if code == wx.WXK_UP:
            self.setCommand(1)
        if code == wx.WXK_DOWN:
            self.setCommand(-1)
        evt.Skip()
