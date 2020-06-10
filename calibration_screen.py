from __future__ import absolute_import, division, print_function
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock, info
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.info import RunTimeInfo
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
from random import choice as randomchoice

##### Setup the display Window
win = visual.Window(
    size=(1280, 800), fullscr=False, screen=0,
    allowGUI=False, allowStencil=False, units='deg',
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)

fixation = visual.TextStim(win=win, name='Fix_Cue',
    text=u'+', units='norm',
    font=u'Arial',
    pos=(0, 0), height=0.3, wrapWidth=None, ori=0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

dots=[visual.TextStim(win=win,text='o',color='white') for n in range(0,9)]
print(dots)

calibration=1
while calibration:
    fixation.draw()
    

