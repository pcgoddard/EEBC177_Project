# Final_Project

#Background
  This code is designed to analyze a  large collection of data from the Chris Colwell Circadian Rhythm Lab in the UCLA Psychiatry and Behavioral Science department. The data of interest contain physiological information on Huntington's Diseased mice gathered over several weeks of radio telemetry recording. The data I am interested in are activity levels, body temperature and heart rate. Three cohorts of mice were analyzed: Huntingtin gene homozygous, heterozygous and healthy wild type as a control.
  
#Data Setup
  The data were recorded by the machine into excel binary files in 20-second intervals (ie. each row is 20 seconds apart) for the full test period, and the machine automatically switched excel files approximately every 24 hours, but the transition meant that some data were not recorded. The machine recorded the date and live time (eg 9:42am) in one field instead of separate ones, and made some erroneous body temperature readings. My code reorganizes the data a little, filters out the poor temperature data, and then extracts all the data when the mouse is at rest or within a  particular activity range.
  For simplicity, I used a single 24-hour sample file of data to develop a code to parse and isolate data of interest. The .xlsb file has multiple sheets, each containing all the data for one of the 7 mice recorded. I exported each sheet to its own .csv file manually and created a code to analyze these csv files.

* raw data file: C2Q175P1_7x.csv
    - where 'x' is one of: a,b,c,e,f,g,h

#Code Instructions
##Parse Date and Time
* Define the replace_all function
    - sets up "replace_all" to read a dictionary of elements and their replacements
    - each entry should be: 'element_in_text:replacement'
* Using parse_data function:
    - enter 'C2Q175P1_7x' in place of FILE to parse a specific file
    - function reads through the raw data and writes the parsed data to a new file called "parsed_C2Q175P1_7x.csv"
    - in the dictionary 'reps': 
        - first entry ['  ' : ' , '] splits time and date into two fields by replacing the space with a comma delimiter
        - the following entries clean up the time and date columns by adjusting the headers and makignthe date more readable in a .csv file.
* When the function is complete, you will receive the following message:

'Parsed data has been extraced to new file.'

##Filter Temperature
* Some temperature readings, column K, showed a 10 degree change in 20 seconds, which is not plausible. I using graphical analysis, I determined that the temperature cannot reasonable change more than about 0.3 degrees C in 20 seconds
* The filter_temp function extracts data with valid temperature readings based on this threshold value
    - it inserts the revised header into a new document
    - if a line's temperature reading differs from the previous by more than 0.3, the elapsed time, date, and realtime data are recorded in the new document, and the rest of the line is written in blank
    - if the temperature change is valid, all the data in the line are copied over
* Using the function:
    - make sure the parsed data file is in your directory
    - enter 'C2Q175P1_7x' in place of FILE
    - open the function and replace 'saved = 36.23' with 'saved = first_value_in_x's_temp_column'
        - this forces the analyst to double check that the first reading is plausible for the given cohort
        - 'saved' value updates with each iteration to the last valid temperature
* Resulting file:
    - file name: filtered_parsed_C2Q175P1_7x.csv
    - looks like: the data appears the same except that in lines with false temperature data, only the time and date fields appear
    - these blank lines maintain consistent 20-second intervals across all files
* When the function is complete, you will receive the following message:

'Data with filtered body temp has been extraced to new file.'

##Extracting Active Data
* Sometimes it is useful to look at the heart rate and temperature data for times that the mice were active (within a controlled range)
* Activity data in column M (index 12)
* Selected range: 3 to 4 units
    - activity measure is arbitrary on scale of 1- ~300
    - to change range, replace 3 and 4 in code
* Using the function
    - make sure the filtered data file is in your directory
    - enter 'C2Q175P1_7x' in place of FILE
    - code scanning for number values in column 12
        - if activity value is between 3 and 4, inclusive, the data line is extracted
        - if activity value is numerical and not on the interval, the date and time data are copied with a blank line
        - if activity is blank from temperature filtering,  function ignores the error and treats it like a non-interval numerical value
* Resulting file:
    - file name: activeHR_C2Q175P1_7x.csv
    - date and times for each line
    - blank data when activity is not in desired range
    - full line when activity is in desired range
* When the function is complete, you will receive the following message:

'Active telemetry data has been extracted.'

##Extracting Rest Data
* Similar to the active data function
* Instead of activity range, function extracts rest data:
    - activity is zero
    - *and* following at least a full minute (3 rows) of zero activity
    - this accounts for the "cool down period" in which the heart slows down after activity before we measure the rest data
* Using the function:
    - make sure the filtered data file is in your directory
    - enter 'C2Q175P1_7x' in place of FILE
    - lines with 0 activity following at least 3 preceding lines of 0 activity are copied to the new file
    - like the activeHR function, all other lines are marked with the date and time data and a blank line
* Resulting file:
    - file name: activeHR_C2Q175P1_7x.csv
    - date and times for each line
    - blank data when activity is above 0
    - full line when mouse is resting (ie. activity is at 0)
* When the function is complete, you will receive the following message:

'Resting telemetry data has been extracted.'

#Potential
* Resulting files for each mouse:
    - parsed_C2Q175P1_7x.csv
    - filtered_parsed_C2Q175P1_7x.csv
    - activeHR_C2Q175P1_7x.csv
    - restHR_C2Q175P1_7x.csv
* Can easily compile desirec combinations of data
    - eg: by genotype (homozygous, heterozygous, wildtype)
    - eg: by data type (activity, temperature, heart rate, etc.)
    - eg: average data for 2 hour bins instead of 2 second bins
* Statistical analysis
    - *I may continue to work towards these steps for my own work, but I currently do not have the statistical or programming background, or proficient enough understanding of the data's nuances to group or analyze the data further.*
