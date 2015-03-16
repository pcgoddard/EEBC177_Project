#!/usr/bin/env ipython

#Code assumes that the raw csv data (extracted sheet by sheet for each mouse: abc(d)efgh) is titled like: C2Q175P1_7a.csv where '7' refers to the trial day and 'a' is the specific mouse

#to use this code, replace FILE with 'C2Q175P1_7a' (or respective file name)

##PARSE TIME & DATE##
#define replace_all function
def replace_all(text, dic): #enter text and dictionary of replacements into function
    for i, j in dic.iteritems(): #for each entry i:I, j:J in dic,
        text = text.replace(i, j) #replace former with latter in text
    return text
#define parse_data function
def parse_data(FILE): #separate time and date, correct header
    f1 = open("" + FILE + ".csv").read() #opens original csv file as string 'f1'
    f2 = open("parsed_ " + FILE + ".csv", "w") #creates new file to write the parsed data to via file object 'f2'
											   #new file will read: parsed_FILE.csv
    reps = {' ':',', '/':'_', 'RealTime':'Date', 'Event':'Realtime'} #dictionary of desired replacements
	    #entry 0: split date and time; replace the space with comma delimiter
	    #entry 1: replace / in date with _
	    #entries 2,3: adjust column headers
    f1parsed = replace_all(f1, reps) #creates string with edited f1 data
    f2.write(f1parsed) #writes parsed data to file stored in f2
    f2.close() #closes file object

##FILTER TEMPERATURE DATA##
#in column 10 (K), if the difference between numerical lines is less than -0.3 or greater than 0.3, remove line
def filter_temp(FILE): #UPDATE SAVED TO RELEVENT VALUE# #remove temperature readings outside threshold deviation
    f2 = open("parsed_ " + FILE + ".csv") #open newly parsed data
    f3 = open("filtered_parsed_ " + FILE + ".csv", "w") #open new file for filtered data
    f3.write("ElapsedTime,Date,Realtime, , ,I1Num,I1RR-I,I1RR-I(SD),I1HR,I1HR(SD),I2T_Mean,I2T_Mean(SD),I3A_TA,I3A_TA(SD)\r\n") #adds corrected header
    saved = 36.23 #whatever first value in row is; update to each next good value
    f2.readline() #skip first line in f2
    for line in f2: #iterate line by line
        fields = line.split(",") #define fields as comma delimited
        if abs(float(fields[10]) - saved) > 0.30: #if the difference from row_n to row_m is > 0.3, mark row_m as outlier and do not extract
            f3.write(fields[0])
            f3.write('\n') #for outlier, write time marker to maintain consistency across files for comparability
        else:
            f3.write(line) #write the lines with accurate data to new file
        saved = float(fields[10]) #update 'saved' value to last non-outlier body temp for each new line
    f2.close() #close file objects
    f3.close()

##CONDITIONAL: EXTRACT ACTIVE/REST DATA##
#active HR:
def activeHR(FILE): #extract lines with activity between 3 and 4 units
    f3 = open("filtered_parsed_ " + FILE + ".csv") #open filtered data
    f3.readline() #skip header in for_loop
    f4 = open("activeHR_ " + FILE + ".csv", "w") #open new file for extracted 'active' data
    f4.write("ElapsedTime,Date,Realtime, , ,I1Num,I1RR-I,I1RR-I(SD),I1HR,I1HR(SD),I2T_Mean,I2T_Mean(SD),I3A_TA,I3A_TA(SD)\r\n") #write in corrected header
    for line in f3:
        fields = line.split(",") #define field delimiter
        if float(fields[12]) >= 3 and float(fields[12]) <= 4:
            f4.write(line) #if activity value in column 12 (M) is between 3 and 4 units, write line to new file
    f3.close() #close file objects
    f4.close()
	
#resting HR: 
def restHR(FILE): #extract lines with activity = 0 after 1 full minute of rest
    f3 = open("filtered_parsed_ " + FILE + ".csv") #open filtered data
    f3.readline() #skip header in for_loop
    f5 = open("restHR_ " + FILE + ".csv", "w") #open new file for extracted 'resting' data
    f5.write("ElapsedTime,Date,Realtime, , ,I1Num,I1RR-I,I1RR-I(SD),I1HR,I1HR(SD),I2T_Mean,I2T_Mean(SD),I3A_TA,I3A_TA(SD)\r\n") #insert header into new file
    counts = 0 #set up counter; set counter to 0
    for line in f3: #iterate line by line
        fields = line.split(",") #define field delimiter as comma
        if float(fields[12]) == 0: 
            counts = counts + 1 #if mouse has no activity, add to counts
        else:
            counts == 0 #if there is activity, reset counter to 0
        if counts > 2 and float(fields[12]) == 0:
            f5.write(line) #if counts is greater than 2, there are at least 3 preceding lines (1 minute) of no activity; write the current line to resting HR document
    f3.close() #close files
    f5.close()

##COMPILE FILTERED DATA FOR EACH MOUSE##
#7a, 8a, 9a, etc. into one file for analysis
