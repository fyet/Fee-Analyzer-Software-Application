#########################################################################################################
# Author: Timothy Fye
# Title: File to read data in from CSV document
# All rights reserved
#########################################################################################################
import read_data_from_excel # import get_orders
import read_data_from_csv   # import get_orders
import create_hashMap
import create_linkedList
import compute_custom_algorithm
import write_data_to_excel
# Shouldnt need these, have separate functions/files that will import these
# import doublyLinkedList # import data structure executable
# import hashMap # import hasmap module

def main():

    # Fee Schedule Prep
    spreadsheetArray = read_data_from_excel.get_excel_data("productFeesByState.xlsx")   # Call function that reads data from provided excel file and returns an array containing arrays of row data
    hash_map_package = create_hashMap.prepare_data_structure(spreadsheetArray)          # Call a function that accepts an array of arrays, inserts it into a hashmap, then returns an object with the data structure and a dictionarykey array

    # Order Data Prep
    spreadsheetArray = read_data_from_excel.get_excel_data("orderList.xlsx") # Call function that reads data from provided excel file and returns an array containing arrays of row data
    linked_list_package = create_linkedList.prepare_data_structure(spreadsheetArray)    # Call a function that accepts an array of arrays, inserts it into a linkedlist, then returns an object with the data structure and a dictionarykey array

    # Compute Algorithm
    payload = compute_custom_algorithm.run(hash_map_package,linked_list_package)

    # Write Computed Data in Array Payload to Output File
    write_data_to_excel.push_excel_data("output_file_increases.xls", payload[0])

    # Write Computed Data in Array Payload to Output File
    write_data_to_excel.push_excel_data("output_file_rushes.xls", payload[1])

if __name__ == '__main__':
    main()
