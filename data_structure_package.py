##########################################################################################################
# Author: Timothy Fye
# Title: hashMap
#
# Summary: This class is simply a class to return an object that has two things: 
#   1. An instantiated and filled data scructure
#   2. An array that holds dictionary keys. Each data structure's nodes holds one varaible, which stores a dictionary. 
#       This dictionary holds all data for that node. In order to reference the values in that dictionary this array provides 
#       a list of keys. Using the key will retrieve the desired value. 
#
# This class will be used by 'create_linkedList.py' and 'create_hashMap.py' documents. They will create a datastructure, 
#   fill it up with data, store the dictioary keys in an array, instantiate/drop it in this class, then return the packet
#   to the calling function for use. 
#
# Examples: 
#   To use data structure methods: ds_package.datastructure.method() # See datastructure specification file for available methods
#
#   To retreive all key values: ds_package.datastructure.keys_dictionary
#
#   They may be used as such after package has been created/returned:
#        
#       # below gets a node from a linkedlist    
#       node = ds_package.data_structure.getNext()        
#       # below uses the 'title' of the fifth column in a spreadsheet (arrays are zero-indexed) to get the value of the cell in the node (aka row) for that column (aka key).   
#       cell = node.data[ds_package.dictionary_keys[4]]  
#       print(cell)
#
##########################################################################################################

##########################################################################################################
# Node class: This class is purposed for containing a key/value pair. (The value passed to this data 
# structure can be either a single variable or an array. The node needs to be built with a next pointer, 
# so we can create a singly linked list. If our hash key function yeilds a collision, we can add the node 
# to the same index that is currently in use, but simply make the all nodes in that index a linked list. 
##########################################################################################################
class ds_package:
    # Constructor function to hold & set the class' local variables
    def __init__(self, data_structure, keys_dictionary):
            self.data_structure = data_structure     # this will hold a fully created data structure
            self.keys_dictionary = keys_dictionary   # this will hold an array of keys 