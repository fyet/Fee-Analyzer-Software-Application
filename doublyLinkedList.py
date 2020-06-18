#########################################################################################################
# Author: Timothy Fye
# Title: doublyLinkedList
#
# Overview: A linkedlist is a data structure that "chains" together "nodes". Each node is essentially a custom
#   data type, or a container that holds data elements/variable that are pertinent to a specific node. An example would
#   be a linkedlist of orders for a company. Each node represents one order. Each order might have data elements that
#   pertain only to that order (i.e. customer, product, tracking number, order date, etc.). Each node has a dedicated variable
#   that "points" to the next node in the sequence. A "doubly linked list" means each node has a dedicated variable that points
#   to the previous node as well. This way an algorithm can step through all nodes (or in this case orders) by moving node to node
#   by returning a pointer to the next or previous node in the sequence. Note: the data elements of a node can be accessed through this
#   pointer by the calling function. This data structure has a handful of methods, defined below, that allows someone interacting with
#   the datastructure to add a new node to the chain, move forward and backward along the chain while returning the 'current node',
#   amongst other operations. Read comments below to better understand the class' API. Note on asymptotic runtime complexity: This
#   data structure has a big-O complexity of O(n) as it has to traverse through the entire list in the worst case. The linked list will
#   have a handful of 'get' methods that will return one thing: the data varible of the node rather than the entire node itself (the user
#   has no need to access pointer variables, they should only care about getting the data they pushed into the list back out). Passing an
#   entire node back would be very bad practice, as the datastructure is supposed to handle all the details of pointer variables and interacting
#   with the linkedListNode class. All the user cares about is getting whatever they stored in the data variable back out exactly how they
#   put it in.
#
# Purpose: I used linkedLists for alot of different projects. The primary use-case is to read data in from
#   an excel spreadsheet and store each row as a node in the linked list (I could also store columns as nodes if desired). One
#   challange I faced is that each spreadsheet for each project is different. Sometimes there is 10 columns and 5000 rows, while
#   othertimes there are 100,000 rows and 100 columns. Explicitly defining a node's variables in the node below means that the datastructure
#   had to be re-written for each and every project. This was very cumbersome. To enable this datastructure to be flexible, each
#   node only contains one single variable. The variable can be whatever the user of the datastructure library would like. It can hold an array,
#   list, dictionary, string, int, etc. This means that I never have to re-write this data structure library. I only have to pass in what I would
#   like it to contain.
#
# Description: Returning to my spreadsheet use-case example above, I prefer to create a dictionary. It may look like this:
#       - nodeVariableDictionary = { "customer" : "John Smith", "product" : ,"samsung phone" : ,"tracking number" : "389175", "order date" : "10/18/2018", "cost" : 650 }
#   Note that within the dictionary, each column name is the key and the value is the cell for each row. Don't forget dictionary are key-value pair structures themselves.
#   Now I can use the "push" function to create a node that will store this dictionary. As I loop through the linkedList, I can access the variable that stores
#   the dictionary in a node, and then evaluate the dictionary's contents as needed outside of this library. If I only need to store one string variable in my node then
#   I can simply store a single string variable in the node's data variable. The bottom line is that the user of this library can define contents.
#
#########################################################################################################

##########################################################################################################
# linkedListNode class: This class is purposed for containing a single data variable. The variable can
#   be a complex object containing further variables, such as a list/dictionary/or array. Alternatively the
#   variable can be more simplistic and only hold a single data value (such as a string, int, or float). It is
#   up to the user what they want a single node to hold in the linked list datastructure.
##########################################################################################################
class linkedListNode:
    # Constructor function to hold & set the class' local variables
    def __init__(self, data):
            self.data = data           # data variable to hold whatever the user would like to store in the node
            self.nextPtr = None        # next pointer for linkedListNode, initialzed to null. This will eventually point to another linkedListNode to make a linked list.
            self.previousPtr = None    # previous pointer for linkedListNode, initialized to null. This will eventually point to another linkedListNode to make a linked list.

