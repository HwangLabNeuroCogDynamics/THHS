
from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,

                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,

                   sqrt, std, deg2rad, rad2deg, linspace, asarray)

from numpy.random import random, randint, normal, shuffle,uniform,permutation
import os  # handy system and path functions
import sys  # to get file system encoding
import serial #for sending triggers from this computer to biosemi computer
import csv
import copy
from psychopy import visual, core

expInfo = {'subject': '', 'session': '01','EEG? [y/n]':'n','refresh':50}
expName='alpha_pilot'
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1680,1050],units='deg',fullscr=False,monitor='testMonitor',checkTiming=True)
no_stim=6
vis_deg=3.5


for key in ['escape']:
    event.globalKeys.add(key, func=core.quit)
    


if expInfo['EEG? [y/n]']=='y':
    EEGflag=1
else:
    EEGflag=0

if EEGflag:
    #port=serial.Serial('COM4',baudrate=115200)
    #port.close()
    startSaveflag=bytes([254])
    stopSaveflag=bytes([255])
    #cue_onset_trig=bytes([101])
    
    target_possibilities=['tarH','tarN']
    dis_possibilities=['disH','disL']
    dis_loc_possibilities=['locHR','locHL','locL']
    dis_types=['disP','disA']
    
    cue_trigDict={}
    trig_num=101
    for t in target_possibilities:
        for d in dis_possibilities:
            for l in dis_loc_possibilities:
                for type in dis_types:
                    label=t+d+l+type+'_trig'
                    trig=trig_num
                    cue_trigDict[label]=trig
                    trig_num+=2 #setting it up so that it increases by every odd number after 101
     
    probe_trigDict={}
    if trig_num == 101:
        print('oops, the cue_trigDict did not work')
        core.quit()
    tar_VI=['tarH','tarN']
    dis_VI=['disV','disI']
    disLoc_HL=['locHV','locHI','locL','locN']
    trig_num=trig_num+2
    for t in tar_VI:
        for d in dis_VI:
            for l in disLoc_HL:
                label=t+d+l+'_trig'
                trig=trig_num
                probe_trigDict[label]=trig
                trig_num+=2
    
    subNonRespTrig=bytes([trig_num+2])
    subRespTrig=bytes([trig_num+4])
    ITItrig=bytes([trig_num+6])
    endofBlocktrig=bytes([trig_num+8])
    
    other_trigDict={'startSaveflag':startSaveflag,'stopSaveflag':stopSaveflag,'ITItrig':ITItrig,'endofBlocktrig':endofBlocktrig}
    #cue_trigDict={'HHP_trig':HHP_trig,'HLP_trig':HLP_trig,'HHA_trig':HHA_trig,'HLA_trig':HLA_trig,
    #        'NLP_trig':NLP_trig,'NLA_trig':NLA_trig,'NHP_trig':NHP_trig,'NHA_trig':NHA_trig}
    #probe_trigDict={'tarVdisVH_trig':tarVdisVH_trig,'tarVdisVL_trig':tarVdisVL_trig,
    #        'tarNdisVH_trig':tarNdisVH_trig,'tarNdisVL_trig':tarNdisVL_trig,'tarVdisIH_trig':tarVdisIH_trig,'tarVdisIL_trig':tarVdisIL_trig,'tarNdisIH_trig':tarNdisIH_trig,
    #        'tarNdisIL_trig':tarNdisIL_trig}
    response_trigDict={'subNonRespTrig':subNonRespTrig,'subRespTrig':subRespTrig}
    print(cue_trigDict)
    print(probe_trigDict)
    print(other_trigDict)
    print(response_trigDict)

if EEGflag:
    filename='Z:/AlphaStudy_Data/eegData/eeg_behavior_data'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])
else:
    filename='Z:/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date']) #for dells
    #filename='/Volumes/rdss_kahwang/AlphaStudy_Data/behavData'+u'/%s_%s_%s_%s' % (expInfo['subject'], expName, expInfo['session'],expInfo['date'])

refresh_rate=expInfo['refresh']

num_trials=100 #has to be even number
num_reps=2 

