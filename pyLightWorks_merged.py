# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 19:17:12 2014

@author: Nicholas Zwiryk
"""

from collections import deque
import pygame.midi as midi
import numpy as np
import time
import config
import operator
import ctypes
from random import randint
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
                self.colorVector[key] = 'ccw'
                
            elif value == 'ccw':
                self.colorVector[key] = 'cw'
            else:
                self.colorVector[key] = value
           
   
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
                 self.Shift(vibLookup[y],self.colorVector[y],1)
                 time.sleep(0.01)
            elif self.colorVector[y] == 0:
                 self.set_vibration(0,vibLookup[y])              

    def Shift(self,color,direction,count):
        for x in range(0,count):    
            if direction == "cw":
                self.set_vibration(getArrayVib(rotate(bin(self.lastState[colorLookup[color]]/256)[2:].zfill(8),count)),color)
            if direction == "ccw":
                self.set_vibration(getArrayVib(rotate(bin(self.lastState[colorLookup[color]]/256)[2:].zfill(8),-1*count)),color)
                
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


noteMidi = {'kick':36, 'snare':38, 'yellowTom':48, 'blueTom':45, 'greenTom':43,'closedHiHat':42,'openHiHat':51,'ride':59, 'crash':49}
midiNote = {36:'kick', 38:'snare', 48:'yellowTom', 45:'blueTom', 43:'greenTom',42:'closedHiHat',51:'openHiHat',59:'ride', 49:'crash'}
#noteChart = {'kick':0, 'snare':0, 'yellowTom':0, 'blueTom':0, 'greenTom':0,'closedHiHat':0,'openHiHat':0,'ride':0, 'crash':0}

binSize = 10
flagThreshold = 0.75
flaggedNote = -1
midi.quit()
midi.init()
m = midi.Input(1,4096)
noteBin = deque('',binSize)
timeBin = deque('',binSize)
velocityBin = deque('',binSize)
histBin = [36,38,42,43,45,48,49,51,60]
sensitivity = 0.25
timeBin.append(0)

lArray = ledArray(0,{'red':0,'blue':0,'green':0,'yellow':0, 'fog':0},{'red':0,'blue':0,'green':0,'yellow':0},{'red':0b10000000,'blue':0b00000001,'green':0b10101010,'yellow':000010001})
rArray = ledArray(1,{'red':0,'blue':0,'green':0,'yellow':0, 'fog':0},{'red':0,'blue':0,'green':0,'yellow':0},{'red':0b10000000,'blue':0b00000001,'green':0b10101010,'yellow':000010001})

def calcFlagNotes(threshold):
    global flaggedNote
    noteThresholdCount = binSize*flagThreshold
    
    if config.noteChart[max(config.noteChart.iteritems(), key=operator.itemgetter(1))[0]] >= noteThresholdCount:
        flaggedNote = noteMidi[max(config.noteChart.iteritems(), key=operator.itemgetter(1))[0]]
    else:
        return -1

def getCrashFlag():
    if config.noteChart['crash'] <= 1:
        return True
    else:
        return False

def midiMonitor():
    global flaggedNote
    avgNoteDelta = 75
    oldNoteDelta = 1
    avgVelocity = 64
    timeToSwitch = 0.1
    lastTimeStamp = time.time()
    lArray.lightBoot()
    rArray.lightBoot()
    accentFlag = False
    while True:
        lastKeyPress = m.read(1)
        
        if lastKeyPress != []: 
            if lastKeyPress[0][0][0] != 137:          
                lastNote =lastKeyPress[0][0][1]
                lastMidiTimeStamp = lastKeyPress[0][1]
                lastVelocity = lastKeyPress[0][0][2]
                
                noteBin.appendleft(lastNote)
                timeBin.appendleft(lastMidiTimeStamp)
                velocityBin.appendleft(lastVelocity)
                
                timeDelta = list(timeBin)
                avgNoteDelta  = abs(np.mean(np.diff(timeDelta)))
                lastNotes = list(noteBin)
                avgVelocity = np.mean(velocityBin)
                noteHist = np.histogram(lastNotes,sorted((list(histBin))))
                #print lastNote
                if getCrashFlag() and lastNote == noteMidi['crash']:
                    accentFlag = True
                #print avgNoteDelta
                for x in noteHist[1][0:len(noteHist[1])-1]:
                    config.noteChart[midiNote[x]]=list(noteHist[0])[list(noteHist[1]).index(int(x))]
                    
                calcFlagNotes(flagThreshold)
                
                if lastNote == flaggedNote:
                    accentFlag = True
                    flaggedNote = -1
                
        if accentFlag:
           lArray.allOn()
           rArray.allOn()
           time.sleep(0.02)
           accentFlag = False
           lArray.AllOff()
           rArray.AllOff()
           lArray.lightBoot()
           rArray.lightBoot()
           
        if (oldNoteDelta + sensitivity*oldNoteDelta) <avgNoteDelta or (oldNoteDelta - sensitivity*oldNoteDelta) > avgNoteDelta:
            lArray.updateVector(avgVelocity,avgNoteDelta)
            rArray.mirrorState(lArray)
            lArray.updatePattern()
            updateHue()
            lArray.lightBoot()
            rArray.lightBoot()
 
        
        timeToSwitch -= (time.time() - lastTimeStamp)
        lastTimeStamp = time.time()
        oldNoteDelta = avgNoteDelta

        if timeToSwitch < 0:
                lArray.lightUpdate()
                rArray.lightUpdate()
                timeToSwitch = float(avgNoteDelta/(700))
               
    