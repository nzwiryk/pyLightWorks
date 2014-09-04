# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 18:55:24 2014

@author: Nicholas Zwiryk
"""

import ctypes
red = 32768
blue = 8192
green = 16384
yellow= 24576
fogon = 256
fogoff = 512

ledarray = {'00000001':256,
            '00000010':512,
            '00000011':768,
            '00000100':1024,
            '00000101':1280,
            '00000110':1536,
            '00000111':1792,
            '00001000':2048,
            '00001001':2304,
            '00001010':2560,
            
            }
# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll

# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint

# Now we're ready to call it.  Set left motor to 100%, right motor to 50%
# for controller 0
vibration = XINPUT_VIBRATION(65535, 65535)
XInputSetState(0, ctypes.byref(vibration))

# You can also create a helper function like this:
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor), int(right_motor))
    XInputSetState(controller, ctypes.byref(vibration))

# ... and use it like so
#set_vibration(0, 1.0, 0.5)