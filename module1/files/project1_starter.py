"""
Project 1. Feel free to delete everyting and start from blank.
"""

# 0.import the time module
import

# record the start time
start_time = time.time()

# 1.generate a list with numbers from 1 to 20, name the list as list1
list1 = list(range(1,21))

# 2.print the first 5 elements of list1
print (list1[])

# 3.replace the last entry of the list with 100, and print the whole

print(list1)

# 4.sort the list from the largest to the smallest elemnet. and print list again
list1.sort()
print(list1)

# 5.generate a new list with entries from 14 to 40 with step size 2, name it list2
list2= list(range())

# 6. write a loop, dividing the first 10 entries of list2 by 5, keep the rest of
# list2 unchanged, and store the result in list3
list3 = []
for x in list2[:10]:
    y = x/5
    list3.append(y)
list3 = list3 + list2[10:]

# 7. Given the dictionary hrbook, print the value associate with the key "emp2".
hrbook= {
    'emp1': {'name': 'John', 'salary': 7500},
    'emp2': {'name': 'Emma', 'salary': 8100},
    'emp3': {'name': 'Brad', 'salary': 6500}
    }
print(hrbook.get('emp2'))

# 8. Add a new record to the hrbook
#The key is emp4, value is {'name': 'Misty', 'salary': 7700}


# 9. Use loop and conditional branching to do the following:
# for those whose salary is lower than 7000, replace the salary with 7000,
# for those whose salary is between 7000 and 8000, replace the salary with 8000,
# for those whose salary is higher than 8000, replace the salary with 8200.

for employee in hrbook:
    if hrbook[employee]['salary']<7000:

    elif

    else:


# 10. time your work
# record the end time
end_time =
t = end_time-start_time
print(f"spent {t} seconds to run this script")