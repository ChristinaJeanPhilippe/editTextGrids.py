

#!/usr/bin/env python
# coding=utf-8

import os
"""
This file creates tiers for multiple speakers and copies annotations to their
corresponding speaker.
"""
import tgt
import re

primary_dir = '/home/bill/Desktop/خريف ٢٠٢١/NEH project/aeneasOutput'

tGs = os.listdir(primary_dir)   
tGs = [i for i in tGs if i.endswith(u'.TextGrid')]

tG_paths = []

for tG_ in tGs:
    tG_path = os.path.join(primary_dir,tG_)
    tG_paths.append(tG_path)

sorted_tG_paths = sorted(tG_paths)
for i in range(len(sorted_tG_paths)):
    print(i,": ",sorted_tG_paths[i])

tr_dir = '/home/bill/Desktop/خريف ٢٠٢١/NEH project/toAlign/savedSpeaker'

transc = os.listdir(tr_dir)   
transc = [i for i in transc if i.endswith(u'.txt')]

transc_paths = []

for transc_ in transc:
    transc_path = os.path.join(tr_dir,transc_)
    transc_paths.append(transc_path)

#match the files in the two
sorted_transc_paths = sorted(transc_paths)
for i in range(len(sorted_transc_paths)):
    print(i,": ",sorted_transc_paths[i])
matchedTranscriptPaths = []
matchedTGPaths = []
for i in range(len(sorted_transc_paths)):
    transcriptName = sorted_transc_paths[i].split('/')[-1]
    transcriptProj = re.findall(r'^([A-Z]+)',transcriptName)[0]
    transcriptNum = re.findall(r'^[A-Z]+[\s-](\d+[A-Z]*)',transcriptName)[0]
    for j in range(len(sorted_tG_paths)):
        #print(sorted_tG_paths[j])
        tGName = sorted_tG_paths[j].split('/')[-1]    
        tGProj = re.findall(r'^([A-Z]+)',tGName)[0]
        tGNum = re.findall(r'^[A-Z]+[\s-](\d+[A-Z]*)',tGName)[0]
        if transcriptNum ==tGNum and transcriptProj == tGProj:
            #print(i,": ",transcriptProj,transcriptNum,tGProj,tGNum)
            matchedTranscriptPaths.append(sorted_transc_paths[i])
            matchedTGPaths.append(sorted_tG_paths[j])
            continue


grids_dir = '/home/bill/Desktop/خريف ٢٠٢١/NEH project/multipleTieredAeneasOutput'

#Editing textGrids, add new tiers

testLists = []
testGrids = []
dictionaries = []
accs = []

for i in range(len(matchedTranscriptPaths)):
    transcript = matchedTranscriptPaths[i]
    tG = matchedTGPaths[i]
    gridRead = tgt.read_textgrid(matchedTGPaths[i])
    tierNames = gridRead.get_tier_names()
    with open(transcript,"r",errors="ignore") as readTransc:
        speakerLines = readTransc.readlines()
        speakers = set(speakerLines)
    #Generate tiers for speakers
    for speaker in speakers:
        gridRead.add_tier(tgt.core.IntervalTier(start_time=0,end_time=gridRead.end_time,name=speaker,objects=None))
    #Cycle through annotations in Token tier, move to each speaker tier
    tokenTier = gridRead.get_tier_by_name('Token')
    annotations = tokenTier.annotations
    numAnnotAdded = 0
    print(transcript,"Len annot: ",len(annotations),"\nLen lines: ",len(speakerLines))
    if len(annotations) > 0:
        for j in range(len(annotations)):
            annotation = annotations[j]
            speakerLine = speakerLines[j]
            speakerTier = gridRead.get_tier_by_name(speakerLine)
            speakerTier.add_annotation(annotation)
            numAnnotAdded +=1
    #acc = round(numAnnotAdded/len(annotations),2)
    #accs.append(acc)
    #print(tG,"\nNum lines= :",len(linesToMatchAnnot),"\nNum annotations: ",len(annotations),
          #"\nNum of annot added: ",numAnnotAdded,acc)
    testGrids.append(gridRead)
    gridOutFilename = tG.split('/')[-1].split('.TextGrid')[0]
    gridOutPath = os.path.join(grids_dir,gridOutFilename+".eaf")
    #tgt.write_to_file(gridRead, gridOutPath, format='short')
    tgt.write_to_file(gridRead, gridOutPath, format='eaf', include_empty_intervals=False, include_point_tiers=True)
