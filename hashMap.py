##########################################################################################################
# Author: Timothy Fye
# Title: hashMap
#
# Overview: A hashmap is a data structure that stores key/value pairs. It leverages indexing to be very 
#   efficient. First the size of the hashmap is provided. A hashmap will then be created with an equal number of 
#   'compartments' as desired size. A hasmap can essentially be conceptualized as an array. A hashmap takes a 
#   provided key, which for example could be a string of text, then runs the key through a hash function. 
#   That hash function converts letters into digits. The digits is then divided by the size of the hashmap and
#   the remainder is found (using the modulus function). Finding the modulus (or remainder) gaurantees that 
#   the result will be somewhere between 0 and the size (as a remainder cannot be greater than the divisor). 
#   The remainder becomes the "comparment" (better visualized as array index/element) where the 
#   key/value node will be stored. There is a chance that two different keys result in the same comparment.   
#   As a result, each "compartment" (or array element) is a linked list. If there are multiple nodes then they
#   are simply chained together. This direct indexing approach allows for extremely efficient operations. 
#   Note on asymptotic runtime complexity: This data structure generally has big-O complexity of O(1). Direct  
#   indexing means there is no traversal, and you go straight to the node you want to evaluate. Granted, if there
#   are alot of "collisions" (aka a ton of nodes share the same "compartment") then the O(n) property of linked 
#   lists will decrease efficency. Good hash map data structures will re-size when they get too full to avoid this. 
#   
# Purpose: I use hashmaps for alot of different project. At the core they are a collection of nodes with two simple variables, 
#   a key variable and a value variable. The primary use-case is to read data in from an excel spreadsheet and store each row 
#   data as a dictionary of values in a node (I could also store columns as nodes if desired). Within the dictionary (which 
#   itself will be stored in a node's 'value' variable), each column name is the key and the value is the cell for each row. 
#   Don't forget dictionary are key-value pair structures themselves. Why not just use dictionaries? They are great for 
#   simple maps, but more complex projects require slightly more complex data structures such as this. 
# 
# Description: Review the methods below to get a better understanding of this library's API. 
#
##########################################################################################################

##########################################################################################################
# Node class: This class is purposed for containing a key/value pair. (The value passed to this data 
# structure can be either a single variable or an array. The node needs to be built with a next pointer, 
# so we can create a singly linked list. If our hash key function yeilds a collision, we can add the node 
# to the same index that is currently in use, but simply make the all nodes in that index a linked list. 
##########################################################################################################
class hashNode:
    # Constructor function to hold & set the class' local variables
    def __init__(self, input_key, input_value):
            self.key = input_key
            self.value = input_value # this can be any type of variable - such as a dictionary, string, int, or array of any of a type.  
            self.nextPtr = None      # next pointer for node, initialzed to null. This may eventually point to another node to make a linked list.

