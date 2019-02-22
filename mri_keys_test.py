
from __future__ import absolute_import, division, print_function
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock, info
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware.emulator import launchScan # Add and customize this www.psychopy.org/api/hardware/emulator.html
from psychopy.info import RunTimeInfo

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
from random import choice as randomchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import glob # this pulls files in directories to create Dictionaries/Str
import pandas as pd #Facilitates data structure and analysis tools. prepend 'np.'
#import matplotlib.pyplot as plt #This will be relevant for later functions
import pyglet as pyg
import copy
import csv


win = visual.Window(
    size=(1280, 800), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False, units='deg',
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
Fix_Cue = visual.TextStim(win=win, name='Fix_Cue',
    text=u'+', units='norm',
    font=u'Arial',
    pos=(0, 0), height=0.3, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);
print('ready')
Fix_Cue.draw()
win.flip()
b=event.waitKeys(4)
#a=event.getKeys()
#print(a)
^print(b)