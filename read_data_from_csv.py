#########################################################################################################
# Author: Timothy Fye
# Title: read_data_from_csv
# Function: get_csv_data(filepath)
# Parameters: A path to a file (if file is in same directory as source code simply put in name of file)
#
# Purpose: This function allows me to read data from any csv file regardless of column size or row 
#   length. Before this file I had to write a single, all encompassing script to read data from a document straight into 
#   a data structure. This was messy and caused me to have to re-write scripts from stratch for each project. This function 
#   is now a black box. I call it and feed it a path to file. It returns spreadsheet data in a format of an array of arrays. 
#   The returned array can then be passed to any handler function specifically built to push the array into a data structure as  
#   project demands. The referenced handler function will instantiate the proper datastructure and also account for the amount of columns/rows
#   for the project at hand (as the input file will be known to me at that time). This function can be reused for all projects, 
#   aids in keeping duties encapsulated within their own methods, and mitigates the amount of code that has to be modified  
#   everytime I need to start a new project.
#
# Description: This function opens a csv file and returns an array of arrays to the calling function.
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
# NOTE: CSV is comma-deliminated document. This means that if the text within cells have commas in them 
#       then that cell will be read as two different cells in two different columns instead of one cell
#       under one column. Any csv document with commas in the text will essentially return an unreliable array.
#       Commas basically mean "new cell starts here". A doc with 15 columns that has text with no commas will 
#       produce an array of 15 values. A doc with 15 columns, but one cell that has text: Tom Reynold, Sr.
#       will produce 16 columns. This will put any algorithm that processes the returned array off-kilter.  
#       Therefore, before using this function be sure to open a csv, select all, hit ctrl-f, and find/replace 
#       all commas with either nothing or wiht a different delimantor (such as "|"). The other option is to ensure 
#       that the values of all cells are surrounded by parenthesis. In this case commas in the cell text will
#       be okay and not result in unrelabile output. Example: "Tom Reynolds, Sr." should be okay. 
#
# Example Usage (put this in calling function): 
#   import read_data_from_csv
#   spreadsheetArray = read_data_from_csv.get_csv_data("file.csv") # Call function that reads data from provided csv file and returns an array containing arrays of row data
#
#########################################################################################################
import csv # import csv module 

# This function is responsible for opening csv file, reading data from it, and returning an array or arrays that hold all spreadsheet data. 
def get_csv_data(filepath):

    # File name to be opened (must be saved in same directory as .py exe's or full path provided)
    inputFile = filepath

    # Read data from a csv file
    with open(inputFile) as csvInputFile:                  # Open file, set doc alias to csvfile 
        payload = csv.reader(csvInputFile, delimiter=",")  # Payload will contain the tokenized response from csv.reader function. Intuitively enough, delimiter for standard CSV is ",". 
        values = []                                        # Initialize an array that will hold all values in the workbook         
        for rowArray in payload:                           # Each "row" in payload consists of a string that is parsed into an arry, using the delimiter to determine values in each array element. (1st line may be: ['Dog ', 'Cat']. 2nd line may be:['Calvin ', 'Fluffy']. Row[1] = 'Cat') 
            values.append(rowArray)                        # Append the row array of cell values to the values array

    # close file
    csvInputFile.close    

    # return the data array to calling function 
    return values

# Test Code - unccomment lines below & run for testing
# payload = get_csv_data("fees.csv") # use any csv file in the same directory as this program 
# print(payload)