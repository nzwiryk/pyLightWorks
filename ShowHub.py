# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 18:28:41 2014

@author: Nicholas Zwiryk
"""

from multiprocessing import Process
import MidiMonitor
import PyStageKit as sk
from random import randint
from time import sleep

def inputHub():
    MidiMonitor.midiMonitor()
    
def lightManager():
    sk.Marquee([sk.red],1,'cw',0.2,0b11001100, MidiMonitor.avgNoteDelta)
    while MidiMonitor.avgNoteDelta < 400:
        sk.set_vibration(sk.getArrayVib(0b11111111),sk.randomColor())
        while MidiMonitor.avgNoteDelta <200:
            sk.Marquee([sk.blue],20,"cw",MidiMonitor.avgNoteDelta/100, randint(0,255),MidiMonitor.avgNoteDelta)
            

if __name__=='__main__':
    p1 = Process(target = inputHub())
   
    p2= Process(target = lightManager())
    p1.start()
    #sleep(5)
    p2.start()    



