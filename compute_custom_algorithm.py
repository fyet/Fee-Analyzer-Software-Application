#########################################################################################################
# Author: Timothy Fye
# Title: compute_custom_algorithm
#
# Description: The contents of 'compute_custom_algorithm' will be re-written per project. This is the file that
#   runs algorithm on data. Since the data/column structure of the input file is known this file can access
#   that data through datastructures accordingly, make computations/additions/deletions on file as necessary, 
#   then constuct an array of arrays that can be passed back to main (which can be then passed to write_data_to_excel.py or
#   writ_)
#
# Instead of passing back an array of arrays this funcition acutallly passes back two array of arrays with in another 
#   array. I want two reports generated from this single run. Typically it would just pass back an array of arrays
# 
#########################################################################################################

# Helper function called by run(). It defines a title row.
def _initializeTitleRowValuesSpeadsheetOne(spreadsheetArray):
    # Define an array of column titles to be injected as the first array (aka row) in our spreasheetArray
    columnTitles = [ "Reference ID #",
                     "City",
                     "State",
                     "County",
                     "Zip",
                     "Product Type",
                     "Completed Date",
                     "Rush",
                     "Site Size",
                     "GLA",
                     "Appraised Value",
                     "Original Client Fee",
                     "Increase Amount",
                     "New Client Fee",
                     "Increase %",
                     "Complexity Reasons",
                     "Comments" ]

    spreadsheetArray.append(columnTitles)
    return spreadsheetArray

# Helper function called by run(). It defines a title row.
def _initializeTitleRowValuesSpeadsheetTwo(spreadsheetArray):
    # Define an array of column titles to be injected as the first array (aka row) in our spreasheetArray
    columnTitles = [ "Reference ID #",
                     "City",
                     "State",
                     "County",
                     "Zip" ]

    spreadsheetArray.append(columnTitles)
    return spreadsheetArray

# Helper function called by run(). It finds a valid key for current node and returns it.
def _buildKey(node,hash_map_package,linked_list_package):
    # construct a key to input to hashmap function that is comprised of the data elements in the linked list node of state, county, and city
    # it is good to note, the create_hashMap.py file is concatenating state + county + city, but the latter two may be blank since not all
    # counties & cities have special fees in the fee schedule (open the productFeesByState.csv file for more details). Most fees are just state-level fees.
    # We need to check to see if the key we built is in the hashmap before we try to get the product list of fees for that territory
    # first build a key from the linked list node's data variable's state, county, and city (using dictionary column index)
    key = node[linked_list_package.keys_dictionary[4]] + node[linked_list_package.keys_dictionary[6]] + node[linked_list_package.keys_dictionary[3]]
    result = hash_map_package.data_structure.hashMapContains(key)        # check to see if the key is in the hashmap with the hashMapContains() function
    if(result == 0):                                                     # if the function returned zero then the key was not found
        key = node[linked_list_package.keys_dictionary[4]] + node[linked_list_package.keys_dictionary[6]] # next, build a key from the linked list node's data variable's state and county
        result = hash_map_package.data_structure.hashMapContains(key)    # check to see if the key is in the hashmap with the hashMapContains() function
        if(result == 0):                                                 # if the function returned zero then the key was not found
            key = node[linked_list_package.keys_dictionary[4]]      # next, build a key from the linked list node's data variable's state variable
            result = hash_map_package.data_structure.hashMapContains(key)# check to see if the key is in the hashmap with the hashMapContains() function
            if(result == 0):                                             # if the function returned zero then the key was not found
                print("Error: key '", key,"' was not found in hash map. Exiting program.") # print error
                exit()                                                   # stop execution and kill program. We can't proceed until input is fixed to include key
    # If we reach this line then a valid key was found, return it to calling run()
    return key

