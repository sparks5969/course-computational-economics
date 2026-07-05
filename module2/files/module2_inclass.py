"""
Module 2. in-class coding practice
"""

# section 1. import packages
import json
import copy

# section 2. import the datasets
with open('project2_data.json') as f:
    preference = json.load(f)
del f

# Extract information
guyprefers = preference['men_preference']
galprefers = preference ['women_preference']  
guys = list(guyprefers.keys())
  
# section 3. assignment, copy, and deepcopy
'''
assignment (a = b)
What it does: It creates a reference to the original object. 
No new object is created; both a and b point to the same memory location.
'''
a = [1, 2, 3]
b = a  # No new object is created
b[0] = 100
print(a)  # Output: [100, 2, 3]

"""
2. Shallow Copy (copy.copy())
What it does: Creates a new object but does not create copies of nested objects 
(only top-level references are copied).

Implication: Changes to mutable elements (such as lists inside lists) 
within the copied object will also affect the original.
"""

a = [[1, 2, 3], [4, 5, 6]]
b = copy.copy(a)  # Shallow copy

b[0] = ["fantastic"]
print(b)
print(a)

b = copy.copy(a)  # Shallow copy
b[0][0] = 100
print(b)
print(a)  # Output: [[100, 2, 3], [4, 5, 6]]


"""
3. Deep Copy (copy.deepcopy())
What it does: Creates a new object and recursively copies all nested objects as well.

Implication: Changes to any part of the copied object do not affect the original object.
"""

a = [[1, 2, 3], [4, 5, 6]]
b = copy.deepcopy(a)  # deep copy

b[0] = ["fantastic"]
print(b)
print(a)

b = copy.deepcopy(a)  # deep copy
b[0][0] = 100
print(b)
print(a)  # Output: [[1, 2, 3], [4, 5, 6]]


# section 4. structure
guypreference = copy.deepcopy(guyprefers)

free_guy = copy.deepcopy(guys)
example = free_guy[:3]
while example:
    a_brave_guy = example.pop()
    print(f'now processing {a_brave_guy}')
    print("=========================")
    mylist = guypreference[a_brave_guy].copy()
    while mylist:
        my_girl = mylist.pop()
        print(f"the lady's name is {my_girl}")
    