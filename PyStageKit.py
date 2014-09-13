# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 18:55:24 2014

@author: Nicholas Zwiryk
"""

import ctypes
import time
import config
from random import randint

vibLookup = {'red':32768, 'blue':8192, 'green':16384,'yellow':24576, 'fogOn':256, 'fogOff':512}
colorLookup = {32768:'red',8192:'blue', 16384:'green',24576:'yellow'}
lastState = {'red':0,'blue':0,'green':0,'yellow':0, 'fog':0}
colorVector = {'red':0,'blue':0,'green':0,'yellow':0}
patternVector = {'red':0b11001100,'blue':0b00000001,'green':0b10101010,'yellow':000010001}
stateLookup = ['cw','ccw',1]
red = 32768
blue = 8192
green = 16384
yellow= 24576
fogon = 256
fogoff = 512

colors = [red,green,blue,yellow]

noteMidi = {'kick':36, 'snare':38, 'yellowTom':48, 'blueTom':45, 'greenTom':43,'closedHiHat':42,'openHiHat':51,'ride':59, 'crash':49}
midiNote = {36:'kick', 38:'snare', 48:'yellowTom', 45:'blueTom', 43:'greenTom',42:'closedHiHat',51:'openHiHat',59:'ride', 49:'crash'}

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
    
def lightBoot():
    for y in colorVector:
        if colorVector[y]!=0:
            set_vibration(getArrayVib(patternVector[y]),vibLookup[y])
            time.sleep(0.01)

def lightUpdate():
    for y in colorVector:
        if colorVector[y] != 0:              
             Shift(vibLookup[y],colorVector[y],1)
             time.sleep(0.01)
             

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
    
def getVelVib():
    return min(colorLookup, key = lambda x:abs(x-config.avgVelocity*512))
    
def getTimeVib():
    return min(colorLookup, key = lambda x:abs(x-config.avgNoteDelta**-1*3e6))
    
def updateVector():
    colorVector = {'red':0,'blue':0,'green':0,'yellow':0}
    colorVector[colorLookup[getVelVib()]]=stateLookup[randint(0,len(stateLookup)-1)]
    colorVector[colorLookup[getTimeVib()]]=stateLookup[randint(0,len(stateLookup)-1)]