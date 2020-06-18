#########################################################################################################
# Author: Timothy Fye
# Title: write_data_to_excel
# Function: push_excel_data(filepath, payload)
# Parameters: 
#   - A path to a file (if file is in same directory as source code simply put in name of file) 
#     - *** filepath must include extentions .xls - Example: "output.xls" or "../dir/output.xls" NOT "output" or "..dir/output" ***
#   - An array of arrays containing spreadsheet data 
#
# Purpose: This function allows me to write data to an excel file regardless of column size or row 
#   length. This function is a black box. I call it and feed it a file name in addition to an array of arrays. 
#   The method takes the array of arrays, creates/opens a new file with the name provided, and feeds the array
#   data into the file. This function can be reused for all projects, aids in keeping duties encapsulated within 
#   their own methods, and mitigates the amount of code that has to be modified everytime I need to start a new project.
#
# Description: This function creates/opens an excel file and writes data contained into the spreadsheet from parameter
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
# References: https://www.programering.com/a/MTMyQDNwATU.html (styling and adding formulas is possible)
#
# NOTE: 'xlwt' module may need to be installed for this function to work. See instructions in line below.
#   - There are a few different modules to write different excel types - https://stackoverflow.com/questions/16560289/using-python-write-an-excel-file-with-columns-copied-from-another-excel-file
#
# NOTE: Currently I have built this to accept an array of array payload. It may be beneifical to update this program to 
#       accept JSON input instead as this is more standardized than defining specific array syntax. Or perhaps 
#       update program to include a parameter flag to indiciate the type of payload being passed in so it can handle
#       both.
#########################################################################################################
import xlwt # import excel read module ---> [ *** Note: You may need to open the command line in the directory you are running this executable and install excel module with command 'pip install xlwt' *** ]

# This function is responsible for creating/opening excel file, writing data to it, and closing the file. Note: "filepath" must include extention .xls
def push_excel_data(filepath, payload):

    # Check to ensure appropraite extention is included (only .xls is supported by 'xlwt' module - need to use 'xlsxwriter' or 'openpyxl' modules for .xlsx)
    if ( filepath.find('.xlsx') != -1 or filepath.find('.xls') == -1):
        print("Error: file parameter must have .xls extention. Example 'output.xls' ")
        return 

    # Set varible to file name w/ extention    
    outputFile = filepath

    # XLS: create a file for writing 
    workbook = xlwt.Workbook(encoding = 'ascii')   # Create a new workbook
    worksheet = workbook.add_sheet('Sheet 1')      # Add a sheet to the workbook
    
    # Write data from array into spreadsheet
    rowIndex = 0                                            # Initialize row index to zero, this will be incremented as we step through sub-arrays in outer array
    for row in payload:                                     # For each row in the payload array (aka outer array)...               
        columnIndex = 0                                     # Initialize a column index to zero, this will be incremented as we step through current sub-array (aka current row)                    
        for cell in row:                                    # For each item in the row array (aka cell)...
            worksheet.write(rowIndex, columnIndex, cell)    # Write data relative the appropriate row and column index
            columnIndex += 1                                # Increment the column index so we move to next column and prepare to write to next cell during next pass
        rowIndex += 1                                       # Increment the row index so we move to next line as we prepare to write next row

    # Save file for persistence of changes
    workbook.save(outputFile)

# Test Code - unccomment lines below & run for testing
# spreadsheet = [ ["r1-c1","r1-c2","r1-c3"], ["r2-c1","r2-c2","r2-c3"], ["r3-c1","r3-c2","r3-c3"] ]
# push_excel_data("output.xls",spreadsheet) 