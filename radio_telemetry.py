#!/usr/bin/env ipython

##parse out time and date##
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

###REPLACE 'FILE' WITH EXACT FILE NAME###
f1 = open('FILE.csv').read() #opens original csv file as string 'f1'
f2 = open('parsed_FILE.csv', 'w') #creates new file to write the parsed data to via file object 'f2'
reps = {' ':',', '/':'_', 'RealTime':'Date', 'Event':'Realtime'} 
	#entry 0: split date and time; replace the space with comma delimiter
	#entry 1: replace / in date with _
	#entries 2,3: adjust column headers
f1parsed = replace_all(f1, reps) #creates string with edited f1 data
f2.write(f1parsed) #writes parsed data to file stored in f2
f2.close() #closes file object

#noise filtering on temperature data
#in column J, if the difference between numerical lines is less than -0.2 or greater than 0.2, flag the line
#this will highlight unrealistic body temperature changes resulting from erroneous readings

##highlight files with full 24 hours of continuous recording##
	#in column 0, "ElapsedTime", if row_n - row_(n-1) = 20, do nothing
	#if row_n - row_(n-1) > 20, flag
	#for every 4320+ lines that are unflagged, export to a new file

##conditional to select heart rate data at certain activity levels##
	#resting heart rate:
		#if activity (column 11 (L)) = 0 for three consecutive 20s periods, extract any data lines immediately following if they too have activity = 0
		#extract lines with activity between 3 and 4 units

#Graphing in R
	#talk to Tamara
	#level of activity: young/WT, young/Q175 and old/WT, old/Q175
	#HR, high activity: young/WT, young/Q175 and old/WT, old/Q175
	#HR, no activity: young/WT, young/Q175 and old/WT, old/Q175
	#Temp, high activity: young/WT, young/Q175 and old/WT, old/Q175
	#Temp activity: young/WT, young/Q175 and old/WT, old/Q175
