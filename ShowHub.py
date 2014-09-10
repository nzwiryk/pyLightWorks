# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 18:28:41 2014

@author: Nicholas Zwiryk
"""

import threading
import MidiMonitor
import PyStageKit as sk
import config


sk.AllOff()
def inputHub():
   MidiMonitor.midiMonitor()
    
def lightManager():
    while MidiMonitor.midi.time()-config.lastTimeStamp<6000000:
       sk.updateVector()
       sk.Marquee(config.avgNoteDelta/50)
        
        
         

if __name__=='__main__':
    threading.Thread(target = inputHub).start()
    threading.Thread(target = lightManager).start()



