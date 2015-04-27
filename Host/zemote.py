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

import Queue
import serial_tool
import zemote_gui

snd_queue = Queue.Queue() # Queue to send from USB
rcv_queue = Queue.Queue() # Queue to receive from USB
# The flag connected is not protected. May need protection in the future
serial_queue = {'connected': False, 'snd': snd_queue, 'rcv': rcv_queue}

# Arduino vendor ID
vendorID = '2341:0043'

if __name__ == '__main__':
    # Launch the serial thread
    #serial_thread = serial_tool.serial_tool(vendorID, serial_queue)
    #serial_thread.start()   

    # Launch the gui thread
    zemote_gui.zemote_gui()
