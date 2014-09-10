# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 13:41:13 2014

@author: Nicholas Zwiryk
"""

from collections import deque
import pygame.midi as midi
import numpy as np
import config


noteMidi = {'kick':36, 'snare':38, 'yellowTom':48, 'blueTom':45, 'greenTom':43,'closedHiHat':42,'openHiHat':51,'ride':59, 'crash':49}
midiNote = {36:'kick', 38:'snare', 48:'yellowTom', 45:'blueTom', 43:'greenTom',42:'closedHiHat',51:'openHiHat',59:'ride', 49:'crash'}


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
                config.lastTimeStamp = lastKeyPress[0][0][1]
                lastVelocity = lastKeyPress[0][0][2]
                
                
                noteBin.appendleft(lastNote)
                timeBin.appendleft(config.lastTimeStamp)
                velocityBin.appendleft(lastVelocity)
                
                timeDelta = list(timeBin)
                config.avgNoteDelta  = abs(np.mean(np.diff(timeDelta)))
                config.lastNotes = list(noteBin)
                config.avgVelocity = np.mean(velocityBin)
                noteHist = np.histogram(list(noteBin),sorted((list(histBin))))
               
                    
                
                for x in noteHist[1][0:len(noteHist[1])-1]:
                    config.noteChart[midiNote[x]]=list(noteHist[0])[list(noteHist[1]).index(int(x))]
                    