# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 18:28:41 2014

@author: Nicholas Zwiryk
"""

import threading
import MidiMonitor
import PyStageKit as sk
import config
from time import sleep

sk.AllOff()
def inputHub():
   MidiMonitor.midiMonitor()
    
def lightManager():
    while MidiMonitor.midi.time()-config.lastTimeStamp<6000000:
       sk.colorVector = {'red':0,'blue':0,'green':0,'yellow':0}
       sk.AllOff()
       sk.updateVector()
       sk.Marquee(config.avgNoteDelta/1000)
       print config.avgNoteDelta
       print config.avgVelocity

        
def fogManager():
    while MidiMonitor.midi.time()-config.lastTimeStamp<600000:
        sk.set_vibration(65535,256)
        sleep(120)
        sk.set_vibration(65535,512)
        sleep(6000)
        
         

if __name__=='__main__':
    threading.Thread(target = inputHub).start()
    threading.Thread(target = lightManager).start()
    threading.Thread(target = fogManager).start()


