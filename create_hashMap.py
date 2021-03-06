#########################################################################################################
# Author: Timothy Fye
# Title: create_hashMap
# Function: prepare_data_structure(valuesArray)
# Parameters: An array of arrays that typically represent spreadsheet data
#
# Returns: An Object with two data members: 
#   1. A data structure
#   2. An array to reference the dictionary keys (or data in each node the data structure returns)
#
# Purpose: I have a number of projects requiring a variable number of data points to be injected into a hashmap.
#   This document cuts down the amount of code I need to re-write for each project. Essentialy the input data (or parameter)
#   for this function will be an array of arrays. Each sub-array is what will be pushed into each node in the hashMap. 
#   The sub-array's contents are stored in a dictionary format, then that dictionary pushed into the hashMap as the value. 
#   I like to think of each sub-array like a row in a spreadsheet. The entire array would be equivalent to a workbook. 
#   The members within sub-arrays would be the cells in a row. The variable names equal the columns. Since columns, rows,
#   and the amount of cells in each row will vary per project this doc is written in a way that it doesn't care about the size
#   of the project/input array. The column names from the spreadsheet (aka the first array in the array of arrays) becomes the key to the 
#   dictionary references above. The document is dynamic, and will keep pushing cells into a row to a row dictionary until all cells in each
#   rowArray have been pushed. It then keeps pushing all row dictionaries into the hashmap until all rows are pushed into map. 
#
# Description: This function is a black box. It accepts an array of arrays representing spreadsheet data (but
#   any array-of-arrays formatted data works), then loops through each value and pushes it into a newly 
#   instantiated hashmap. The function then returns the hashmap. 
# 
# Note: I don't want to waste time re-naming column variables to match what the values in the title row (aka first row) in the spreadsheet are
#   (in terms of this function the "title row" of the spreadsheet is the first array in the array of array argument provided to function). 
#   I also don't want to waste time manually typing out the 'row_values' keys to exactly match the column titles from spreadsheet/array. As such, 
#   I am simply taking the text stored in my titleRow array elements (or the first array in the valuesArray) and plugging that 
#   directly in as my key to the 'row_values' array. This function can input data from a spreadsheet/array of any size and inject it into a
#   hashmap. No need to worry about any modifications to this file on a per project basis. 
#
# Note: THERE CAN BE NO DUPLICATE TITLES IN THE TITLE ARRAY (AKA FIRST ARRAY IN ARRAY OF ARRAYS) - otherwise the values will be overwritten 
#   on like keys in the value dicationary pushed to hashmap
#
# Instructions: Line 57 is the only line that needs to be updated on a per-project basis. This is where the key is defined. 
#
#########################################################################################################
import hashMap                 # import hasmap library module
import data_structure_package  # import object container class

# This function is responsible for opening csv file, reading data from it, and inserting it into a newly instantiated hashmap. The function returns a hashmap that contains the fee schedule. 
def prepare_data_structure(valuesArray):
 
    # Declare new hashMap to hold the fee schedule
    hash_map = hashMap.hashMap(4000)

    # Grab the first array inside of the valuesArray. The first array should contain the titles of each column. The cell values in each column of the first row will be used 
    # as the 'key' in our 'row_values' dictionary. Essentially whatever is in the first row (or first array in the provided array of arrays) will become the variable names 
    # we will use to reference the values in our value_array dictionary
    titleRow = valuesArray[0] 

    # Loop through each sub-array in the valuesArray (aka each row from a spreadsheet)
    for rowArray in valuesArray: 

        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
        #         THIS IS THE ONLY LINE THAT NEEDS TO BE UPDATED ON PER PROJECT BASIS               #
        # Declare a key to be inserted into hash map (this key is the State + County + City)        #
        key = rowArray[0] + rowArray[1] + rowArray[2]                                               #
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

        # Declare an empty dictionary. The for loop below will walk through each cell in each line, create a key/value pair for that cell (the 'key' is equal to the title of column, while the
        # 'value' is equal to the text in the cell/current rowArray element), then it adds the newly created key/value pair to the row_values{} dictionary. 
        row_values = {}

        # Loop through rowArray so we evaluate each cell and adds to dictionary. This way the program reads any size data from spreadsheet/array into a hashmap without any modification required.
        index = 0 # create index to use in loop below
        for cell in rowArray:
            # Declare values to be inserted into hash map. Store each row as a dictionary. Note: Column title row cells are the key names. This means that to reference the value in the dictionary
            # outside of this function we must know the value of the keys, either by referencing the first array in our array of arrays (realizing that the column names go left to right), or by 
            # explicitly typing in the value in the first column of our spreadsheet when referencing the array. 
            # To Review: We are building a dicitonary that represetns a single row. The first row in the input spreadsheet/array of arrays, containing column title names, are used as the key. 
            # The cell values in the rows are stored in the dictionary from left to right, with the value in the first column first and the value in the last column last.
            # The row_values dictionary will be passed to the hash map with the previously created key as the look up value to obtain the dictionary of row_values back. 
            # That way a call to hashmap for the provided key will return a dictionary of all row items for that row. Instead of a python dictionary a JSON string 
            # could also be created and stored in the hashmap. For refresher on dictionary usage: https://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python/ 
            # Note: All the keys will exactly match what is in the first row of the spreadsheet (aka first array in the provided array of arrays) 
            cell_value = {titleRow[index] : rowArray[index]} # create a new dictioary entry for the cell
            row_values.update(cell_value)                    # push the new dictionary entry into the row_values dictionary
            index = index + 1                                # increment the counter so we move to the next column/cell in the row (this way the program is dynamic and I never have to account for amount of column per project)

        # put data into map 
        hash_map.hashMapPut(key,row_values)

    # Define an object to return to calling function. This object contains two things, the datastructure and also an array of keys to refernces values in the returned dictionary for all nodes. 
    dictionary_keys = titleRow

    # Create a deliverable package to return to user
    ds = data_structure_package.ds_package(hash_map,dictionary_keys)

    # return to main function 
    return ds