# Helper function called by run(). It receives a node's site size, gla, and value and then calculates the step/tier. The function returns a "1" for "Tier 1", "2" for "Tier 2", "3" for "Tier 4", or "Q" for "Quote".
def _calculateTier(siteSize,gla,appraisedValue):

    # Start out by cleaning data. Some columns may be "N/A", which means that we can't perform mathmatical operations on them. We will push in objects into dictionary
    #   if they are not equal to 'N/A'. We will clean up the data before pushing as well, which means removing things like "ac" or "sq. ft" from "site size" and converting
    #   siteSize to ac if given in sq ft.
    availablePropertyCriteria = {} # create an empty dictionary

    # 1. Evaluate siteSize, see if it exists for this node (aka - value is not "N/A" or empty), convert to sq. ft if necessary, then clean so it is only integers. Push to dictionary if it exists
    if(siteSize.find("N/A") == -1 and siteSize != "" and siteSize != None): # Find substring instead of trying to find exact match (there may be hanging spaces or newline characters that would mess up comparison otherwise)
        if(siteSize.find("s") == -1 and siteSize.find("S") == -1): # Find substring to verify that the value is in acrage and not sq. ft.
            # Now we need to strip everything after the space in data. We know input file sends info in as '1234 sf' or '3143 sq. ft'
            index = siteSize.find(" ")             # Find index where the space exists
            numString = siteSize[:0 + index]       # Store the substring of numbers, which is all the data to the left of the space. Note: This may include a comma
            numString = numString.replace(",", "") # Remove any commas from string as we will not be able to convert from string to float with commas included.
            value = float(numString)               # Cast string to float data type
            dict_entry = { "site_size" : value }   # Create a dictionary entry
            availablePropertyCriteria.update(dict_entry) # Push entry to dictionary for later evaluation
        else: # The value is in square feet
            # Now we need to strip everything after the space in data. We know input file sends info in as '1234 ac' or '3143 acerage'
            index = siteSize.find(" ")             # Find index where the space exists
            numString = siteSize[:0 + index]       # Store the substring of numbers, which is all the data to the left of the space. Note: This may include a comma
            numString = numString.replace(",", "") # Remove any commas from string as we will not be able to convert from string to float with commas included.
            value = float(numString)               # Cast string to float data type
            value = value / 43560                  # Convert to acreage
            dict_entry = { "site_size" : value }   # Create a dictionary entry
            availablePropertyCriteria.update(dict_entry) # Push entry to dictionary for later evaluation
    else: # Push a value of zero for site_size since it doesnt exist. This will enable us to perform mathmatical operations in the section below.
        dict_entry = { "site_size" : 0 }             # Create a dictionary entry
        availablePropertyCriteria.update(dict_entry) # Push entry to dictionary for later evaluation

    # 2. Evaluate GLA, see if it exists for this node (aka - value is not "N/A" or empty). Data should already be sq ft as this data point is pulled into the input spreasheet from a database that stores uniform appraisal xml data
    if(gla.find("N/A") == -1 and gla != "" and gla != None): # Find substring instead of trying to find exact match (there may be hanging spaces or newline characters that would mess up comparison otherwise)
        numString = gla.replace(",", "")                # Remove any commas from string as we will not be able to convert from string to float with commas included.
        value = int(numString)                          # Cast string to int data type
        dict_entry = { "gla" : value }                  # Create a dictionary entry
        availablePropertyCriteria.update(dict_entry)    # Push entry to dictionary for later evaluation
    else: # Push a value of zero for gla since it doesnt exist. This will enable us to perform mathmatical operations in the section below.
        dict_entry = { "gla" : 0 }               # Create a dictionary entry
        availablePropertyCriteria.update(dict_entry) # Push entry to dictionary for later evaluation

    # 3. Evaluate Appraised Value, see if it exists for this node (aka - value is not "N/A" or empty). Data should already be okay as this data point is pulled into the input spreasheet from a database that stores uniform appraisal xml data
    if(appraisedValue.find("N/A") == -1 and appraisedValue != "" and appraisedValue != None): # Find substring instead of trying to find exact match (there may be hanging spaces or newline characters that would mess up comparison otherwise)
        numString = appraisedValue.replace(",", "")     # Remove any commas from string as we will not be able to convert from string to float with commas included.
        value = int(numString)                          # Cast string to int data type
        dict_entry = { "appraised_value" : value }      # Create a dictionary entry
        availablePropertyCriteria.update(dict_entry)    # Push entry to dictionary for later evaluation
    else: # Push a value of zero for appraised_value since it doesnt exist. This will enable us to perform mathmatical operations in the section below.
        dict_entry = { "appraised_value" : 0 }       # Create a dictionary entry
        availablePropertyCriteria.update(dict_entry) # Push entry to dictionary for later evaluation

    # Determine what the tier should be (hardwiring dummy figures & criterion, actual threshold criterion & values would be defined by a company to match proprietary complexity structure depending on property factors)
    if((availablePropertyCriteria["site_size"] > 8) or (availablePropertyCriteria["gla"] > 4999) or (availablePropertyCriteria["appraised_value"] > 4005000)):
        return "Q" # Return Q; if this block fires then the property is considered "Quote
    elif((availablePropertyCriteria["site_size"] > 3.9) or (availablePropertyCriteria["gla"] > 2999) or (availablePropertyCriteria["appraised_value"] > 2005000)):
        return 3 # Return 3; If this block fires then the property falls within our fee schedule's "Tier 3" range
    elif((availablePropertyCriteria["site_size"] > 1.9) or (availablePropertyCriteria["gla"] > 1999) or (availablePropertyCriteria["appraised_value"] > 1005000)):
        return 2 # Return 2; If this block fires then the property falls within our fee schedule's "Tier 2" range
    else:
        return 1 # Return 1; If this block fires then the property falls within our fee schedule's "Tier 1" range

