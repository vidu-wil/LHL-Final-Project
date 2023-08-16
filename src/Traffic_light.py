#!/usr/bin/env python3

###################################################################
# The Traffic light controller is created using a templated       #
# from Sounfounder raphael-kit and modified to use the            #
# ML predictions and function as a 4-way traffic light controller #
###################################################################


# importing modules

import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime
import pandas as pd

#define the pins connect to 74HC595
SDI   = 24      #serial data input(DS)
RCLK  = 23     #memory clock input(STCP)
SRCLK = 18      #shift register clock input(SHCP)
number = (0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90)

placePin = (10,22,27,17)
ledPin_1 =(16,20,12)
ledPin_2 = (25,8,7)
ledPin_3 =(4,5,6)
ledPin_4 = (13,19,26)

# set initial times for each light
greenLight_NS = 30
yellowLight_NS = 2
redLight_NS = 32

greenLight_WE = 30
yellowLight_WE = 2
redLight_WE = 32

lightColor=("Red_NS","Green_NS","Yellow_NS", "Red_WE")

colorState=0
counter = 30
counter_2 = 30
timer1 = 0

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    for pin in placePin:
        GPIO.setup(pin,GPIO.OUT)
    for pin in ledPin_1:
        GPIO.setup(pin,GPIO.OUT)
    for pin in ledPin_2:
        GPIO.setup(pin,GPIO.OUT)
    for pin in ledPin_3:
        GPIO.setup(pin,GPIO.OUT)
    for pin in ledPin_4:
        GPIO.setup(pin,GPIO.OUT)
    global timer1
    timer1 = threading.Timer(1.0,timer)
    timer1.start()

def clearDisplay():
    for i in range(8):
        GPIO.output(SDI, 1)
        GPIO.output(SRCLK, GPIO.HIGH)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def hc595_shift(data):
    for i in range(8):
        GPIO.output(SDI, 0x80 & (data << i))
        GPIO.output(SRCLK, GPIO.HIGH)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def pickDigit(digit):
    for i in placePin:
        GPIO.output(i,GPIO.LOW)
    GPIO.output(placePin[digit], GPIO.HIGH)

def timer():        #timer function
    global counter
    global colorState
    global timer1
    global counter_2
    timer1 = threading.Timer(1.0,timer)
    timer1.start()
    counter-=1
    counter_2 -= 1
    timing()
    if (counter is 0 or counter_2== 0):
        if(colorState is 0):
            counter= yellowLight_NS
            counter_2 = redLight_WE
        if(colorState is 1):
            counter=greenLight_NS
        if (colorState is 2):
            counter=redLight_NS
            counter_2= yellowLight_WE
        if (colorState is 3):
            counter_2= greenLight_WE
        colorState=(colorState+1)%4
    print ("counter : %d    color: %s "%(counter,lightColor[colorState]))

def lightup():
    global colorState
    for i in range(0,3):
        GPIO.output(ledPin_1[i], GPIO.HIGH)
        GPIO.output(ledPin_2[i], GPIO.HIGH)
        GPIO.output(ledPin_3[i], GPIO.HIGH)
        GPIO.output(ledPin_4[i], GPIO.HIGH)
        if colorState == 0:
            GPIO.output(ledPin_1[0], GPIO.LOW)
            GPIO.output(ledPin_2[0], GPIO.LOW)
            GPIO.output(ledPin_3[1], GPIO.LOW)
            GPIO.output(ledPin_4[1], GPIO.LOW)
        elif colorState == 1:
            GPIO.output(ledPin_1[0], GPIO.LOW)
            GPIO.output(ledPin_2[0], GPIO.LOW)
            GPIO.output(ledPin_3[2], GPIO.LOW)
            GPIO.output(ledPin_4[2], GPIO.LOW)
        elif colorState == 2:
            GPIO.output(ledPin_1[2], GPIO.LOW)
            GPIO.output(ledPin_2[2], GPIO.LOW)
            GPIO.output(ledPin_3[0], GPIO.LOW)
            GPIO.output(ledPin_4[0], GPIO.LOW)
        elif colorState == 3:
            GPIO.output(ledPin_1[1], GPIO.LOW)
            GPIO.output(ledPin_2[1], GPIO.LOW)
            GPIO.output(ledPin_3[0], GPIO.LOW)
            GPIO.output(ledPin_4[0], GPIO.LOW)

def timing():
    global greenLight_NS
    global yellowLight_NS
    global redLight_NS
    global greenLight_WE
    global yellowLight_WE
    global redLight_WE
    df1 = pd.read_csv("../output/output_junc1.csv")
    now = datetime.now()
    Hour = int(now.strftime("%H"))
    Day = int(now.strftime("%d"))
    Year = int(now.strftime("%Y"))
    Month = int(now.strftime("%m"))
    number_of_vehicles = df1.loc[(df1['Hour']== Hour) & (df1['Day']==Day) &
           (df1['Year']==Year) & (df1['Month']==Month)]['Vehicles'].values[0]

    if number_of_vehicles < 30:
        greenLight_NS = 100
        yellowLight_NS = 3
        redLight_NS = 103

        greenLight_WE = 100
        yellowLight_WE = 3
        redLight_WE = 103

    elif (number_of_vehicles < 31) and (number_of_vehicles > 61):
        greenLight_NS = 60
        yellowLight_NS = 3
        redLight_NS = 63

        greenLight_WE = 60
        yellowLight_WE = 3
        redLight_WE = 47

    else:
        greenLight_NS = 45
        yellowLight_NS = 3
        redLight_NS = 48

        greenLight_WE = 45
        yellowLight_WE = 3
        redLight_WE = 48

def display():
    global counter

    a = counter % 10000//1000 + counter % 1000//100
    b = counter % 10000//1000 + counter % 1000//100 + counter % 100//10
    c = counter % 10000//1000 + counter % 1000//100 + counter % 100//10 + counter % 10

    if (counter % 10000//1000 == 0):
        clearDisplay()
    else:
        clearDisplay()
        pickDigit(3)
        hc595_shift(number[counter % 10000//1000])

    if (a == 0):
        clearDisplay()
    else:
        clearDisplay()
        pickDigit(2)
        hc595_shift(number[counter % 1000//100])

    if (b == 0):
        clearDisplay()
    else:
        clearDisplay()
        pickDigit(1)
        hc595_shift(number[counter % 100//10])

    if(c == 0):
        clearDisplay()
    else:
        clearDisplay()
        pickDigit(0)
        hc595_shift(number[counter % 10])

def loop():
    while True:
        display()
        lightup()

def destroy():   # When "Ctrl+C" is pressed, the function is executed.
    global timer1
    GPIO.cleanup()
    timer1.cancel()      #cancel the timer

if __name__ == '__main__': # Program starting from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()