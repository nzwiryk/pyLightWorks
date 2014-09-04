# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 13:41:13 2014

@author: Nicholas Zwiryk
"""

from collections import deque
import pygame.midi as midi
import numpy as np





midi.init()
if m != 0:
    m = 0
m = midi.Input(1,4096)

noteBin = deque('',16)
noteDelta = []
def midiMonitor():
    global avgNoteDelta
    avgNoteDelta = 0
    while True:     
        note = m.read(1)     
        if note != []:          
            if note[0][0][0]!=128:
                noteDelta = []            
                key = note[0][0][1]
                #print key
                noteBin.appendleft(note)
                for x in noteBin:
                    noteDelta.append(x[0][1])
                avgNoteDelta  = abs(np.mean(np.diff(noteDelta)))
                print avgNoteDelta
            