# Helper function called by run(). It returns complexity details array.
def _textMineComplexityNotesforincreases(notes):
    # Define an empty array that will hold complexity reasons
    complexityDetails = []

    # Check to see if the text 'rural' or 'remote' exists in notes. If so, push value to complexityReasons array
    if(notes.find("rural") != -1 or notes.find("remote") != -1):
        complexityDetails.append("rural/remote")
    # Check to see if the text 'waterfront', 'riverfront', 'oceanfront' exists in AE notes. If so, push value to complexityReasons array
    if(notes.find("waterfront") != -1 or notes.find("riverfront") != -1 or notes.find("oceanfront") != -1 or
       notes.find("water front") != -1 or notes.find("river front") != -1 or notes.find("ocean front") != -1 ):
        complexityDetails.append("waterfront")
    # Check to see if the text 'solar' exists in notes. If so, push value to complexityReasons array
    if(notes.find("solar") != -1):
        complexityDetails.append("solar energy home")
    # Check to see if the text 'golf' exists in notes. If so, push value to complexityReasons array
    if(notes.find("golf") != -1):
        complexityDetails.append("golf course")
    # Check to see if the text 'gated' exists in notes. If so, push value to complexityReasons array
    if(notes.find("gated") != -1):
        complexityDetails.append("gated community")
    # Check to see if the text 'condotel' exists in notes. If so, push value to complexityReasons array
    if(notes.find("condotel") != -1):
        complexityDetails.append("condotel")
    # Check to see if the text 'mixed use' exists in notes. If so, push value to complexityReasons array
    if(notes.find("mixed use") != -1):
        complexityDetails.append("mixed use")

    return complexityDetails

# Helper function called by run(). It returns quote if a quote factor was tripped. Returns 0 if none and 1 if some.  
def _textMineComplexityNotesforquotefactors(notes):
    # Define a variable we will return to calling function
    quoteFactors = 0

    # Check to see if the text 'rural' or 'remote' exists in notes. If so, push value to complexityReasons array
    if(notes.find("outbuildings") != -1 or notes.find("mountain") != -1):
        quoteFactors = 1

    return quoteFactors    

