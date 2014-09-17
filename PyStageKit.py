# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 18:55:24 2014

@author: Nicholas Zwiryk
"""

import ctypes
import time
from random import randint
import config
import pyHueRock as hr


vibLookup = {'red':32768, 'blue':8192, 'green':16384,'yellow':24576, 'fogOn':256, 'fogOff':512}
colorLookup = {32768:'red',8192:'blue', 16384:'green',24576:'yellow'}
lastState = {'red':0,'blue':0,'green':0,'yellow':0, 'fog':0}


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

class ledArray(object):
    def __init__(self,controller,lastState, colorVector,patternVector):
        self.controller = controller
        self.lastState = lastState
        self.colorVector = colorVector
        self.patternVector = patternVector

    def set_vibration(self, left_motor, right_motor):
        global lastLeft
        global lastRight
        global lastState
        vibration = XINPUT_VIBRATION(int(left_motor), int(right_motor))
        XInputSetState(self.controller, ctypes.byref(vibration))
        lastLeft = left_motor
        lastRight = right_motor
        if lastRight == vibLookup['red']:
            self.lastState['red'] = lastLeft
        elif lastRight  == vibLookup['blue']:
            self.lastState['blue'] = lastLeft
        elif lastRight == vibLookup['green']:
            self.lastState['green'] =lastLeft
        elif lastRight == vibLookup['yellow']:
            self.lastState['yellow'] = lastLeft
        elif lastRight == ['fogOn']:
            self.lastState['fog'] = 1
        else:
            self.lastState ['fog'] = 0
            
    def mirrorState(self,array):
        global colorVector
        self.patternVector = array.patternVector
        for key, value in array.colorVector.iteritems():
            if value == 'cw':
                self.colorVector[key] == 'ccw'
            elif value == 'ccw':
                self.colorVector[key] == 'cw'
            else:
                self.colorVector[key] == value
   
    def lightBoot(self):
        for y in self.colorVector:
            if self.colorVector[y]!=0:
                self.set_vibration(getArrayVib(self.patternVector[y]),vibLookup[y])
                time.sleep(0.01)
            elif self.colorVector[y] == 0:
                self.set_vibration(0,vibLookup[y])
           
    def AllOff(self):
        self.set_vibration(65535,65535)
             
    def allOn(self):
        for x in colors:
            self.set_vibration(65535,x)
            time.sleep(0.01)  

    def lightUpdate(self):
        for y in self.colorVector:
            if self.colorVector[y] != 0:              
                 self.Shift(vibLookup[y],config.colorVector[y],1)
                 time.sleep(0.01)
            elif self.colorVector[y] == 0:
                 self.set_vibration(0,vibLookup[y])              

    def Shift(self,color,direction,count):
        for x in range(0,count):    
            if direction == "cw":
                self.set_vibration(getArrayVib(rotate(bin(lastState[colorLookup[color]]/256)[2:].zfill(8),count)),color)
            if direction == "ccw":
                self.set_vibration(getArrayVib(rotate(bin(lastState[colorLookup[color]]/256)[2:].zfill(8),-1*count)),color)
                
    def updateVector(self,avgVelocity, avgNoteDelta):

        self.colorVector = {'red':0,'blue':0,'green':0,'yellow':0}
        
        self.colorVector[colorLookup[getVelVib(avgVelocity)]]=stateLookup[randint(0,len(stateLookup)-1)]
        self.colorVector[colorLookup[getTimeVib(avgNoteDelta)]]=stateLookup[randint(0,len(stateLookup)-1)]
     
    
    def updatePattern(self):
        for key, value in self.patternVector.iteritems():
            self.patternVector[key] = config.patternStates[randint(0,(len(config.patternStates)-1))]

def getArrayVib(state):
    vib = int(state)*256
    return vib          

        
def rotate(strg,n):
    return int((strg[n:] + strg[:n]),2)
    
def randomColor():
    return colors[randint(0,len(colors)-1)]
    
def getVelVib(avgVelocity):
    
    return min(colorLookup, key = lambda x:abs(x-avgVelocity*512))
    
def getTimeVib(avgNoteDelta):
    return min(colorLookup, key = lambda x:abs(x-avgNoteDelta**-1*3e6))
    


def updateHue():
    currentColors = []
    for x in range (0,len(hr.lights)-1):
        currentColors.append(randint(hr.hueColors['blue'],hr.hueColors['red']))
        hr.lights[x].hue = currentColors[x]
    