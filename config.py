# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 19:50:15 2014

@author: Nicholas Zwiryk
"""

import pyHueRock as hr

avgNoteDelta = 300
avgVelocity = 50
lastNotes = []
noteChart = {'kick':0, 'snare':0, 'yellowTom':0, 'blueTom':0, 'greenTom':0,'closedHiHat':0,'openHiHat':0,'ride':0, 'crash':0}
lastTimeStamp = 0
#colorVector = {'red':0,'blue':0,'green':0,'yellow':0}
hueColorState = {hr.l1:hr.hueColors['red'], hr.l2:hr.hueColors['purple'], hr.l3:hr.hueColors['blue']}

#patternVector = {'red':0b10000000,'blue':0b00000001,'green':0b10101010,'yellow':000010001}
patternStates = [0b00000001,0b00110011,0b10101010,0b10001001, 0b00010001, 0b11111111]