########################################################################################################
# doublyLinkedList class: This class is the container for the entire linked list data structure
########################################################################################################
class doublyLinkedList:
    # -> Constructor to initialize class' local variables
    def __init__(self):
        self.frontPtr = None          # front pointer for traversal/handling of list (always points to the first node in the list)
        self.backPtr = None           # back pointer for traversal/handling of list (always points to the last node in the list)
        self.currentListPtr = None    # current pointer for traversal/handling of list (points to the current node in the list)

        # Below variable is so the getNext() function works the first time after initally calling push() to fill structure with data. The getNext() iterates self.currentListPtr to the next node,
        # THEN it returns the data of the next node. The self.currentListPtr pointer stays associated to the node it just returned. If self.currentListPtr points to the first node
        # (aka self.frontPtr) when a list is created/initialized/filled with data then it will move to the second node, return it's data, and skip the first! For various logical reasons,
        # cheifly related to ensuring popCurrent() function will remove the node that was just returned to user when they last called getNext(), it is important the self.currentListPtr
        # does not advance prematurely so when the user calls popCurrent() self.currentListPtr is still pointing to the node they just returned. Basically having getNext() store current node
        # in tempnode, advance to next node, then return tempnode would mean popCurrent() would delete the new self.currentListPtr. Since there is both getNext() and getPrevious() in this
        # doubly linked list, we cannot go back one or forward one node in popCurrent() because we dont know which direction the user "came from". Therefore getNext() must iterate to next
        # node in chain, then return. However. The first call to getNext() remains problematic due to the challange of potentially skipping the first node. The plan is to have a
        # 'frontSetinel', which is just a pointer that will point to self.frontPtr but not be an official part of the link. It is just a one-way pointer that self.currentListPtr will start on
        # so that when getNext() is intially called it can iterate to the true first node, set it as current, and return its data. Visualization:
        #
        #  This is how the list will be formatted, notice frontSetinel is a node rather than a var, and the true front pointer does not point back to it. It is a one way street so that currentListPtr
        #  can advance. currentListPtr will not be static of course, it will point to different nodes depending on what functions are a called and in what order. Example with three nodes below for visualization:
        #
        #     None <- [node] -> <- [node] -> <- [node] -> None
        #             ^    ^                      ^
        #  [frontSetinel] frontPtr              backPtr
        #     ^
        #   currentListPtr
        self.frontSetinel = linkedListNode(None) # Note: as it is logical the current pointer should start at the front of the queue, we don't need one for getPrevious(). This will simply return null if the user
                                                 # tries to call it right after they initialize the linked list.

    # -> push Function:
    # - Add an item to the back of the linked list
    def push(self, data):
        # check to see if the linked list is empty. If front is equal to "None", then there are no items in the list and we need to
        # build a new item
        if(self.frontPtr == None):
            # since there is no "new" or "malloc" operator in python, dynamic memory operates differently. Create a new linkedListNode object and pass the
            # parameters through to the linkedListNode constructor.
            new = linkedListNode(data)
            self.frontPtr = new  # set the front pointer to the newly created linkedListNode and point to the first (& only) linkedListNode
            self.backPtr = new   # set the back pointer to the newly created linkedListNode, and point to the last (& only) linkedListNode
            self.frontSetinel.nextPtr = self.frontPtr # set the nextPtr attribute of the "hidden" node that points one-way to the first node in the list. The true front node's previousPtr will never be set to it as it is not part of the linked list.
            self.currentListPtr = self.frontSetinel # set the list's pointer to point to the "hidden" node that points one-way. It is not a part of the linked list, just a starting point so getNext() works and popCurrent() is possible. See above for full description.
        # there is a linkedListNode in the linked list. We need to add a new linkedListNode to the back of the list by referencing the back pointer
        else:
            # since there is no "new" or "malloc" operator in python, dynamic memory operates differently. Create a new linkedListNode object and pass the
            # parameters through to the linkedListNode constructor.
            new = linkedListNode(data)
            new.previousPtr = self.backPtr # new.nextPtr is already set to "None" per constructor, new.previousPtr needs to be set to the current back linkedListNode
            self.backPtr.nextPtr = new     # the current back linkedListNode's next pointer needs to be set to point to the new linkedListNode
            self.backPtr = new             # set back pointer to "point" to the new linkedListNode as it is the new back pointer

    # -> popFront Function:
    # - Remove the front-most node and re-adjust the pointers in the chain accordingly
    def popFront(self):
        # check to see if the linked list is empty. If front pointer is equal to "None", then there are no items in the list to remove. Otherwise...
        if(self.frontPtr != None):
            if(self.getLength() > 1): # If we have more than one node in the linked list...
                if(self.currentListPtr != self.frontPtr and self.currentListPtr != self.frontSetinel): # Make sure self.currentListPtr is not pointing to the front node or the front setinenl 
                    currentPtr = self.frontPtr            # Set a temporary variable equal to the first node in the list
                    self.frontPtr = self.frontPtr.nextPtr # Make the self.frontPtr equal to the self.frontPtr.nextPtr
                    self.frontPtr.previousPtr = None      # Set the new front pointer's previous pointer to None
                    currentPtr.nextPtr = None             # Disconnect the node from chain entirely
                    del currentPtr                        # explicity delete the separated node in the list (memory management is more necessary in C languages than Python, but still good practice so there are no hanging vars) 
                else: # In this circumstance the front pointer should be equal to current list pointer (and we need to reset the current pointer to point to the new front - otherwise we can't iterate and are pointed to the removed node)
                    currentPtr = self.frontPtr            # Set a temporary variable equal to the first node in the list
                    self.frontPtr = self.frontPtr.nextPtr # Make the self.frontPtr equal to the self.frontPtr.nextPtr
                    self.frontPtr.previousPtr = None      # Set the new front pointer's previous pointer to None
                    currentPtr.nextPtr = None             # Disconnect the node from chain entirely
                    del currentPtr                        # explicity delete the separated node in the list (memory management is more necessary in C languages than Python, but still good practice so there are no hanging vars) 
                    self.currentListPtr = self.frontPtr   # point the current list pointer that was previously pointing to the removed front node and set it equal to the new front node
            else: # There is only one node, we may delete
                currentPtr = self.frontPtr # Set a temporary variable equal to the first/only node in the list
                del currentPtr             # delete the first node in the list
                self.frontPtr = None       # set the list's pointer to None/Null. We only had one node in list, popping it means there is nothing in list and no list pointers can be pointing to node
                self.backPtr = None        # set the list's pointer to None/Null. We only had one, popping it means there is nothing in list and no list pointers can be pointing to node
                self.currentListPtr = None # set the list's pointer to None/Null. We only had one, popping it means there is nothing in list and no list pointers can be pointing to node    


    # -> popBack Function:
    # - Remove the back-most node and re-adjust the pointers in the chain accordingly
    def popBack(self):
        # check to see if the linked list is empty. If back pointer is equal to "None", then there are no items in the list to remove. Otherwise...
        if(self.backPtr != None):
            if(self.getLength() > 1): # If we have more than one node in the linked list...
                if(self.currentListPtr != self.backPtr):    # Make sure self.currentListPtr is not pointing to the back node
                    currentPtr = self.backPtr               # Set a temporary variable equal to the last node in the list
                    self.backPtr = self.backPtr.previousPtr # Make the self.backPtr equal to the self.backPtr.previousPtr (or the second to last node in the list)
                    self.backPtr.nextPtr = None             # Set the new back pointer's next pointer to None
                    currentPtr.previousPtr = None           # Disconnect the node from chain entirely
                    del currentPtr                          # explicity delete the separated node in the list (memory management is more necessary in C languages than Python, but still good practice so there are no hanging vars)
                else: # In this circumstance the back pointer should be equal to current list pointer (and we need to reset the current pointer to point to the new back - otherwise we can't iterate and are pointed to the removed node)
                    currentPtr = self.backPtr               # Set a temporary variable equal to the last node in the list
                    self.backPtr = self.backPtr.previousPtr # Make the self.backPtr equal to the self.backPtr.previousPtr (or the second to last node in the list)
                    self.backPtr.nextPtr = None             # Set the new back pointer's next pointer to None
                    currentPtr.previousPtr = None           # Disconnect the node from chain entirely
                    del currentPtr                          # explicity delete the separated node in the list (memory management is more necessary in C languages than Python, but still good practice so there are no hanging vars)
                    self.currentListPtr = self.backPtr   # point the current list pointer that was previously pointing to the removed front node and set it equal to the new front node
            else: # There is only one node, we may delete
                currentPtr = self.backPtr  # Set a temporary variable equal to the last/only node in the list
                del currentPtr             # delete the first node in the list
                self.frontPtr = None       # set the list's pointer to None/Null. We only had one node in list, popping it means there is nothing in list and no list pointers can be pointing to node
                self.backPtr = None        # set the list's pointer to None/Null. We only had one, popping it means there is nothing in list and no list pointers can be pointing to node
                self.currentListPtr = None # set the list's pointer to None/Null. We only had one, popping it means there is nothing in list and no list pointers can be pointing to node

    # -> popCurrent Function:
    # - Remove the current node and re-adjust the pointers in the chain accordingly
    def popCurrent(self):
        # check to see if the linked list is empty. If back pointer and front pointers are equal to "None", then there are no items in the list to remove. Otherwise...
        if(self.frontPtr != None and self.backPtr != None):
            if(self.getLength() > 1): # If we have more than one node in the linked list...
                # check to see if the self.currentListPtr happens to be equal to the first node
                if(self.currentListPtr == self.frontPtr):
                    self.popFront() # simply call the popFront() function as it will handle this case
                # check to see if the self.currentListPtr happens to be equal to the last node
                elif(self.currentListPtr == self.backPtr):
                    self.popBack() # simply call the popFront() function as it will handle this case
                else: # the currentNode happens to be somewhere in the middle of the linked list
                    currentPtr = self.currentListPtr # set a temporary variable to the self.currentListPtr
                    # "Remove" the link in the chain
                    currentPtr.previousPtr.nextPtr = currentPtr.nextPtr # this points the nextPtr of currentPtr's previous node to what currentPtr's nextPtr is pointing to
                    currentPtr.nextPtr.previousPtr = currentPtr.previousPtr # this points the previousPtr of currentPtr's next node to what currentPtr's previousPtr is pointing to
                    self.currentListPtr = self.currentListPtr.nextPtr # make sure the self.currentListPtr is set to the next node as the current one will be deleted
                    currentPtr.previousPtr = None # disconnect currentPtr's previousPtr from the linked list
                    currentPtr.nextPtr = None # disconnect currentPtr's nextPtr from the linked list
                    del currentPtr             # delete the first node in the list
            else: # There is only one node, we may delete
                currentPtr = self.backPtr  # Set a temporary variable equal to the last/only node in the list
                del currentPtr             # delete the first node in the list
                self.frontPtr = None       # set the list's pointer to None/Null. We only had one node in list, popping it means there is nothing in list and no list pointers can be pointing to node
                self.backPtr = None        # set the list's pointer to None/Null. We only had one, popping it means there is nothing in list and no list pointers can be pointing to node
                self.currentListPtr = None # set the list's pointer to None/Null. We only had one, popping it means there is nothing in list and no list pointers can be pointing to node

    # -> getNext Function:
    # Return the next pointer in list (if calling this function in loop then loop until returned pointer is equal to "None" - the back of queue is not connected to front)
    # Note: Once user loops all the way through the self.currentListPtr will point to null, user can use getFront(), or getBack() to reset pointer to valid node as desired.
    # They can also call getPrevious() and go in reverse order.
    def getNext(self):
        if(self.currentListPtr != self.backPtr): # In the case the self.currentListPtr is not pointing to the very last node in the list
            self.currentListPtr = self.currentListPtr.nextPtr # iterate the list's pointer variable to point to the next item in the list. We know there is one because currentPtr != None.
            return self.currentListPtr.data # return the node we just iterated to
        else: # If self.currentListPtr is pointing to the very last node in the list then there is no next, return None/Null
            return None

    # -> getPrevious Function:
    # Return the previous pointer in list (if calling this function in loop then loop until returned pointer is equal to "None" - the front of queue is not connected to back)
    # Note: Once user loops all the way through the self.currentListPtr will point to null, user can use getFront(), or getBack() to reset pointer to valid node as desired.
    # They can also call getNext() and go in reverse order.
    def getPrevious(self):
        if(self.currentListPtr != self.frontPtr): # In the case the self.currentListPtr is not pointing to the very last node in the list
            self.currentListPtr = self.currentListPtr.previousPtr # iterate the list's pointer variable to point to the next item in the list. We know there is one because currentPtr != None.
            return self.currentListPtr.data # return the node we just iterated to
        else: # If self.currentListPtr is pointing to the very last node in the list then there is no next, return None/Null
            return None

    # -> getFront Function:
    # Return the front pointer in list (** NOTE: LOGICALLY ENOUGH, THIS RESETS THE CURRENT POINTER TO POINT TO FRONT **)
    def getFront(self):
        self.currentListPtr = self.frontPtr # Reset the list's current pointer variable to equal the pointer at the front of the list
        currentPtr = self.currentListPtr # have our function's local pointer variable point to the node that is the list's current pointer varible
        return currentPtr.data

    # -> getBack Function:
    # Return the front pointer in list (** NOTE: LOGICALLY ENOUGH, THIS RESETS THE CURRENT POINTER TO POINT TO BACK **)
    def getBack(self):
        self.currentListPtr = self.backPtr # Reset the list's current pointer variable to equal the pointer at the back of the list
        currentPtr = self.currentListPtr # have our function's local pointer variable point to the node that is the list's current pointer varible
        return currentPtr.data

    # -> getLength Function:
    # Traverse the list to count how many nodes exist, then return the total nodes to calling function
    def getLength(self):
        currentPtr = self.frontPtr         # set the linked list's current pointer to linked list's front pointer
        counter = 0                        # set the counter to zero
        while(currentPtr != None):         # while the linked list's current pointer's next pointer is not null, keep iterating
            # increment our counter by one
            counter = counter + 1
            # iterate our currentPtr to the currentPtr's next nextPtr so we traverse to the next linkedListNode
            currentPtr = currentPtr.nextPtr
        return counter

    # -> printList Function:
    # Traverse the list & print
    def printList(self):
        currentPtr = self.frontPtr         # set the linked list's current pointer to linked list's front pointer
        while(currentPtr != None):         # while the linked list's current pointer's next pointer is not null, keep iterating
            # print all of the linkedListNode's member variables
            print(currentPtr.data)

            # iterate our currentPtr to the currentPtr's next nextPtr so we traverse to the next linkedListNode
            currentPtr = currentPtr.nextPtr