# Helper function called by run(). It calculates the fee of the assignment per fee list, factoring in and adding the appropriate complexities
def _calculateFee(baseFee, tier, rush, complexityDetailsArray):

    # Ensure the baseFee is note quote ('Quote' can be passed in from 'productFeesByState.xlsx' in certain states). If it is, return 'Q'
    if(baseFee.find("Quote") != -1):
        return 'Q'

    # Define an empty array that will hold complexity reasons
    fee = int(baseFee)

    # Add the tier add-on cost if appropriate
    if(tier == 2):
        fee = fee + 300 # Dummy Add-on fee for tier 2 
    # Add the tier add-on cost if appropriate
    if(tier == 3):
        fee = fee + 400 # Dummy Add-on fee for tier 3 
    # Return 'Q' if quote, we cannot calculate the fee if the property was within quote criteria
    if(tier == "Q"):
        return 'Q'

    # Add the rush fee to the fee if a rush was requested
    if(rush.find("Yes") != -1):
        fee = fee + 150

    # Note: Thoertically say company defines all possible additions for each addon in the complexityDetailsArray to be $105 add
    #   This means we can just find the length of complexityDetailsArray, multiply it by $105 since each one would be $105 add,
    #   then add that number to our base fee
    addon = len(complexityDetailsArray) * 105 # find addon for remaining complexity possibilities
    fee = fee + addon                         # addon the final amount

    return fee                                # return commensurate fee back to calling function


