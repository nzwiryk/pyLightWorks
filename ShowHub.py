# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 18:28:41 2014

@author: Nicholas Zwiryk
"""

import threading
import MidiMonitor
import PyStageKit as sk
import config
from random import randint
from time import sleep

sk.AllOff()
def inputHub():
   MidiMonitor.midiMonitor()
    
def lightManager():
    while True:
        sk.Marquee([sk.red],1,'cw',0.2,0b11001100, config.avgNoteDelta)
        while config.avgNoteDelta < 400:
            sk.set_vibration(sk.getArrayVib(0b11111111),sk.randomColor())
            sleep(randint(0,3))
            sk.AllOff()
            while config.avgNoteDelta <200:
                sk.Marquee([sk.randomColor()],config.avgNoteDelta/30,"cw",config.avgNoteDelta/500, randint(0,255),config.avgNoteDelta)
         

if __name__=='__main__':
    threading.Thread(target = inputHub).start()
    threading.Thread(target = lightManager).start()



