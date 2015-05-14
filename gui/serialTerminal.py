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
        self.terminalTextCtrl = wx.TextCtrl(self, -1, '', size=(300, -1),
                                            style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.terminalTextCtrl.SetMinSize((100, -1))
        self.inputTextCtrl = wx.TextCtrl(self, -1, '', size=(200, -1),
                                         style=wx.TE_PROCESS_ENTER)
        self.sendButton = wx.Button(self, name='Send', label='Send')
        self.clearButton = wx.Button(self, name='Clear', label='Clear')
        # Sizer
        botSizer = wx.BoxSizer(wx.HORIZONTAL)
        botSizer.AddMany([
            (self.inputTextCtrl, 1),
            (self.sendButton, 0),
        ])
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
            ((5,5),0),
            (self.clearButton, 0),
            ((5,5),0),
            (self.terminalTextCtrl, 1, wx.EXPAND),
            ((5,5),0),
            (botSizer, 0),
        ])
        self.SetSizerAndFit(sizer)

        # Binding 
        self.sendButton.Bind(wx.EVT_BUTTON, self.OnSend)
        self.clearButton.Bind(wx.EVT_BUTTON, self.OnClear)
        self.inputTextCtrl.Bind(wx.EVT_CHAR, self.OnChar)   
        
        # Read thread buffer display
        self.core.read_thread_buffer = self.terminalTextCtrl

    def updateTerminal(self, line):
        self.terminalTextCtrl.AppendText(line)

    def setCommand(self, direction):
        if (len(self.history) == 0):
            return
        elif (direction == -1 and self.historyIndex==0):
            return
        elif (direction == 1 and self.historyIndex+1 == len(self.history)):
            return
        else:            
            self.historyIndex += direction
            self.inputTextCtrl.SetValue(self.history[self.historyIndex])

    def OnSend(self, e):
        rawCmd = self.inputTextCtrl.GetValue()
        if self.core.send(rawCmd):
            self.history.insert(0, rawCmd)
        self.inputTextCtrl.SetValue('')

    def OnClear(self, e):
        self.terminalTextCtrl.Clear()

    def OnChar(self, e):      
        code = e.GetKeyCode()
        if code == wx.WXK_RETURN:
            self.OnSend(None)
        if code == wx.WXK_UP:
            self.setCommand(1)
        if code == wx.WXK_DOWN:
            self.setCommand(-1)
        e.Skip()
