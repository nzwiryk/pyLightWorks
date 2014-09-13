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


noteMidi = {'kick':36, 'snare':38, 'yellowTom':48, 'blueTom':45, 'greenTom':43,'closedHiHat':42,'openHiHat':51,'ride':59, 'crash':49}
midiNote = {36:'kick', 38:'snare', 48:'yellowTom', 45:'blueTom', 43:'greenTom',42:'closedHiHat',51:'openHiHat',59:'ride', 49:'crash'}
noteChart = {'kick':0, 'snare':0, 'yellowTom':0, 'blueTom':0, 'greenTom':0,'closedHiHat':0,'openHiHat':0,'ride':0, 'crash':0}

binSize = 16

midi.quit()
midi.init()
m = midi.Input(1,4096)
noteBin = deque('',binSize)
timeBin = deque('',binSize)
velocityBin = deque('',binSize)
histBin = [36,38,42,43,45,48,49,51,60]

def midiMonitor():
    while True:
        lastKeyPress = m.read(1)
        
        if lastKeyPress != []: 
            if lastKeyPress[0][0][0] != 128:          
                lastNote =lastKeyPress[0][0][1]
                lastTimeStamp = lastKeyPress[0][1]
                lastVelocity = lastKeyPress[0][0][2]
                
                noteBin.appendleft(lastNote)
                timeBin.appendleft(lastTimeStamp)
                velocityBin.appendleft(lastVelocity)
                
                timeDelta = list(timeBin)
                avgNoteDelta  = abs(np.mean(np.diff(timeDelta)))
                lastNotes = list(noteBin)
                avgVelocity = np.mean(velocityBin)
                noteHist = np.histogram(list(noteBin),sorted((list(histBin))))
                
                for x in noteHist[1][0:len(noteHist[1])-1]:
                    noteChart[midiNote[x]]=list(noteHist[0])[list(noteHist[1]).index(int(x))]
        
        timeToSwitch = avgNoteDelta/1000
        lastTimeStamp = time.time()
        sk.updateVector()
        sk.lightBoot()
        timeToSwitch -= time.time() - lastTimeStamp
        lastTimeStamp = time.time()
        if timeToSwitch < 0:
                sk.lightUpdate()
        print avgNoteDelta
        print avgVelocity