# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 18:55:24 2014

@author: Nicholas Zwiryk
"""

import ctypes
import time
import MidiMonitor
from random import randint

vibLookup = {'red':32768, 'blue':8192, 'green':16384,'yellow':24576, 'fogOn':256, 'fogOff':512}
colorLookup = {32768:'red',8192:'blue', 16384:'green',24576:'yellow', 256:'fogOn', 512:'fogOff'}
lastState = {'red':0,'blue':0,'green':0,'yellow':0, 'fog':0}

red = 32768
blue = 8192
green = 16384
yellow= 24576
fogon = 256
fogoff = 512

colors = [red,green,blue,yellow]

#controller = int(raw_input("Enter the numerical controller number, indexing from 0:"))
controller = 0
# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

#vibration = XINPUT_VIBRATION(65535, 65535)
#XInputSetState(0, ctypes.byref(vibration))

# You can also create a hel0per function like this:
def set_vibration(left_motor, right_motor):
    global lastLeft
    global lastRight
    global lastState
    vibration = XINPUT_VIBRATION(int(left_motor), int(right_motor))
    XInputSetState(controller, ctypes.byref(vibration))
    lastLeft = left_motor
    lastRight = right_motor
    if lastRight == vibLookup['red']:
        lastState['red'] = lastLeft
    elif lastRight  == vibLookup['blue']:
        lastState['blue'] = lastLeft
    elif lastRight == vibLookup['green']:
        lastState['green'] =lastLeft
    elif lastRight == vibLookup['yellow']:
        lastState['yellow'] = lastLeft
    elif lastRight == ['fogOn']:
        lastState['fog'] = 1
    else:
        lastState ['fog'] = 0


def getArrayVib(state):
    vib = int(state)*256
    return vib
def AllOff():
    set_vibration(65535,65535)
    
def Marquee(color,duration,direction,delay,pattern, avgnd):
    stop = time.time()+duration
    for y in color:
        set_vibration(getArrayVib(pattern),y)
        time.sleep(0.01)                    
    while time.time() < stop and avgnd+avgnd*0.2>MidiMonitor.avgNoteDelta and avgnd-avgnd*0.2<MidiMonitor.avgNoteDelta:
            for x in range(0,8):
                for y in color:
                    Shift(y,direction,1)
                    time.sleep(0.01)
                    time.sleep(delay)
    AllOff()
def Shift(color,direction,count):
    for x in range(0,count):    
        if direction == "cw":
            set_vibration(getArrayVib(rotate(bin(lastState[colorLookup[color]]/256)[2:].zfill(8),count)),color)
        if direction == "ccw":
            set_vibration(getArrayVib(rotate(bin(lastState[colorLookup[color]]/256)[2:].zfill(8),-1*count)),color)
def rotate(strg,n):
    return int((strg[n:] + strg[:n]),2)
    
def randomColor():
    return colors[randint(0,len(colors)-1)]