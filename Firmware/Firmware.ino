/*
 * Zemote
 * (C) Copyright 2014 Cameron Lai
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the GNU Lesser General Public License
 * (LGPL) version 3.0 which accompanies this distribution, and is available at
 * https://www.gnu.org/licenses/lgpl-3.0.txt
 *
 * Zemote is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 */

#define VERSION_NUM 0.1
#define DEBUG 0

#include <IRremote.h>
#include <EEPROM.h>
#include "pins.h"
#include "button.h"
#include "transceive.h"

// Local functions
void getAddr();
void saveToEEPROM();
void readFromEEPROM();

/**
 * \fn void setup()
 * \brief Set up buttons and USB and read from EEPROM
 */
void setup(){
  Serial.begin(9600);
  Serial.print("Zemote\n");  
  for (int i=0; i<NUM_PHY_BUTTONS; i++)
  {
    pinMode(buttons[i], INPUT); // Input pins
    digitalWrite(buttons[i], HIGH); // Internal pull-up resistor
  }
  readFromEEPROM();
}

/**
 * \fn void loop()
 * \brief Main loop that handles button checking and USB communication
 */
void loop()
{   
  char cmd1, cmd2, cmd3;  
  if (Serial.available() > 2)
  {
    cmd1 = Serial.read();
    cmd2 = Serial.read();
    cmd3 = Serial.read();
    if (cmd3 == '\n')
    {
#if DEBUG==1
      Serial.print(cmd1);
      Serial.print(cmd2);
      Serial.print(cmd3);
#endif
      cmd2 -= 48;
      if (cmd2 < 0 || cmd2 > NUM_SOFT_BUTTONS)
      {
        serial_error(cmd1);
        serial_error(cmd2+48);
        return; 
      }
      switch(cmd1)
      {
      case 'T':
        sndIRStream(cmd2);
        break;
      case 'S':
        saveToEEPROM();
        break;
      case 'R':
        readFromEEPROM();
        break;
      case 'V':
        Serial.println(VERSION_NUM);
        break;
      default:
        break;
      }
      serial_ack(cmd1);
      if (cmd1 == 'P') rcvIRStream(cmd2);
    }
    else
    {
      serial_error(cmd1);
    }   
  }
  check_buttons();
}

/**
* \fn int getAddr(int buttonLen, int cmdLen)
* \brief Get address for EEPROM read and save
*/
int getAddr(int buttonLen, int cmdLen)
{
  return (buttonLen * NUM_COMMANDS_PER_BUTTON + cmdLen) * NUM_BYTES_PER_COMMAND;
}

/**
 * \fn void saveToEEPROM()
 * \brief Save IR data to EEPROM and 441 bytes are used in EEPROM.
 */
void saveToEEPROM()
{  
  unsigned char tmpValue;
  int k;

  for (int i=0; i<NUM_SOFT_BUTTONS; i++)
  {
    for (int j=0; j<NUM_COMMANDS_PER_BUTTON; j++)
    {
      EEPROM.write(getAddr(i,j), user_cmd[i][j].bits);
#if DEBUG==1
      Serial.println(getAddr(i,j));
      Serial.print("Bits:");
      Serial.println(user_cmd[i][j].bits);
#endif
      for (k=0; k<4; k++)
      {
        tmpValue = (unsigned char)(user_cmd[i][j].value >> (k * 8));
        EEPROM.write(getAddr(i,j)+k+1, tmpValue);
#if DEBUG==1
        Serial.println(getAddr(i,j)+k+1);
        Serial.print("Value:");
        Serial.println(tmpValue, HEX);
#endif
      }
      EEPROM.write(getAddr(i,j)+k+1, user_cmd[i][j].decode_type);
#if DEBUG==1
      Serial.println(getAddr(i,j)+k+1);
      Serial.print("Decode:");
      Serial.println(user_cmd[i][j].decode_type, DEC);
#endif
    } 
  }
  for (int i=0; i<NUM_SOFT_BUTTONS; i++)
  {
    EEPROM.write(getAddr(NUM_SOFT_BUTTONS, 0)+i, user_cmd_len[i]);
#if DEBUG==1
    Serial.println(getAddr(NUM_SOFT_BUTTONS, 0)+i);
    Serial.print("Len:");
    Serial.println(user_cmd_len[i], DEC);
#endif
  }
}

/**
 * \fn void readFromEEPROM()
 * \brief Read IR data from EEPROM and 441 bytes are used in EEPROM.
 */
void readFromEEPROM()
{
  unsigned char tmpValue;
  unsigned long tmpValue2, tmpSum;
  int k;

  for (int i=0; i<NUM_SOFT_BUTTONS; i++)
  {
    for (int j=0; j<NUM_COMMANDS_PER_BUTTON; j++)
    {
      user_cmd[i][j].bits = EEPROM.read(getAddr(i,j));
#if DEBUG==1
      Serial.println(getAddr(i,j));
      Serial.print("Bits:");
      Serial.println(user_cmd[i][j].bits);
#endif
      tmpSum = 0;
      for (k=0; k<4; k++)
      {
        tmpValue = EEPROM.read(getAddr(i,j)+k+1);  
#if DEBUG==1
        Serial.println(getAddr(i,j)+k+1);
        Serial.print("Value:");
        Serial.println(tmpValue, HEX);
#endif       
        tmpSum += ((unsigned long)tmpValue) << (k*8);
      }
      user_cmd[i][j].value = tmpSum;
#if DEBUG==1
      Serial.print("Cmd:");
      Serial.println(tmpSum, HEX);
#endif

      user_cmd[i][j].decode_type = EEPROM.read(getAddr(i,j)+k+1);
#if DEBUG==1
      Serial.println(getAddr(i,j)+k+1);
      Serial.print("Decode:");
      Serial.println(user_cmd[i][j].decode_type, DEC);
#endif
    } 
  }
  for (int i=0; i<NUM_SOFT_BUTTONS; i++)
  {
    user_cmd_len[i] = EEPROM.read(getAddr(NUM_SOFT_BUTTONS, 0)+i);
#if DEBUG==1
    Serial.println(getAddr(NUM_SOFT_BUTTONS, 0)+i);
    Serial.print("Len:");
    Serial.println(user_cmd_len[i], DEC);
#endif
  }
}