## Test Code - uncomment lines below & run for testing (to iterate through list you can use getNext() or getPrevious() until it returns null OR use getLength() and loop through an equal number while calling getNext() or getPrevious())
# List = doublyLinkedList() # Instantiate a new list
# orderOne = { "customer" : "John Smith", "product" : "samsung phone" , "tracking number" : "389175", "order date" : "10/18/2018", "cost" : 650 }   # Declare dictionary
# orderTwo = { "customer" : "Tony Gonzales", "product" : "apple iphone" , "tracking number" : "21456", "order date" : "10/17/2018", "cost" : 1650 } # Declare dictionary
# orderThree = { "customer" : "Jimmy Johnson", "product" : "flip phone" , "tracking number" : "11125", "order date" : "10/1/2018", "cost" : 1 }     # Declare dictionary
# print("Pushing 3 items to list")       # Console log message
# List.push(orderOne)                    # Push entry to list
# List.push(orderTwo)                    # Push entry to list
# List.push(orderThree)                  # Push entry to list
# List.printList()                       # Test print
# length = List.getLength()              # Return the size
# print("List Length: ",length)          # Print the number of nodes
# print("Popping front node from list")  # Console log message
# List.popFront()                        # Pop the first node
# print("Printing Next Node after deleting front:")
# node = List.getNext()                   # Get next node in list
# print(node)
# print("Printing Next Node after Next Node after deleting front:")
# node = List.getNext()                   # Get next node in list
# print(node)                                    # Test print 
# print("Printing Entire List")
# List.printList()                       # Test print
# length = List.getLength()              # Return the size
# print("List Length: ",length)          # Print the number of nodes
# print("Popping back node from list")   # Console log message
# List.popBack()                         # Pop the first node
# List.printList()                       # Test print
# length = List.getLength()              # Return the size
# print("List Length: ",length)          # Print the number of nodes
# print("Popping back node from list")   # Console log message
# List.popBack()                         # Pop the first node
# List.printList()                       # Test print
# length = List.getLength()              # Return the size
# print("List Length: ",length)          # Print the number of nodes
# print("Pushing 3 items to list")       # Console log message
# List.push(orderOne)                    # Push entry to list
# List.push(orderTwo)                    # Push entry to list
# List.push(orderThree)                  # Push entry to list
# List.printList()                       # Test print
# length = List.getLength()              # Return the size
# print("List Length: ",length)          # Print the number of nodes
# node = ""                              # intialize node
# print("Looping through list with getNext() and printing response")
# while(node != None):
#     node = List.getNext()   # Test get next
#     if(node != None):
#         print(node)
# print("Reverse Looping through list with getPrevious() and printing response")
# node = ""                              # re-intialize node
# while(node != None):
#     node = List.getPrevious()   # Test get next
#     if(node != None):
#         print(node)
# print("try out getBack()")
# node = List.getBack()   # Test get back
# print(node)
# print("try out getFront()")
# node = List.getFront()   # Test get back
# print(node)
# print("moving to second node with getNext()")
# node = List.getNext()
# print(node)
# print("now deleting the middle node with popCurrent()")
# List.popCurrent()
# List.printList()                       # Test print
# length = List.getLength()              # Return the size
# print("pushing one more item to list")
# List.push(orderThree)                  # Push entry to list
# print("List Length: ",length)          # Print the number of nodes
# print("try out getBack()")
# node = List.getBack()   # Test get back
# print(node)
# print("Popping back node from list")   # Console log message
# List.popBack()                         # Pop the first node
# node = List.getPrevious()   # Test get next
# print(node)