#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:15:25 2020

@author: sw
"""

class Customer:
    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type
        

eg1 = Customer('Sining','Gold')
eg2 = Customer ('Jesse','silver')


print(eg1.name,eg1.membership_type)


customer_list = [Customer('Sining','Gold'),
                 Customer ('Danny','Silver')]

print(customer_list[1].name)


class Customer:
    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type
        species = 'human'
    
    # update membership   
    def update_membership(self,new_membership):
        self.membership_type = new_membership
        
customer_list = [Customer('Sining','Gold'),
                 Customer ('Danny','Silver')]

print(customer_list[1].name,customer_list[1].membership_type)

customer_list[1].update_membership('Gold')

print(customer_list[1].name,customer_list[1].membership_type)

# this method is not really necessary, as we can assign attribute values directly
customer_list[1].membership_type='super'
print(customer_list[1].name,customer_list[1].membership_type)

# more examples
class Customer:
    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type
    # update membership   
    def update_membership(self,new_membership):
        self.membership_type = new_membership
        # invoke an API
        # update address
        # charge money
        # return a product
        # destory one's PC
        # conquer the world
        
# some other useful methods we can overwrite
    # str
class Customer:
    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type
    # update membership   
    def update_membership(self,new_membership):
        self.membership_type = new_membership
        # invoke an API
        # update address
        # charge money
        # return a product
        # destory one's PC
        # conquer the world
    
        
    def __str__(self):
        return self.name + " " + self.membership_type

# before overwrite __str__
print(customer_list[1])
# after overwrite the __str__

customer_list = [Customer('Sining','Gold'),
                 Customer ('Danny','Silver')]

print(customer_list[1])



# talk about the self and static method
class Customer:
    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type
    # update membership   
    def update_membership(self,new_membership):
        self.membership_type = new_membership
        # invoke an API
        # update address
        # charge money
        # return a product
        # destory one's PC
        # conquer the world
        
    def __str__(self):
        return self.name + " " + self.membership_type
        
    def print_all(customer_list):
        print('All customer in database')
        for people in customer_list:
            print(people)

customer_list = [Customer('Sining','Gold'),
             Customer ('Danny','Silver')]
customer_list[1].print_all(customer_list)
Customer.print_all(customer_list)

