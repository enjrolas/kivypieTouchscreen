#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
    
#Set GPIO mode
GPIO.setmode(GPIO.BCM)

#Setup GPIO
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #second from the top
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #bottom

#Set up backlight GPIO
#os.system("sudo sh -c 'echo 252 &gt; /sys/class/gpio/export'")

#Set the intitial counter value to zero
counter = 0

#var for the 'while' statement to keep it running
var = 1

lastPressed=True
pressed=False
pressTime=0
debounce=0.25
while var == 1:
    pressed=GPIO.input(27)
    if pressed==False and lastPressed==True and time.time()>=(pressTime+debounce):
        pressTime=time.time()
        print("button pressed %f" % time.time())
    lastPressed=pressed
