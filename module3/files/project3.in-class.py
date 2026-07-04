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

 