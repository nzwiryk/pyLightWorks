# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 19:17:12 2014

@author: Nicholas Zwiryk
"""

from collections import deque
import pygame.midi as midi
import numpy as np
import PyStageKit as sk
import time
import config


noteMidi = {'kick':36, 'snare':38, 'yellowTom':48, 'blueTom':45, 'greenTom':43,'closedHiHat':42,'openHiHat':51,'ride':59, 'crash':49}
midiNote = {36:'kick', 38:'snare', 48:'yellowTom', 45:'blueTom', 43:'greenTom',42:'closedHiHat',51:'openHiHat',59:'ride', 49:'crash'}
#noteChart = {'kick':0, 'snare':0, 'yellowTom':0, 'blueTom':0, 'greenTom':0,'closedHiHat':0,'openHiHat':0,'ride':0, 'crash':0}

binSize = 8
flagThreshold = 0.5

midi.quit()
midi.init()
m = midi.Input(1,4096)
noteBin = deque('',binSize)
timeBin = deque('',binSize)
velocityBin = deque('',binSize)
histBin = [36,38,42,43,45,48,49,51,60]
sensitivity = 0.2
timeBin.append(0)

def calcFlagNotes(threshold):
    noteThresholdCount = binSize*flagThreshold 
    for key, value in config.noteChart.itemitems():
        if value >= noteThresholdCount:
            return noteMidi[key]
        else:
            return 0

def getCrashFlag():
    if config.noteChart['crash'] == 0:
        return True
    else:
        return False

def midiMonitor():
    avgNoteDelta = 75
    oldNoteDelta = 1
    avgVelocity = 64
    timeToSwitch = 0.1
    lastTimeStamp = time.time()
    sk.lightBoot()
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
                
                if getCrashFlag() and lastNote == midiNote['crash']:
                    accentFlag = True
                #print avgNoteDelta
                for x in noteHist[1][0:len(noteHist[1])-1]:
                    config.noteChart[midiNote[x]]=list(noteHist[0])[list(noteHist[1]).index(int(x))]
                if lastNote == calcFlagNotes(flagThreshold):
                    accentFlag = True
                
        if accentFlag:
           sk.set_vibration(65535,65535)
           time.sleep(0.02)
           accentFlag = False
           sk.AllOff()
           sk.lightBoot()
           
        if (oldNoteDelta + sensitivity*oldNoteDelta) <avgNoteDelta or (oldNoteDelta - sensitivity*oldNoteDelta) > avgNoteDelta:
            sk.updateVector(avgVelocity,avgNoteDelta)
            sk.updatePattern()
            sk.updateHue()
            sk.lightBoot()
            #print 'update!'
        
        
        timeToSwitch -= (time.time() - lastTimeStamp)
        lastTimeStamp = time.time()
        oldNoteDelta = avgNoteDelta
       # print timeToSwitch
        if timeToSwitch < 0:
                sk.lightUpdate()
                timeToSwitch = float(avgNoteDelta/(700))
               
                #print timeToSwitch