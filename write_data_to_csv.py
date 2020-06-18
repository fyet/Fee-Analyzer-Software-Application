#########################################################################################################
# Author: Timothy Fye
# Title: write_data_to_csv
# Function: push_csv_data(filepath, payload)
# Parameters: 
#   - A path to a file (if file is in same directory as source code simply put in name of file) 
#     - *** filepath must include extentions .csv - Example: "output.csv" or "../dir/output.csv" NOT "output" or "..dir/output" ***
#   - An array of arrays containing spreadsheet data 
#
# Purpose: This function allows me to write data to a csv file regardless of column size or row 
#   length. This function is a black box. I call it and feed it a file name in addition to an array of arrays. 
#   The method takes the array of arrays, creates/opens a new file with the name provided, and feeds the array
#   data into the file. This function can be reused for all projects, aids in keeping duties encapsulated within 
#   their own methods, and mitigates the amount of code that has to be modified everytime I need to start a new project.
#
# Description: This function creates/opens a csv file and writes data contained into the spreadsheet from parameter
#   consisting of an array of arrays. The input array of arrays needs to be in the syntax below. Notice that the 
#   cell values of each row are contained in each sub-array. Anotherwards, the outer array contains arrays of rows,
#   which contains cell values from the left most column to the right most column. Example for visualization: 
#
#       [ 
#           [(row 1, column 1), (row 1, column 2), (row 1, column 3),...(row 1, column n)],  
#           [(row 2, column 1), (row 2, column 2), (row 2, column 3),...(row 2, column n)],
#           ............................................................                  ,
#           [(row n, column 1), (row n, column 2), (row n, column 3),...(row n, column n)]
#       ]    
#
# NOTE: CSV is comma-deliminated document. This means that if the strings within sub-arrays have commas in them 
#       then that string will be written as two different cells in two different columns instead of one cell
#       under one column. Commas basically mean "new cell starts here". This may cause the spreadsheet to not 
#       have like-columns aligned. Ensure the input array's sub-array contents are surrounded by parenthesis to 
#       avoid this. Example: "Tom Reynolds, Sr." should be okay.  
#
# NOTE: Currently I have built this to accept an array of array payload. It may be beneifical to update this program to 
#       accept JSON input instead as this is more standardized than defining specific array syntax. Or perhaps 
#       update program to include a parameter flag to indiciate the type of payload being passed in so it can handle
#       both.
#########################################################################################################
import csv # import csv module 

# This function is responsible for creating/opening csv file, writing data to it, and closing the file. Note: "filepath" must include extention .csv
def push_csv_data(filepath, payload):

    # Check to ensure extention is included 
    if (filepath.find('.csv') == -1):
        print("Error: file parameter must have .csv extention. Example 'output.csv' ")
        return 

    # Set varible to file name w/ extention    
    outputFile = filepath

    # CSV: create a file, set flag to w so we can write
    with open(outputFile,"w") as csvOutputFile:

        # Write data from array into spreadsheet    
        for row in payload:                      # For each sub-array (aka row) in payload array
            for cell in row:                     # For each cell in that row array 
                csvOutputFile.write(str(cell))   # Cast value in cell to string and then write it to file 
                csvOutputFile.write(",")         # As this is csv file, write a comma so we move to next column and prepare to write to next cell during next pass
            csvOutputFile.write("\n")            # After each row write a new line before we loop to the next line 

    #close file
    csvOutputFile.close    

# Test Code - uncomment lines below & run for testing
# spreadsheet = [ ["r1-c1","r1-c2","r1-c3"], ["r2-c1","r2-c2","r2-c3"], ["r3-c1","r3-c2","r3-c3"] ]
# push_csv_data("output.csv",spreadsheet) 