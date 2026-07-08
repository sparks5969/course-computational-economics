# 1. demonstrate how class works
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

eg1.name


class Customer:
    def __init__(self, name, membership_type):
        self.name = name
        self.membership_type = membership_type
        
    def update_membership(self, new_membership):
        self.membership_type = new_membership
    
    # invoke an API
    # update address
    # charge money
    # return a product
    # destory one's PC
    # conquer the world
    

eg1 = Customer("Sining", 'Gold')
eg2 = Customer("Jesse", "Silver")

eg2.membership_type

eg2.update_membership("gold")
eg2.membership_type



# 2. demonstrate how inheritance works
class Econ_agent:
    def __init__(self, name, budget):
        self.name = name
        self.endowment = budget
        
# instaniate an object
eg1 = Econ_agent("Sining", 10)


# creating a child class
class Consumer(Econ_agent):
    def __init__(self, name, endowment, id_number, wtp):
        super().__init__(name, endowment)  # keep the inheritance
        self.id_number = id_number
        self.wtp = wtp
        
consumer1 = Consumer("James", 50, 1, 20)

consumer1.name



# encapsulation is important

# BAD: Global variables

# one consumer is acting
money = 100
items = []

# Code in one part of the program
money = money - 30  # buying a book
items.append("book")


# aother consumer is coming.....
money = money * 2   # oops, someone else is using 'money' for calculations
items.clear()       # someone clearing a list, not knowing it's our shopping items!

# now consumer 1 back to shopping Back to shopping
money = money - 20  # buying food, but 'money' isn't what we expect anymore!
items.append("food")

print(f"Money: ${money}")  # Value is unexpected
print(f"Items: {items}")   # Items list lost previous purchases!


# GOOD: Encapsulation
class Consumer:
    def __init__(self, budget):
        self._budget = budget
        self._items = []
    
    def buy(self, item, price):
        if price > self._budget:
            raise ValueError("Not enough money!")
        self._budget -= price
        self._items.append(item)

buyer1 = Consumer(100)
buyer1.buy("book", 30)  # Our shopping logic is protected from outside interference
buyer1.buy("robot", 50)
buyer1.buy("air condition", 300)

# if you want to have a new consumer to do something, you will first need to
# instantiate it!
buyer2 = Consumer(50)  # Another consumer with different budget

buyer2.buy("coffee", 5)  # buyer2 has their own money and items
# Each buyer has their own separate budget and items - no interference!


# Create a market with multiple consumers
import random

# Create a list of consumers with different budgets
buyers = []
num_buyers = 5

# Method 1: Simple for loop
for i in range(num_buyers):
    budget = random.randint(50, 150)  # Random budget between 50-150
    buyer = Consumer(budget)
    buyers.append(buyer)

# Method 2: List comprehension (more concise)
buyers = [Consumer(random.randint(50, 150)) for _ in range(num_buyers)]

# Now you can have all buyers try to buy something
item_price = 40
for buyer in buyers:
    try:
        buyer.buy("book", item_price)
    except ValueError as e:
        print(f"A buyer couldn't afford the book: {e}")

 

 