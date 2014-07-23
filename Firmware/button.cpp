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
 
#include "pins.h"
#include "button.h"
#include "transceive.h"

// Local variables
char lastButtonStates[NUM_PHY_BUTTONS] = {
  HIGH};
char justPressed[NUM_PHY_BUTTONS]= {
  0};
long lastDebounceTime[NUM_PHY_BUTTONS] = {
  0};
char current_channel = HOME_CHANNEL;

/**
 * \fn check_buttons()
 * \brief button checking loop
 */
void check_buttons(){
  for (char i=0;i<NUM_PHY_BUTTONS;i++){
    int reading = digitalRead(buttons[i]);
    if (reading != lastButtonStates[i]) lastDebounceTime[i]=millis();
    if ((millis()-lastDebounceTime[i]) > DEBOUNCE_DELAY) {
      if (reading == LOW && lastButtonStates[i] == LOW && justPressed[i] == 0) {
        button_send_handler(i);
        justPressed[i] = 1;
      }
      if (reading == HIGH && lastButtonStates[i] == HIGH) justPressed[i] = 0;
    }
    lastButtonStates[i]=reading;
  }
}

/**
 * \fn void button_send_handler(unsigned char button)
 * \brief maps the physical button to the software buttons and channels
 */
void button_send_handler(unsigned char button){
  switch(button)
  {
  case 3: // Home Button
    sndIRStream(HOME_CHANNEL);
    break;
  case 4: // Channel Plus Button
    current_channel++;
    if (current_channel >= NUM_SOFT_BUTTONS) current_channel = HOME_CHANNEL;
    sndIRStream(current_channel);
    Serial.println(current_channel);
    break;
  case 5: // Channel Minus Button
    current_channel--;
    if (current_channel < 1) current_channel = NUM_SOFT_BUTTONS-1;
    sndIRStream(current_channel);
    Serial.println(current_channel);
    break;
  default:
    sndIRStream(button);
    break;
  }
}




