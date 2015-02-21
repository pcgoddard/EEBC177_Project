#parse out time and date
	#format: mm/dd/yyyy\s\hh:mm:ss
	#split at space

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