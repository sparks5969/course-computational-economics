"""
Weekly project 2. The Gale-Shapley algorithm
"""

# Section 1. Preparation
# 1-1. import all the necessary python modules


# 1-2. import the datasets
with open('project2_data.json') as f:


# Section 2 Extract information from the dataset, 
# 2-1. create a dictionary 'guyprefer' contains mens' preferences
guyprefers = 
    
# 2-2. create a dictionary 'galprefer' contains women's preferences
galprefers = 
    
# 2-3. create a list contains guys who are currently not engaged, 
# sort alphabetically
free_guy = 

# 2-4. generate an empty dictionary 'engage_book' to store result
engage_book = 

# 2-5. make copies of guyprefers and gal refers
guypreference = .copy()


# Section 3. Impletement the Gale-Shapley algorithm 
# Follow the algorithm flowchart, it should be very helpful

# pop the first guy in the free_guy list, let him take the move
a_brave_guy = free_guy.pop(0)
# get his preference list
mylist = guypreference[a_brave_guy].copy()
# let this guy take the move
while  mylist:
    # Let's propose to my favorate lady!
    my_girl = mylist.pop(0)
    # YOU WILL NEED TO DO THE REST, GOOD LUCK AND HAVE FUN!.


student_list.remove[0]
# Section 4 (optional). Stability check
# define stability: there are no two people of opposite sex who would both
# rather have each other than their current partners.

