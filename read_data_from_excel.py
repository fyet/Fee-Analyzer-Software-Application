#########################################################################################################
# Author: Timothy Fye
# Title: read_data_from_excel
# Function: get_excel_data(filepath)
# Parameters: A path to a file (if file is in same directory as source code simply put in name of file)
#
# Purpose: This function allows me to read data from any excel file regardless of column size or row 
#   length. Before this file I had to write a single, all encompassing script to read data from a document straight into 
#   a data structure. This was messy and caused me to have to re-write scripts from stratch for each project. This function 
#   is now a black box. I call it and feed it a path to file. It returns spreadsheet data in a format of an array of arrays. 
#   The returned array can then be passed to any handler function specifically built to push the array into a data structure as  
#   project demands. The referenced handler function will instantiate the proper datastructure and also account for the amount of columns/rows
#   for the project at hand (as the input file will be known to me at that time). This function can be reused for all projects, 
#   aids in keeping duties encapsulated within their own methods, and mitigates the amount of code that has to be modified  
#   everytime I need to start a new project.
#
# Description: This function opens an excel file and returns an array of arrays to the calling function.
#   The array of arrays is in the syntax below. Notice that the cell values of each row are contained in each 
#   sub-array. Anotherwards, the outer array contains arrays of rows, which contains cell values from the left most 
#   column to the right most column. Example for visualization: 
#
#       [ 
#           [(row 1, column 1), (row 1, column 2), (row 1, column 3),...(row 1, column n)],  
#           [(row 2, column 1), (row 2, column 2), (row 2, column 3),...(row 2, column n)],
#           ............................................................                  ,
#           [(row n, column 1), (row n, column 2), (row n, column 3),...(row n, column n)]
#       ]    
# 
# References: https://stackoverflow.com/questions/22169325/read-excel-file-in-python 
#
# NOTE: 'xlrd' module may need to be installed for this function to work. See instructions in line below.
#
# Example Usage (put this in calling function): :
#   import read_data_from_excel 
#   spreadsheetArray = read_data_from_excel.get_excel_data("fees.xlsx") # Call function that reads data from provided excel file and returns an array containing arrays of row data
#
#########################################################################################################
import xlrd # import excel read module ---> [ *** Note: You may need to open the command line in the directory you are running this executable and install excel module with command 'pip install xlrd' *** ]

# This function is responsible for opening excel file, reading data from it, and returning an array or arrays that hold all spreadsheet data. 
def get_excel_data(filepath):

    # File name to be opened (must be saved in same directory as .py exe's or full path provided)
    inputFile = filepath

    # Read data from an excel file
    wb = xlrd.open_workbook(inputFile)                        # Open the file in question
    for s in wb.sheets():                                     # For all sheets that exist in the workbook 
        values = []                                           # Initialize an array that will hold all values in the workbook   
        for row in range(s.nrows):                            # For each row on the current sheet in workbook
            col_value = []                                    # Initialize an array that will hold all column values for specified row 
            for col in range(s.ncols):                        # For each column that is in the current row 
                value  = (s.cell(row,col).value)              # Find the value of the cell, the col reference will increment each loop 
                try : value = str(int(value))                 # See if we can cast the value to an in within a string 
                except : pass                                 # Include exception 
                col_value.append(value)                       # Append the cell value to the column value array 
            values.append(col_value)                          # Append the column value array 

    # return the data array to calling function 
    return values

# Test Code - unccomment lines below & run for testing
# payload = get_excel_data("orderList.xlsx") # use any csv file in the same directory as this program 
# print(payload)