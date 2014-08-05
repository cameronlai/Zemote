# Zemote

Zemote is a project to rethink the idea of a programmable remote control.
Nowadays, entertainment systems have became more and more complicated. 
You could have a game console connected, a few external TV boxes, a recorder, a computer or any sort of devices connected to your television and you would have a separate remote for every one of these devices.
The old days when you only had one television and one remote control are gone. 
Image if you could easily combine all thoses remote into one based on your own preference,
life will be so much simpler and this is where Zemote comes in.

Programmable remote controls in the market are expensive and complicated. 
Also, they often lack the ability to work with devices produced by other companeis. 
Zemote attempts to solve the problem by allowing you to program your own remote control, with the use of other remote controls.
It is designed to be simple to program and simple to use.

# Programming a zemote control

1. To program a zemote controller, plug the zemote controller into your computer.

2. The host program will automatically detect the Arduino device and connect.

3. Select your channel or button to program, and then use your original remotes to program zemote.

4. Click finish programming when you're done. If there are more than 8 commands, the host program will finish that programming action as the buffer size is excedded. 

5. Repeat the process for all the channels or buttons you would like to program.

6. Click Save To EEPROM so all programming actions are saved with involatile memory.

7. Finally, you're good to go.

#Development

Zemote firmware is developed based on Arduino and the IRremote library (special thanks to Ken Shirriff for developing it).

Zemote host is developed using Python and Wx as its GUI. The user interface follows the simplicity principal of the product. 

Contributions are welcome. Since the size of the project is still relatively small, all parts of the project are kept the same repository. 

If you have an Arduino, it's super simple for you to build a prototype and start playing around with the code. 

#License

Zemote
(C) Copyright 2014 Cameron Lai
 
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU Lesser General Public License
(LGPL) version 3.0 which accompanies this distribution, and is available at
https://www.gnu.org/licenses/lgpl-3.0.txt
 
Zemote is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.
 
