#!/usr/bin/env ipython

##PARSE TIME AND DATE##
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text
#replace 'FILE' WITH EXACT FILE NAME###
f1 = open('C2Q175P1_7_abcefgh.csv').read() #opens original csv file as string 'f1'
f2 = open('parsed_C2Q175P1_7_abcefgh.csv', 'w') #creates new file to write the parsed data to via file object 'f2'
reps = {' ':',', '/':'_', 'RealTime':'Date', 'Event':'Realtime'} 
	#entry 0: split date and time; replace the space with comma delimiter
	#entry 1: replace / in date with _
	#entries 2,3: adjust column headers
f1parsed = replace_all(f1, reps) #creates string with edited f1 data
f2.write(f1parsed) #writes parsed data to file stored in f2
f2.close() #closes file object

##FILTER TEMPERATURE DATA##
#in column 10 (K), if the difference between numerical lines is less than -0.2 or greater than 0.2, remove line
f2 = open("parsed_C2Q175P1_7_abcefgh.csv")
f3 = open("filtered_parsed_C2Q175P1_7_abcefgh.csv", "w")
f3.write("ElapsedTime,Date,Realtime, , ,I1Num,I1RR-I,I1RR-I(SD),I1HR,I1HR(SD),I2T_Mean,I2T_Mean(SD),I3A_TA,I3A_TA(SD)\r\n") #adds corrected header
saved = 36.23 #whatever first value in row is
f2.readline() #skips first line in f2
for line in f2:
    fields = line.split(",") #tells code values delimited by comma
    if abs(float(fields[10]) - saved) > 0.30:
        print "outlier" #so we can see output
    else:
        f3.write(line) #writes the lines with accurate data to new file
    saved = float(fields[10]) #updates saved value to last non-outlier body temp
f2.close()
f3.close()

##CONDITIONAL: EXTRACT DATA AT CONTOLLED ACTIVITY LEVELS##
#active heartrate: extract lines with activity between 3 and 4 units (row[12])
f3 = open("filtered_parsed_FILE.csv") 
f3.readline()
f4 = open("activeHR_FILE.csv", "w")
f4.write("ElapsedTime,Date,Realtime, , ,I1Num,I1RR-I,I1RR-I(SD),I1HR,I1HR(SD),I2T_Mean,I2T_Mean(SD),I3A_TA,I3A_TA(SD)\r\n")
for line in f3:
    fields = line.split(",")
    if float(fields[12]) >= 3 and float(fields[12]) <= 4:
        f5.write(line)
f3.close()
f4.close()

#resting heartrate: extract lines with activity = 0 following at least one full minute of rest
f3 = open("filtered_parsed_FILE.csv")
f3.readline()
f5 = open("restHR_FILE.csv", "w")
f5.write("ElapsedTime,Date,Realtime, , ,I1Num,I1RR-I,I1RR-I(SD),I1HR,I1HR(SD),I2T_Mean,I2T_Mean(SD),I3A_TA,I3A_TA(SD)\r\n")
counts = 0
for line in f3:
    fields = line.split(",")
    if float(fields[12]) == 0:
        counts = counts + 1 #if mouse has no activity, add to counts
    else:
        counts == 0 #if there is activity, reset counter to 0
    if counts > 2 and float(fields[12]) == 0:
        f5.write(line) #if counts is greater than 2, there are at least 3 preceding lines (1 minute) of no activity; write the current line to resting HR document
f3.close() #close files
f5.close()


#Graphing in R
	#talk to Tamara
	#level of activity: young/WT, young/Q175 and old/WT, old/Q175
	#HR, high activity: young/WT, young/Q175 and old/WT, old/Q175
	#HR, no activity: young/WT, young/Q175 and old/WT, old/Q175
	#Temp, high activity: young/WT, young/Q175 and old/WT, old/Q175
	#Temp activity: young/WT, young/Q175 and old/WT, old/Q175
	
##highlight files with full 24 hours of continuous recording##
	#in column 0, "ElapsedTime", if row_n - row_(n-1) = 20, do nothing
	#if row_n - row_(n-1) > 20, flag
	#for every 4320+ lines that are unflagged, export to a new file
