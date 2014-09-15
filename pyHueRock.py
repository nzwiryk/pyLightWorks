# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 20:03:50 2014

@author: HTPC
"""
import phue

globalBrightness = 170
b = phue.Bridge('192.168.1.12')
b.connect()

l1 = phue.Light(b,1)
l2 = phue.Light(b,2)
l3 = phue.Light(b,3)

lights = [l1, l2, l3]

for x in lights:
    x.transitiontime = 0
    x.brightness = globalBrightness
    x.hue = 170
    x.saturation = 255
    
    
hueColors = {'red':65535, 'yellow':12750,'lightGreen': 25500,'green':36210,'blue':46920,'purple': 56100}
hueLookup = {65535:'red', 12750:'yellow', 25500:'lightGreen',36210:'green',46920:'blue', 56100:'purple'}