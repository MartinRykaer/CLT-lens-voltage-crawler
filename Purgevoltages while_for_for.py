# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 17:11:04 2018

@author: mxg635
"""

import os
import tkinter as tk
from tkinter import filedialog
import datetime as dt
#Need to have PDFminer3k
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


root = tk.Tk()
root.withdraw()


#filename = filedialog.askopenfilename(title = "Pick the PDF file to parse")
dir_path = filedialog.askdirectory(title = "pick the file directory") #pick 2018 or 2017

#get date from file
###


def purgeextract(infilename):
    Report = open(infilename, 'rb')

    outlist = list()
    #setup
    parser = PDFParser(Report)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    #Set parameters
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    #extracting text from PDF
    extracted_text = ''
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()
    texttolist = extracted_text.split('\n')
    
    #Extracting
    found = 0 #Using this to check if the pdf file had any purge values before output
    for i in range (len(texttolist)):
        if found <2:
            if texttolist[i] == 'Type of calibration: Ion transfer (pos): Optimize C-Trap Entrance Lens --- Inject # (V)':
                stop = 0    
                y = 0
                for y in range(len(texttolist)-(i+1)):#location depends on the various calibrations - have to look through it all.

                    if 'result:' in texttolist[i+y].split() and stop == 0:
                        try:
                            outlist.append(['Entrance', texttolist[i+y].split('->')[0].split()[-1],texttolist[i+y].split('->')[1]])
                        except(IndexError):
                            outlist.append('indexissue')
                            
                        stop = 1 #Stopping this loop after it found the result - otherwise it might catch the exit value as well.
                found +=1
                
                
                
            if texttolist[i] == 'Type of calibration: HCD Transfer: Optimize C-Trap Exit Lens --- Purge # (V)':
                y=0
                stop = 0    
                for y in range(len(texttolist)-(i+1)):#Apparently it differs how far away the results are

                    if 'result:' in texttolist[i+y].split() and stop == 0:
                        try:
                            outlist.append(['Exit', texttolist[i+y].split('->')[0].split()[-1],texttolist[i+y].split('->')[1]])
                        except(IndexError):
                            outlist.append('indexissue')
                        stop = 1
                found +=1
            #if found == 2:
                #i = len(texttolist)
    if found != 0:            
        Report.close()
        return(outlist)
    else: 
        Report.close()
        return(0)

outputlist = []

for file in os.listdir(dir_path):
    #print(file[-4:])
    if file[-4:] == '.pdf' and file.split('_')[1] == 'Calibration':
        #print(file)    
        purgev = purgeextract(dir_path+'/'+file)        
        if not purgev == 0:
            outputlist.append([file.split('_')[2],str(file.split('_')[3][:-4]).replace('-',':'), purgev])
            #print(outputlist)
#print(outputlist)
outfile = open('P:/Scripting/Purge voltages crawler'+'/QE10.txt', 'w+')

for entry in outputlist:
    print('entry',entry)    
    outfile.write(str(entry[0])+'\t'+str(entry[1]))
    if len(entry[2])>=1:
        outfile.write('\t'+str(entry[2][0][0])+'\t'+str(entry[2][0][1])+'\t'+str(entry[2][0][2]))
    if len(entry[2])>=2:
        outfile.write('\t'+str(entry[2][1][0])+'\t'+str(entry[2][1][1])+'\t'+str(entry[2][1][2]))
    outfile.write('\n')                        

outfile.close()

#print(purgeextract(filename))


#purgelist.append(infilename.split('/')[-1].split('_')[-1])