def run(hash_map_package, linked_list_package):

    # We will want to return an array of arrays that represents a spreadsheet. The outerarray is equal to the worksheet, while the inner arrays represent each row in the worksheet. The inner array elements represents
    # the cell value for the row from the left-most column to the right most column. This is the format we need to be able to use functions such as 'write_data_to_excel.py' and 'write_data_to_csv.py'
    # The first array in the array represents the first row, which conventionally should be column titles/headers.
    spreadsheetArrayOne = []                                                           # create an empty array
    spreadsheetArrayOne = _initializeTitleRowValuesSpeadsheetOne(spreadsheetArrayOne)  # calls a helper function that will initialize column titles to my desired output, returns the array with a new-sub array containing these column headers

    spreadsheetArrayTwo = []                                                           # create an empty array
    spreadsheetArrayTwo = _initializeTitleRowValuesSpeadsheetTwo(spreadsheetArrayTwo)  # calls a helper function that will initialize column titles to my desired output, returns the array with a new-sub array containing these column headers

    # Initialize node variable as we prepare to step through linkedList
    node = linked_list_package.data_structure.getNext() # This obtains the first node, whose data values are just the title columns of spreadsheet we read into program. Don't perform any operations on the first node.
    counter = 0                                         # Initialize a counter

    # Keep iterating until we reached the end of the list (linked lists's getNext() function returns 'None' - aka 'Null')
    while(node != None):

        # The first node contains column titles since data was read in from spreadsheet. Don't perform any operations on first row, only subsiquent rows.
        if(counter != 0):
            # Call a helper function that will find the proper key for the node in question & return it
            key = _buildKey(node, hash_map_package, linked_list_package)

            # at this point we have found a valid key. The next step is to return the product price dictionary for the key in question.
            productPriceList = hash_map_package.data_structure.hashMapGet(key)

            # the productPriceList now holds the returned value from the key/value pair in the hashmap. This is a dictionary of prices. We can use the
            # linkedList's node's data varaible's job_type variable as an index. The product list dictionary's keys are job types and values are base fees.
            # using the job type as the index will return the base fee. We are basically just doing this: productPriceList["Condo Appraisal (FNMA 1073)"],
            # but allowing ourselves to find the applicable product to the linked list node in question by feeding in its job type (or job type of order).
            # Get the base fee for the job type of the current node. Below is equivalent to saying:
            #   baseFee = productPriceList[node["Job Type"]]) or more simply:  baseFee = productPriceList["1004"] - can't hardcode form in though since it is different per node
            baseFee = productPriceList[node[linked_list_package.keys_dictionary[15]]]

            # Next, save the Site Size (aka acreage), GLA, and Appraised Value in local variable
            # Below is looking at node returned by the linked list (or current node). This node has a 'data' variable that holds a dictionary. The 'value' we want from the dictionary
            #   is site size, GLA, and appraised value. In order to access this we need to enter they 'key' as the array index. We don't need to hardcode the key, we have the keys_dictionary
            #   that is a part of our linked list package. This is the name of the columns from our input spreadhseet. Opening the spreadsheet I can see the columns I am looking for are 12,
            #   13, and 14 (with the rightmost column being '0' as arrays are zero indexed). The dictionary value holds the exact title of the column, which I can use as my index value to get
            #   the key value residing in my node's data dictionary.
            siteSize = node[linked_list_package.keys_dictionary[12]]
            gla = node[linked_list_package.keys_dictionary[13]]
            appraisedValue = node[linked_list_package.keys_dictionary[14]]
            tier = _calculateTier(siteSize,gla,appraisedValue) # Call a helper function that calculates the tier for the property. Function returns 1,2,3, or Q (for 'quote')

            # Next, we will leverage text mining to parse notes for the order/node in question and capture key words. The key words
            #   will help us identify non-rush, non gla, value, lot size complexity adds. An array of reasons will be returned by the
            #   function below
            notes = node[linked_list_package.keys_dictionary[19]] # Grab the "Notes" column from input spreadsheet
            complexityDetails = _textMineComplexityNotesforincreases(notes)

            # Grab the "Rush" column from input spreadsheet
            rush = node[linked_list_package.keys_dictionary[11]]

            # Calculate the commensurate price by passing in the tier varaible (which evaulatued lot size, gla, appraised value), the complexity details (which is a list of all other
            #   complexity possbilities), and the base fee (which will be used as a starting point)
            commensurateFee = _calculateFee(baseFee, tier, rush, complexityDetails)

            # Mark orders that are elible to be passed along to TIAA (all orders that have a fee of 'Q' or where Xsite Fee > commensurateFee)
            # Calculate the difference between the fee charged and the fee that should have been reflected per the fee schedule
            # Calculate the percentage change between the fee charged and the fee that should have been reflected per the fee schedule
            overExpectedCharge = ""
            increaseAmount = ""
            increasePercentage = ""
            xSiteFee = int(node[linked_list_package.keys_dictionary[16]]) # get xsite fee and cast it to an int
            if(commensurateFee == "Q"):
                increaseAmount = "N/A"
                increasePercentage = "N/A"
                overExpectedCharge = "X"
                commensurateFee = "Quote" # This will output 'Quote' to file instead of 'Q', make things more clear for readers
            elif(xSiteFee > commensurateFee):
                increaseAmount = int(node[linked_list_package.keys_dictionary[16]]) - commensurateFee # Find difference between Xsite fee and the fee we should have charged per fee schedule
                increasePercentage = increaseAmount / commensurateFee
                overExpectedCharge = "X"
                # Check to see if we should actually be setting things to quote 
                if(_textMineComplexityNotesforquotefactors(notes) == 1): # we found something that should push this to quote    
                    increaseAmount = "N/A"
                    increasePercentage = "N/A"
                    overExpectedCharge = "X"
                    commensurateFee = "Quote" # This will output 'Quote' to file instead of 'Q', make things more clear for readers                    

            # Prepare a string version of complexityDetails array so when it is written to excel it has commas 
            complexityDetailsString = ""      # Declare a variable
            length = len(complexityDetails)   # Find length of complexityDetails array
            index = 1                         # Declare an index 
            for reason in complexityDetails:  # Loop through each element in array                    
                if(length != (index)):        # Check to make sure we aren't on the last element
                    complexityDetailsString = complexityDetailsString + reason # contactenate the string
                    complexityDetailsString = complexityDetailsString + ", "  # concatenate a comma since we aren't on last element
                else:                         # We are on last element
                    complexityDetailsString = complexityDetailsString + reason # contactenate the string, but don't add a comma
                index = index + 1 # increment the index

            # Only print out the orders where the xSiteFee > commensurateFee
            if(overExpectedCharge == "X" and commensurateFee != "Quote"): # Could use (overExpectedCharge == "X" or overExpectedCharge == "Q") if you wanted both quote orders and overcharges
                # Add the row data we would to eventually like to write to a new spreadsheet for this iteration after evaluating this node's data and making additional computations/evaluations
                # on it. 
                # Note: 'node[linked_list_package.keys_dictionary[n]' is taking the data in the node's data variable (the values from the dictionary) and storing it in the new array. Basically
                # I am going to write out most of the same data that was initially read in. I will add a few new columns/pieces of data, which adds to
                # the original report and is the purpose of this whole exercise (evaluating current data and building a new report with some like
                # data and some new data)
                rowArray = [ node[linked_list_package.keys_dictionary[0]], # Ref Number
                            node[linked_list_package.keys_dictionary[3]], # City 
                            node[linked_list_package.keys_dictionary[4]], # State
                            node[linked_list_package.keys_dictionary[6]], # County 
                            node[linked_list_package.keys_dictionary[5]], # Zip
                            node[linked_list_package.keys_dictionary[15]],# Job Type                      
                            node[linked_list_package.keys_dictionary[8]], # First Completed
                            node[linked_list_package.keys_dictionary[11]],# Rush 
                            node[linked_list_package.keys_dictionary[12]],# Site Size
                            node[linked_list_package.keys_dictionary[13]],# GLA
                            node[linked_list_package.keys_dictionary[14]],# Appraised Value 
                            commensurateFee, # Add what the fee should be
                            increaseAmount, # Difference between Xsite Fee and what fee should have been per schedule
                            node[linked_list_package.keys_dictionary[16]], # Xsite Fee
                            increasePercentage, # Percent change (always positive)
                            complexityDetailsString, # Print out the complexity details
                            node[linked_list_package.keys_dictionary[19]] # Notes
                        ]

                # Append the new row to the spreadsheetArray
                spreadsheetArrayOne.append(rowArray)

            # Only print out the order if it is a rush
            if(node[linked_list_package.keys_dictionary[11]].find("Yes") != -1):
                # Add the row data we would to eventually like to write to a new spreadsheet for this iteration after evaluating this node's data and making additional computations/evaluations
                # on it. 
                # Note: 'node[linked_list_package.keys_dictionary[n]' is taking the data in the node's data variable (the values from the dictionary) and storing it in the new array. Basically
                # I am going to write out most of the same data that was initially read in.
                rowArray = [ node[linked_list_package.keys_dictionary[0]], # Ref Number
                            node[linked_list_package.keys_dictionary[3]], # City 
                            node[linked_list_package.keys_dictionary[4]], # State
                            node[linked_list_package.keys_dictionary[6]], # County 
                            node[linked_list_package.keys_dictionary[5]], # Zip
                        ]

                # Append the new row to the spreadsheetArray
                spreadsheetArrayTwo.append(rowArray)

        node = linked_list_package.data_structure.getNext() # Iterate to the next node
        counter = counter + 1                               # Increment the counter by one

    # combine spreadsheetArrayOne & spreadsheetArrayTwo into the same payload
    payload = []                        # Initialize empty payload array
    payload.append(spreadsheetArrayOne) # Append spreadsheet one to payload array
    payload.append(spreadsheetArrayTwo) # Append spreadsheet two to payload array 
    return payload                      # Return payload