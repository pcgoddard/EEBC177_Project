#!/usr/bin/env ipython

#parse out time and date
f1 = open('file.csv').read() #opens original as string 'f1'
f2 = open('parsed_file.csv', 'w') #creates new file to write the parsed data to via file object 'f2'
reps = {' ':',', '/':'_', 'RealTime':'Date', 'Event':'Realtime'} 
#entry 0: split date and time; replace the space with comma delimiter
#entry 1: replace / in date with _
#entries 2,3: adjust column headers
f1Parsed = replace_all(f1, reps) #creates string with edited f1 data
f2.write(f1Parsed) #writes parsed data to file stored in f2
f2.close() #closes file object

#highlight files with full 24 hours of continuous recording
	#in column A, "ElapsedTime", if time interval is 20s, do nothing
	#if time interval is greater than 20s, flag
	#for every 4320+ lines that are unflagged, export to a new file

#noise filtering on temperature data
	#in column J, if the difference between numerical lines is less than -0.2 or greater than 0.2, flag the line
	#this will highlight unrealistic body temperature changes resulting from erroneous readings
	
#conditional to select heart rate data at certain activity levels
	#resting heart rate:
		#if activity (column L) = 0 for three consecutive 20s periods, extract any data lines immediately following if they too have activity = 0
		#extract lines with activity between 3 and 4 units
