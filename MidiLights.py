# -*- coding: utf-8 -*-
"""
Just a test script to play with mapping MIDI inputs to my Hue Lights. Not actually called in the LightWorks.
"""

import phue
import time
from random import randint
import pygame
import pygame.midi as midi


delay = 0.5

b = phue.Bridge('192.168.1.12')
b.connect()

l1 = phue.Light(b,1)
l2 = phue.Light(b,2)
l3 = phue.Light(b,3)


lights = [l1, l2, l3]

for x in lights:
    x.transitiontime = 0
    
def pulse(id, hue, count):        
    id.brightness = 255
    id.hue = hue
    
   # id.brightness = 0
    
    #id.on = True

def randpulseall(count):
    for x in range(0,count):
        for l in lights:
            l.brightness = 0
            l.hue = randint(0,65535)
            l.brightness = 255
            
midi.init()

#m = midi.Input(1,4096)

def midiLoop():
    while True:     
        note = m.read(1)     
        if note != []:          
            if note[0][0][0]!=128:
                key = note[0][0][1]
                print key
                hue = ((key-48)*2730)
                print hue
                pulse(lights[randint(0,2)],((key-48)*2730),1)
                
def midiMonitor():
    while True:
        note = m.read(1)
        if note != []:
            print (note[0][0][0])
            print (note[0][0][1])