#trialNum':(n),'tarVorI':tarVorI,'disCue_type':disCue_type,'dPOA':dPOA,'disVorI':disVorI,'distractor_loc':loc,'corrResp':corrKey
#blocks.update({'blockInfo_%i'%(block):{'block':block,'tarCue':thisBlock[0],'disCue':thisBlock[1],'highProbLoc?':disProb,'likely_dis':saveDis,'likelyDisHemisphere':disHemi,'trialsData':trialDataList}})

def pracCond(thisBlock,n_practrials=4,demo=False):
    pracDataList=[]
    disCueprac=[]
    for r in range(int(n_practrials/2)):
        disCueprac.append('disP')
        disCueprac.append('disA')
    
    for n in range(n_practrials):
        ITI=2.0
        # info for this block --for subject ######################################
        if n==0:
            for circs in stimuli:
                circs.opacity = 0 
            #fixation.Autodraw=False
            if demo:
                info_msg3=visual.TextStim(win,pos=[0,0],units='norm',text='Begin demonstration')
                info_msg3.draw()
            else:
                info_msg3=visual.TextStim(win,pos=[0,0],units='norm',text='Begin practice block')
                info_msg3.draw()
            win.update()
            core.wait(2)
            fixation.text='+'
            fixation.draw()
            win.flip()
            core.wait(3)# pre-block pause
        for circs in stimuli:
            circs.opacity=1
            circs.setLineColor([0,0,0])
            circs.size=(circs.size[0]/3,circs.size[1]/3)
            circs.pos=(circs.pos[0]/3,circs.pos[1]/3)
        cue_target_1=np.random.choice(right_stim,1)[0]
        cue_target_2=np.random.choice(left_stim,1)[0]
        if thisBlock[0]=='tarH':
            cue_target_1.setLineColor([0,0,255],colorSpace='rgb255') 
            cue_target_2.setLineColor([0,0,255], colorSpace='rgb255')
        #print(disCue_scramble[n])
        fixation.autoDraw=False
        fixation.text=''
        if disCueprac[n]=='disP':
            fixation_DP.autoDraw=True
        elif disCueprac[n]=='disA':
            fixation_DA.autoDraw=True #yellow
        #print(disCueprac)
        wait_here(.5) # ############## Cue presentation ###################
        fixation_DA.autoDraw=False
        fixation_DP.autoDraw=False
        fixation.color=[1,1,1]
        fixation.text='+'
        fixation.autoDraw=True
        for circs in stimuli:
            circs.setLineColor([0,0,0],colorSpace='rgb')
            circs.size=(circs.size[0]*3,circs.size[1]*3)
            circs.pos=(circs.pos[0]*3,circs.pos[1]*3)
        wait_here(1.5) # ############ delay one/SOA period ###############
        target_loc1 = list(right_stim).index(cue_target_1) #where are the two cued circles?
        stim_minus_one = np.delete(right_stim, target_loc1)
        target_loc2 = list(left_stim).index(cue_target_2) 
        stim_minus_two = np.delete(left_stim,target_loc2) #get a list of stimuli that don't include cued circles
        stim_minus_both=list(stim_minus_one)+list(stim_minus_two)
        #stim_minus_both_dis=np.delete(stim_minus_both[:],stim_minus_both.index(likely_dis))
        if thisBlock[0]=='tarH' or thisBlock[0]=='tarN':
            which_circle=np.random.choice([cue_target_1,cue_target_2],1,p=[0.5,0.5])[0] #putting target in one of the circles
            stim_minus_both_tar=stim_minus_both #the target is in the 2 cue circles so these lists are equivalent
        if thisBlock[1]=='disH': # if the distractor cue is valid 100%
            #if disCue_scramble[n]=='disA'
            if disCueprac[n]=='disP': # or the distractor cue was distractor present, then do display distractors
                #if thisBlock[2]=='HP':
                if thisBlock[2]=='LP': #if the distractor location can be randomized then put it anywhere but where we just put the target
                    distractor_stim.pos=np.random.choice(stim_minus_both_tar,1)[0].pos
                    HPorLP='random'
        if disCueprac[n]=='disP':
            distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
            distractor_stim.opacity=1
            distractor_stim.draw()
        target_stim.pos=which_circle.pos
        target_stim.ori=5
        while target_stim.ori==5 or (target_stim.ori == distractor_stim.ori) or (target_stim.ori+180 == distractor_stim.ori) or (target_stim.ori-180==distractor_stim.ori):
            target_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the target
        target_stim.opacity=1
        target_stim.draw()
        if target_stim.ori==0:
            corrKey='up'
        elif target_stim.ori==90:
            corrKey='right'
        elif target_stim.ori==180:
            corrKey='down'
        elif target_stim.ori==270:
            corrKey='left'
        for s in range(len(stimuli)): 
            circs=stimuli[s]
            if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or (disCueprac[n]=='disP' and (circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): 
                #if the circle is not a target or distractor then put other_stim in it
                #circs.setLineColor([255,255,0],colorSpace='rgb255')
                circs.setLineColor([1,-1,-1]) #if the circle is a non singleton distractor make it red
                circs.setFillColor(None)
                redL[s].ori=(np.random.choice([0,90,180,270],1))[0]
                redL[s].pos=circs.pos
                redL[s].opacity=1
                redL[s].draw()
            elif (circs.pos[0]==target_stim.pos[0] and circs.pos[1]==target_stim.pos[1]):
                circs.setLineColor([1,-1,-1]) #if the circle is a target we want it to be red, too
                circs.setFillColor(None)
            else: #if the circle is a chosen distractor, make it yellow
                circs.lineColorSpace='rgb255'
                circs.setLineColor([255,255,0])
                circs.setFillColor(None)
        win.update()
        clock=core.Clock()
        if not demo:
            subResp= event.waitKeys(1.5,keyList=['up','down','left','right'],timeStamped=clock)
            if subResp==None:
                trial_corr=0
            else:
                if subResp[0][0]==corrKey:
                    trial_corr=1
                else:
                    trial_corr=0
        else: 
            core.wait(1.5)
        fixation.draw()
        for circs in stimuli:
            circs.lineColorSpace='rgb'
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
        for letter in other_stim:
            letter.opacity=0
        distractor_stim.opacity=0
        target_stim.opacity=0
        if not demo:
            Thistrial_data= trial_corr
            pracDataList.append(Thistrial_data)
        win.flip()
        core.wait(ITI)
        for circs in stimuli:
            circs.opacity=0
    fixation.autoDraw=False
    if not demo:
        #fixation.color=([0,0,0])
        acc_feedback=visual.TextStim(win, pos=[0,.5],units='norm',text='Your accuracy for the practice round was %i percent. Practice again? (y/n)' %(100*(np.sum(pracDataList)/n_practrials)))
        acc_feedback.draw()
        win.update()
        cont=event.waitKeys(keyList=['y','n'])
        fixation.color=([1,1,1])
        if cont[0]=='y':
            pracCond(thisBlock,n_practrials)
 
def wait_here(t):
    interval=1/refresh_rate
    num_frames=int(t/interval)
    for n in range(num_frames): #change back to num_frames
        fixation.draw()
        win.flip()

def make_ITI():
    if not EEGflag:
        ITI=np.random.choice([1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6],1)[0] #averages to around 2 second?
    else:
        ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI

def make_csv(filename,expStart=False):
    with open(filename+'.csv', mode='w') as csv_file:
        fieldnames=['block','tarCue_validity','disCue_validity','highProbLoc?','highProbLocation','likelyDisHemisphere','trialNum','disCue','disPresentOrAbsent','disVorI','distractor_loc','corrResp','subResp','trialCorr?','RT','stim_loc(T,D)','ITI','trial_trigs','triggers']
        #fieldnames is simply asserting the categories at the top of the CSV
        writer=csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        print('\n\n\n')
        for n in range(len(blocks.keys())): # loop through each block
            blocks_data = list(blocks.keys())[n]
            ThisBlock=blocks[blocks_data] #grabbing the block info for this block
            #print(ThisBlock)
            #print('\n')
            for k in range(len(ThisBlock['trialsData'])): #this should be the # of trials
                ThisTrial=ThisBlock['trialsData'][k] #grabbing the trial info out of data for this trial
                #print(ThisTrial)
                if ThisBlock['tarCue']=='tarH':
                    tvalid='100%'
                else:
                    tvalid='None'
                if ThisBlock['disCue']=='disH':
                    dvalid='100%'
                else:
                    dvalid='50%'
                
                if EEGflag and expStart==True and k==0:
                    writer.writerow({'block':ThisBlock['block'],'tarCue_validity':tvalid,'disCue_validity':dvalid, 'highProbLoc?':ThisBlock['highProbLoc?'], 'highProbLocation':ThisBlock['likely_dis'],
                                    'likelyDisHemisphere':ThisBlock['likelyDisHemisphere'],'trialNum':ThisTrial['trialNum'],
                                    'disCue':ThisTrial['disCue_type'],'disPresentOrAbsent':ThisTrial['dPOA'],'disVorI':ThisTrial['disVorI'],'distractor_loc':ThisTrial['distractor_loc'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'stim_loc(T,D)':ThisTrial['stim_loc'],
                                    'ITI':ThisTrial['ITI'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':(cue_trigDict,probe_trigDict,response_trigDict,other_trigDict)})
                else:
                    writer.writerow({'block':ThisBlock['block'],'tarCue_validity':tvalid,'disCue_validity':dvalid, 'highProbLoc?':ThisBlock['highProbLoc?'], 'highProbLocation':ThisBlock['likely_dis'],
                                    'likelyDisHemisphere':ThisBlock['likelyDisHemisphere'],'trialNum':ThisTrial['trialNum'],
                                    'disCue':ThisTrial['disCue_type'],'disPresentOrAbsent':ThisTrial['dPOA'],'disVorI':ThisTrial['disVorI'],'distractor_loc':ThisTrial['distractor_loc'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'stim_loc(T,D)':ThisTrial['stim_loc'],
                                    'ITI':ThisTrial['ITI'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':''})

if no_stim==6:
    one_oclock = visual.Circle(
    
            win=win, name='1',
    
            size=(0.09, 0.15),
    
            ori=0, pos=((vis_deg/2), (sqrt(3)/2*vis_deg)),
    
            lineWidth=7, lineColor=None, lineColorSpace='rgb',
    
            fillColor=None, fillColorSpace='rgb',
    
            opacity=1, depth=-1.0, interpolate=True)
    
    one_oclock.setAutoDraw(True)
    three_oclock = visual.Circle(
        win=win, name='3',

        size=(0.09, 0.15),

        ori=0, pos=(vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    three_oclock.setAutoDraw(True)
    
    five_oclock = visual.Circle(

        win=win, name='5',

        size=(0.09, 0.15),

        ori=0, pos=((vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    five_oclock.setAutoDraw(True)
    seven_oclock = visual.Circle(

        win=win, name='7',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), -((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-5.0, interpolate=True)

    seven_oclock.setAutoDraw(True)
    nine_oclock = visual.Circle(

        win=win, name='9',

        size=(0.09, 0.15),

        ori=0, pos=(-vis_deg, 0),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-3.0, interpolate=True)

    nine_oclock.setAutoDraw(True)
    eleven_oclock = visual.Circle(

        win=win, name='11',

        size=(0.09, 0.15),

        ori=0, pos=(-(vis_deg/2), ((sqrt(3)/2)*vis_deg)),

        lineWidth=7, lineColor=None, lineColorSpace='rgb',

        fillColor=None, fillColorSpace='rgb',

        opacity=1, depth=-1.0, interpolate=True)

    eleven_oclock.setAutoDraw(True)
    stimuli=[one_oclock,three_oclock,five_oclock,seven_oclock,nine_oclock,eleven_oclock]
    right_stim=stimuli[:3]
    left_stim=stimuli[3:]

size=(.2,.2)
images={'blue_diamond':visual.ImageStim(win=win,name='blue_diamond', units='norm', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/blue_diamond.png'),
    'red_diamond':visual.ImageStim(win=win,name='red_diamond', units='norm', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/red_diamond.png'),
    'yellow_diamond':visual.ImageStim(win=win,name='yellow_diamond', units='norm', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/yellow_diamond.png'),
    'blue_circle':visual.ImageStim(win=win,name='blue_circle', units='norm', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/blue_circle.png'),
    'red_circle':visual.ImageStim(win=win,name='red_circle', units='norm', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/red_circle.png'),
    'yellow_circle':visual.ImageStim(win=win,name='yellow_circle', units='norm', 
    ori=0, size=size,image=os.getcwd()+'/stimuli/yellow_circle.png')}
stimuli=images.keys()

distractor_name=np.random.choice(stimuli,1)[0]
if 'blue' in distractor_name:
    target_color=np.random.choice(['red','yellow'],1)[0]
elif 'yellow' in distractor_name:
    target_color=np.random.choice(['red','blue'],1)[0]
elif 'red' in distractor_name:
    target_color=np.random.choice(['blue','yellow'],1)[0]

if 'circle' in distractor_name:
    target_shape='diamond'
    other_shape='circle'
elif 'diamond' in distractor_name:
    target_shape='circle'
    other_shape='diamond'

distractor_stim=images[distractor_name]
target_stim=images[target_color+'_'+target_shape]
other_stim=[copy.copy(images[target_color+'_'+other_shape]) for i in range(no_stim-2)] # making 4 copies of Other_shape 

print(distractor_shape)

for stim in stimuli:
    stim.size=(1.5,1.5)
    stim.lineWidth=5

distractor_stim.opacity=0
target_stim.opacity=0
distractor_stim.autoDraw=True
target_stim.autoDraw=True

for stim in other_stim:
    stim.autoDraw=True
fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6

intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see a series of circles that will indicate the location of the RED target "T"')
intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')
intro_msg.draw()
intro_msg2.draw() 
intro_msg3.draw()
win.flip()
event.waitKeys()
intro_mesg4= visual.TextStim(win,pos=[0,.5],units='norm',text='Please remain focused on the cross in the middle of the screen whenever there are NOT circles on the screen.')
intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Respond to the orientation of the RED capital "T" using the arrow keys on the keyboard')
intro_mesg6=visual.TextStim(win,pos=[0,-0.5],units='norm',text='You will also sometimes see a YELLOW T. Do NOT respond to the orientation of the YELLOW T. Press any key to continue.')
intro_mesg4.draw()
intro_mesg5.draw()
intro_mesg6.draw()
win.flip()
event.waitKeys()
win.flip()

#targetlist=['tarH','tarN']
cue_list=['dis','neut'] # high prob distractor loc OR randomized prob

stimList=[]
for c in cue_list:
    for n in range(num_trials):
        stimList.append(c)

stimList_blocks=[]
for n in num_reps: 
    stimList_scramble=list(np.random.permutation(stimList))
    stimList_blocks.append(stimList_scramble)

if EEGflag:
    port.open()
    #win.callonFlip(pport.setData,delay1trig)
    port.write(startSaveflag)
    #port.close()

blocks={} # where we will save out the data
likely_dis= np.random.choice(stimuli,1)[0]

#pracBlock=['tarN','disH','LP']
#pracCond(thisBlock=pracBlock,n_practrials=6,demo=True)
#pracCond(thisBlock=pracBlock,n_practrials=8,demo=False)

for block in range(len(stimList_blocks)):
    
    trialDataList=[]
    
    fixation.color=([0,0,0])
    if block !=0:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to continue to the next block')
    else:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin experiment')
    info_msg2.draw()
    win.update()
    key1=event.waitKeys()
    fixation.color=([1,1,1])
    fixation.text='+'
    fixation.draw()
    win.flip() 
    core.wait(3)# pre-block pause
    thisBlock=stimList[block]
    
    neutCue=[]
    for r in range(int(num_trials/4)): # want 1/4 each of present and absent so that it'll = 1/2 neutral trials of total trials
        neutCue.append('P')
        neutCue.append('A')
    
    print(thisBlock)
    neutCue_scramble=np.random.permutation(neutCue)
    #print(disCue_scramble)
    
    for trial in range(len(thisBlock)):
        ITI=make_ITI()
        
        for circs in stimuli:
            circs.opacity=1
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
            circs.size=(circs.size[0]/3,circs.size[1]/3)
            circs.pos=(circs.pos[0]/3,circs.pos[1]/3)
        
        if thisBlock[trial]=='neut':
            cue_circ=np.random.choice(stimuli,6)
            for c in cue_circ:
                cue_circ.autoDraw=True
        elif thisBlock[trial]=='dis':
            cue_circ=np.random.choice(stimuli,1)
            cue_circ[0].autoDraw=True
            
        fixation.autoDraw=True
        
        if EEGflag:
            win.callOnFlip(port.write,bytes([thistrialFlag]))
        
        wait_here(1) # ############## Cue presentation ###################
        
        fixation.autoDraw=True
        for circs in stimuli:
            circs.autoDraw=False
            circs.setLineColor([0,0,0],colorSpace='rgb')
            circs.pos=(circs.pos[0]*3,circs.pos[1]*3)
        
        wait_here(1.5) # ############ delay one/SOA period ###############
        
        if thisBlock[trial]=='dis':
            cue_loc=list(stimuli).index(cue_circ)
            stim_minus_cue=np.delete(stimuli, cue_loc)
            #target_loc1 = list(right_stim).index(cue_target_1) #where are the two cued circles?
            #stim_minus_one = np.delete(right_stim, target_loc1)
            #target_loc2 = list(left_stim).index(cue_target_2) 
            #stim_minus_two = np.delete(left_stim,target_loc2) #get a list of stimuli that don't include cued circles
            #stim_minus_both=list(stim_minus_one)+list(stim_minus_two)
            #stim_minus_both_dis=np.delete(stim_minus_both[:],stim_minus_both.index(likely_dis))
            which_circle=np.random.choice(stim_minus_cue,1)[0]
            distractor_stim.pos==stimuli[cue_loc].pos
        if thisBlock[trial]=='neut': 
            which_circle=np.random.choice(stimuli,1)[0]
            if neutCue_scramble.pop()=='P':
                distractor_stim.pos=which_circle.pos
                while distractor_stim.pos ==which_circle.pos:
                    distractor_stim.pos==np.random.choice(stimuli,1)[0].pos
                distractor_stim.autoDraw=True
        
        target_stim.pos=which_circle.pos
        #target_stim.ori=5
        #while target_stim.ori==5 or (target_stim.ori == distractor_stim.ori) or (target_stim.ori+180 == distractor_stim.ori) or (target_stim.ori-180==distractor_stim.ori):
        #    target_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the target
        #target_stim.opacity=10
        target_stim.autoDraw=True
        
        if target_stim.ori==0:
            corrKey='up'
        elif target_stim.ori==90:
            corrKey='right'
        elif target_stim.ori==180:
            corrKey='down'
        elif target_stim.ori==270:
            corrKey='left'
        
        
        
        #distractor_stim.ori= (np.random.choice([0,90,180,270],1))[0] #choose the orientation of the distractor
        for s in range(len(stimuli)): 
            circs=stimuli[s]
            if not (((circs.pos[0]==target_stim.pos[0]) and (circs.pos[1]==target_stim.pos[1])) or (HPorLP !='noDis'and (circs.pos[0]==distractor_stim.pos[0]) and (circs.pos[1]==distractor_stim.pos[1]))): 
                #if the circle is not a target or distractor then put other_stim in it
                #redL[s].ori=(np.random.choice([0,90,180,270],1))[0]
                other_stim[s].pos=circs.pos
                other_stim[s].autoDraw=True
        
            
        if EEGflag:
                # port.flush()
                win.callOnFlip(port.write,bytes([probetrig]))
#            if EEGflag:
#                port.open()
        
        #wait_here(2) # ############### probe presentation ####################
        
        event.clearEvents()
        max_win_count=int(2/(1/refresh_rate))
        win_count=0
        subResp=None
        clock=core.Clock()
        while not subResp:
            win.flip()
            subResp=event.getKeys(keyList=['up','down','left','right'], timeStamped=clock)
            win_count=win_count+1
            if win_count==max_win_count:
                break
        
        if not subResp:
            if EEGflag:
                port.write(subNonRespTrig)
                resp_trig=subNonRespTrig
            
            trial_corr=np.nan
            RT=np.nan
            key='None'
        else:
            if EEGflag:
                port.write(subRespTrig)
                resp_trig=subRespTrig
            if subResp[0][0]==corrKey:
                trial_corr=1
            else:
                trial_corr=0
                
            RT=subResp[0][1]
            key=subResp[0][0]
        
        fixation.draw()
        for circs in stimuli:
            circs.lineColorSpace='rgb'
            circs.setLineColor([0,0,0])
            circs.setFillColor([0,0,0])
        for circs in other_stim:
            circs.opacity=0
        target_stim.opacity=0
        distractor_stim.opacity=0
        
        win.flip()
        #core.wait(ITI)
        
        
        for stim in stimuli:
            if (stim.pos[0]==target_stim.pos[0]) and (stim.pos[1]==target_stim.pos[1]):
                target_circle=stim
        if (HPorLP !='noDis'):
            for stim in stimuli:
                if (stim.pos[0]==distractor_stim.pos[0]) and (stim.pos[1]==distractor_stim.pos[1]):
                    distractor_circle=stim
            stim_loc=(target_circle.name,distractor_circle.name)
        elif HPorLP=='noDis':
            stim_loc=(target_circle.name,'noDis')
        
        # # translating things so that the output to the CSV file is a bit more readable
        if disVorI=='V':
            disVorI='valid'
        else:
            disVorI='invalid'
        
        if disCue_scramble[n]=='disA':
            disCue_type='Absent'
        else:
            disCue_type='Present'
        
        if HPorLP=='hp':
            loc='high prob'
            dPOA='Present'
        elif HPorLP=='lp':
            loc='low prob'
            dPOA='Present'
        elif HPorLP=='random':
            loc='random prob'
            dPOA='Present'
        elif HPorLP=='noDis':
            loc='None'
            dPOA='Absent'
        if EEGflag:
            Thistrial_data= {'trialNum':(n),'disCue_type':disCue_type,'dPOA':dPOA,'disVorI':disVorI,'distractor_loc':loc,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 'stim_loc':stim_loc,'ITI':ITI,'trial_trigs':(thistrialFlag,probetrig,resp_trig)}
        else:
            Thistrial_data= {'trialNum':(n),'disCue_type':disCue_type,'dPOA':dPOA,'disVorI':disVorI,'distractor_loc':loc,'corrResp':corrKey,'subjectResp':key,'trialCorr?':trial_corr,'RT':RT, 'stim_loc':stim_loc,'ITI':ITI,'trial_trigs':'None'}
        trialDataList.append(Thistrial_data)
        
        print(Thistrial_data)
        
        key=event.getKeys()
        if key: 
            if key[0]=='escape': 
                win.close()
                core.quit()
                print('FORCED QUIT')
        
        if EEGflag:
            win.callOnFlip(port.write,ITItrig)
            
        #core.wait(ITI) #ITI--want to jitter this?, with an average of 4 seconds
        wait_here(ITI)
#            port.close()
#            
    if thisBlock[2]=='HP':
        saveDis=likely_dis.name
        disProb='Yes'
        disHemi=likely_hemi
    else:
        saveDis='randomized'
        disProb='No'
        disHemi='randomized'
    
    blocks.update({'blockInfo_%i'%(block):{'block':block,'tarCue':thisBlock[0],'disCue':thisBlock[1],'highProbLoc?':disProb,'likely_dis':saveDis,'likelyDisHemisphere':disHemi,'trialsData':trialDataList}})
    
    # #########################saving data out###########################################
    if block==0:
        make_csv(filename,expStart=True)
    else:
        make_csv(filename,expStart=False)
    if EEGflag:
        port.write(endofBlocktrig)
    if block==int(len(stimList)/2)-1:
        exit_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='You are halfway through the study!')
        exit_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Please take a break and, when done, call the experimenter over to continue')
        exit_msg.draw() 
        exit_msg3.draw()
        win.flip()
        event.waitKeys(keyList=['q'])

if EEGflag:
    port.write(stopSaveflag)
    port.close()

for stim in stimuli:
    stim.autoDraw=False
fixation.autoDraw=False
 
exit_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Thank you for participating in our experiment!')
exit_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='Your time and cooperation is greatly appreciated.')
exit_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to exit')
exit_msg.draw()
exit_msg2.draw() 
exit_msg3.draw()

win.flip()
event.waitKeys()