#########################################################################################################
# hashMap class: This class is the container for the entire hashMap "Value Variable" data structure
#########################################################################################################
class hashMap:
    # Constructor to initialize class' local variables 
    def __init__(self, input_capacity):
        self.table = [None] * input_capacity  # table/array that will contain the hashNodes, initialize the array with desired elements
        self.size = 0                         # define the size of the hashMap
        self.capacity = input_capacity        # define the capacity of the hashMap

    # Hash function # 1
    # - Convert a key string to an integer value, where we can then divide that by capacity 
    # and place our node into the appropraite index. Retrieval will put the key through this 
    # same function. This means the hash map data structure will operate in constant time O(1)
    # during retreivals
    def hashFunction1(self, key):
        numeralKeyValue = 0                      # declare a variable and intialize to zero 
        for char in key:                         # loop through each character in the provided key string 
            numeralConvertion = ord(char)        # convert the numeral value to it's numeric representation using ord function
            numeralKeyValue += numeralConvertion # keep adding each value to our numeral index so we have a single value that will determine our index
        return numeralKeyValue                   # return the aggregated numeral value for handling by calling function

    # Hash function # 2
    # - This function can be used in lieu of hashFunction1 (only use one of the two for any instantiated hash map, otherwise the retrievals wont work) 
    # - This option has a more complicated hash function index, in theory this function will have less collisions than option number # 1        
    def hashFunction2(self, key):
        numeralKeyValue = 0                      # declare a variable and intialize to zero 
        for char in key:                         # loop through each character in the provided key string 
            numeralConvertion = ord(char)        # convert the numeral value to it's numeric representation using ord function
            # keep adding each value to our numeral index so we have a single value that will determine our index. This time, 
            # we take the numeral value of the character and multiply it by the numeral value of the character plus one. This way 
            # we can have a more unique final value.
            numeralKeyValue += numeralConvertion * (numeralConvertion + 1) 
        return numeralKeyValue                   # return the aggregated numeral value for handling by calling function

    # Hash Map Put Function
    # - Enter (or update) a key/value pair   
    def hashMapPut(self, key, value):

        # check to see if we need to resize 
        usage = self.size/self.capacity  # calculate the % of index slots used 

        # resize the data structure if used slots exceed 70% of total data structure
        if(usage > 0.70):
            self.hashMapResize() #re-set the 'self' attribute to equal the newly returned hash map

        # find the targeted index where we should drop the new Node
        # - use the mudulo operator to find the remainder of dividing the resuls of the hash function 
        # and the capacity of the hash map's table/array. We use mudulos operator to guarantee that 
        # the index will not exceed capacity, as we will be bounded in capacity. 
        index = self.hashFunction1(key) % self.capacity 

        # create a variable that will serve as a pointer to the current node in the index (if there is one)
        nodePtr = self.table[index]

        # if there is no link currently in the index, we can just create a new node. The node constructor 
        # will automatically initialize the list to point to null for us
        if(nodePtr == None):
            # since there is no "new" or "malloc" operator in python, dynamic memory operates differently.   
            new = hashNode(key,value)  # Create a new linkedListNode object and pass the parameters through to the linkedListNode constructor.
            self.table[index] = new      # Place the new object into my table at the empty index 
        # else there is a link currently in the index, and we need to
        # 1) check to see if the current key/value node is already in there while performing step two (if so, we aren't going to re-add it)
        # 2) traverse the nodePtr all the way to the end of the list
        # 3) join it to existing nodes so we have a linked list
        else:
            # create a variable (treated as a bool), that will be marked true if we find the key exists below. 
            keyFoundBool = 0

            # while loop will itereate the linked list that is in the particular index (visualization below)
            # Table Index:    Contents of Index:
            # _______________ _____________
            # [             ] * -> * -> * 
            # [current index] * -> *         <----- we are traversing this list in index "current index"
            # [             ] None
            while(nodePtr.nextPtr != None): # while the linked list's current pointer's next pointer is not null, keep iterating
                # if the currentPtr's key (this is typically a 'string') is not equal to the key we are passing in, then the does not node exist already.         
                if(nodePtr.key != key):
                    # iterate our currentPtr to the currentPtr's next nextPtr so we traverse to the next linked list Node
                    nodePtr = nodePtr.nextPtr
                # Else the keys match and we found an existing value. Update the value instead of creating a new node.   
                else:
                    # set the bool variable to true, we found the key
                    keyFoundBool = 1
                    # update the found key's value to the new value
                    nodePtr.value = value
                    # iterate our currentPtr to the currentPtr's next nextPtr so we traverse to the next linkedListNode
                    nodePtr = nodePtr.nextPtr
            
            # if the keyBoolFound is false (or 0), we need to add our Node to the end of the linked list
            if(keyFoundBool == 0):
                # since there is no "new" or "malloc" operator in python, dynamic memory operates differently.   
                new = hashNode(key,value)  # Create a new linkedListNode object and pass the parameters through to the linkedListNode constructor.
                nodePtr.nextPtr = new     # Set the currentPtr's nextPtr node (now at end of the list) to 'point to' (or contain) the new node.

        # finally, update the hash map's size since we added a node 
        self.size = self.size + 1

    # Hash Map Get Function:   
    # - return a value from a key/value pair     
    def hashMapGet(self, key):
        # find the targeted index where we should drop the new Node
        # - use the mudulo operator to find the remainder of dividing the resuls of the hash function 
        # and the capacity of the hash map's table/array. We use mudulos operator to guarantee that 
        # the index will not exceed capacity, as we will be bounded in capacity. 
        index = self.hashFunction1(key) % self.capacity 

        # create a variable that will serve as a pointer to the current node in the index (if there is one)
        nodePtr = self.table[index]

        # while loop will itereate the linked list that is in the particular index (visualization below)
        # Table Index:    Contents of Index:
        # _______________ _____________
        # [             ] * -> * -> * 
        # [current index] * -> *         <----- we are traversing this list in index "current index"
        # [             ] None
        while(nodePtr != None): # while the linked list's current pointer is not null, keep iterating
            # if the currentPtr's key (this is typically a 'string') is not equal to the key we are passing in, then the does not node exist already.         
            if(nodePtr.key != key):
                # iterate our currentPtr to the currentPtr's next nextPtr so we traverse to the next linked list Node
                nodePtr = nodePtr.nextPtr
            # Else the keys match and we found an existing value. Return the node's value  
            else:
                # return the value in current node
                return nodePtr.value 
        
        # if we made it here, then we can return zero 
        return 0

    # Hash Map Contains Function:   
    # - return a bool to show if a key/value pair is in the hash map    
    def hashMapContains(self, key):
        # find the targeted index where we should drop the new Node
        # - use the mudulo operator to find the remainder of dividing the resuls of the hash function 
        # and the capacity of the hash map's table/array. We use mudulos operator to guarantee that 
        # the index will not exceed capacity, as we will be bounded in capacity. 
        index = self.hashFunction1(key) % self.capacity 

        # create a variable that will serve as a pointer to the current node in the index (if there is one)
        nodePtr = self.table[index]

        # while loop will itereate the linked list that is in the particular index (visualization below)
        # Table Index:    Contents of Index:
        # _______________ _____________
        # [             ] * -> * -> * 
        # [current index] * -> *         <----- we are traversing this list in index "current index"
        # [             ] None
        while(nodePtr != None): # while the linked list's current pointer is not null, keep iterating
            # if the currentPtr's key (this is typically a 'string') is not equal to the key we are passing in, then the does not node exist already.         
            if(nodePtr.key != key):
                # iterate our currentPtr to the currentPtr's next nextPtr so we traverse to the next linked list Node
                nodePtr = nodePtr.nextPtr
            # Else the keys match and we found an existing value. Return the node's value  
            else:
                # return true
                return 1 
        # if we made it here, then we can return false
        return 0

    # Resize Table Function:   
    # - resize the hash table. Otherwise it will get too full and we will have
    # too many collisions. Collisions equal long linked lists per index, which 
    # results in a longer retreival time than O(1).     
    def hashMapResize(self):
        # prepare an empty array 
        tempArray = []

        # copy all data contained in self.hashMap into our array
        for index in self.table:                                  # go through the whole array/table in current hash map
            nodePtr = index                                       # create a variable called nodePtr and set it to the node containted in the current index 
            while(nodePtr != None):                               # traverse through the linked list that is in this index  
                tempArray.append([nodePtr.key, nodePtr.value])    # append key/value pair sub-array in array                      
                nodePtr = nodePtr.nextPtr                         # iterate to end of linked list 
 
        # re-initialize our dataStructure in preparation for re-build
        self.table = [None] * (self.capacity * 2)  # double-sized table/array that will contain the hashNodes, initialize the array with desired elements 
        self.size = 0                              # set size back to zero        
        self.capacity = (self.capacity * 2)        # double our capacity

        # now pass all data back into the newly sized & initialized data structure
        for subarray_entry in tempArray:
            self.hashMapPut(subarray_entry[0],subarray_entry[1]) # reference the sub array, send the saved key/value back to data structure using hasMapPut

    # Print Map Function: Must be handled in calling script since we do not know what type of value was past in. 
    # Remove function could be added here 



# Test Code - uncomment lines below & run for testing 
#Map = hashMap(4000) # Instantiate new hashmap 
#orderOne = { "customer" : "John Smith", "product" : "samsung phone" , "tracking number" : "389175", "order date" : "10/18/2018", "cost" : 650 }   # Declare dictionary
#orderTwo = { "customer" : "Tony Gonzales", "product" : "apple iphone" , "tracking number" : "21456", "order date" : "10/17/2018", "cost" : 1650 } # Declare dictionary
#orderThree = { "customer" : "Jimmy Johnson", "product" : "flip phone" , "tracking number" : "11125", "order date" : "10/1/2018", "cost" : 1 }     # Declare dictionary
#Map.hashMapPut("order_one",orderOne)     # Put record in map
#Map.hashMapPut("order_two",orderTwo)     # Put record in map
#Map.hashMapPut("order_three",orderThree) # Put record in map
#value = Map.hashMapGet("order_two")      # Test retrieving a value  
#print(value)                             # Print value               