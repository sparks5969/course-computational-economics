"""
Practice Project 3: Market Demand & Supply Simulation

Apply Object-Oriented Programming to simulate the market demand/supply model
and find the equilibrium price computationally.
"""

import numpy as np
import matplotlib.pyplot as plt
import math

np.random.seed(380)

# =============================================================================
# Section 1. Define classes
# =============================================================================

# 1-1. Base class: Econ_agent
# attributes: id_number, budget
# methods:    introduce_me(self), print agent's id number and budget

class Econ_agent:

    def __init__(self, id_number, budget):
        self.id_number = id_number
        self.budget    = budget

    def introduce_me(self):
        ...   # print a sentence with the agent's id_number and budget


# 1-2. Child class: Consumer (inherits from Econ_agent)
# additional attributes:
#   preference: how much the consumer likes the product (uniform draw from [0,1])
#   wtp: willingness to pay = budget * preference
# additional methods:
#   buying(self, price)
#     if wtp < price, return 0 (does not buy)
#     otherwise       return min(5, int(wtp / price))

class Consumer(Econ_agent):

    def __init__(self, id_number, budget, preference):
        super().__init__(id_number, budget)
        self.preference = preference
        self.wtp        = self.budget * self.preference

    def buying(self, price):
        if self.wtp < price:
            return 0
        return ...   # min(5, int(self.wtp / price))


# 1-3. Child class: Producer (inherits from Econ_agent)
# additional attributes:
#   opp_cost: opportunity cost per unit (constant for each producer)
# additional methods:
#   selling(self, price)
#     if opp_cost > price, return 0 (does not produce)
#     otherwise            return int(budget / opp_cost)

class Producer(Econ_agent):

    def __init__(self, id_number, budget, opp_cost):
        super().__init__(id_number, budget)
        self.opp_cost = ...   # store opp_cost

    def selling(self, price):
        ...   # return 0 if opp_cost > price, else int(self.budget / self.opp_cost)


# =============================================================================
# Section 2. Generate objects
# =============================================================================

# 2-1. Create a list of 200 consumers
# id_number : 0 to 199
# budget    : normal distribution, mean=500, s.d.=100, np.random.normal(500, 100)
# preference: uniform distribution [0, 1]              np.random.uniform(0, 1)
consumers = []
for i in range(200):
    ...   # instantiate Consumer and append to consumers


# 2-2. Create a list of 50 producers
# id_number : 0 to 49
# budget    : uniform distribution [1000, 2000], np.random.uniform(1000, 2000)
# opp_cost  : uniform distribution [100, 200],    np.random.uniform(100, 200)
producers = []
for i in range(50):
    ...   # instantiate Producer and append to producers


# =============================================================================
# Section 3. Simulate the market mechanism and find the equilibrium
# =============================================================================
# Find the equilibrium price where |total_demand - total_supply| < 5
# Start at price = 100; raise by 1 if demand > supply, lower by 1 otherwise.

price        = 100
total_demand = ...   # initialise (e.g. sum buying at price=100)
total_supply = ...   # initialise (e.g. sum selling at price=100)

while abs(total_demand - total_supply) > 5:
    total_demand = ...   # sum c.buying(price) for all c in consumers
    total_supply = ...   # sum p.selling(price) for all p in producers
    if total_demand > total_supply:
        price += 1
    else:
        price -= 1

print(f"Equilibrium price: {price}")
print(f"Total demand: {total_demand},  Total supply: {total_supply}")


# =============================================================================
# Section 4. Define demand and supply curves
# =============================================================================

# 4-1. Demand function over a price range
def demand(price_range):
    ...   # for each price, sum c.buying(price) for all consumers; return list


# 4-2. Supply function over a price range
def supply(price_range):
    ...   # for each price, sum p.selling(price) for all producers; return list


# 4-3. Visualise demand and supply curves (price range 100 to 200)
price_range = np.arange(100, 201, 1)
...   # compute demand and supply, plot both curves with labels and legend


# =============================================================================
# Section 5. Technology shock — 5% reduction in opp_cost
# =============================================================================
# Reduce every producer's opp_cost by 5%, then re-run the equilibrium search.
# Visualise original supply vs new supply on the same chart.

for p in producers:
    ...   # p.opp_cost *= 0.95

# re-run equilibrium search (same structure as Section 3)
...

# plot demand, old supply, and new supply curves
...


# =============================================================================
# Section 6. Estimate demand and supply functions with linear regression
# =============================================================================
# Use np.polyfit to fit linear regressions to the Section 4 curves.
# Solve the two linear equations to find the analytical equilibrium price.
# Compare with the simulated equilibrium from Section 3.

demand_coeffs = ...   # np.polyfit(price_range, y_demand, 1)
supply_coeffs = ...   # np.polyfit(price_range, y_supply, 1)

# print estimated functions
...

# solve for analytical equilibrium: set Q_d = Q_s and solve for P
P_eq = ...   # (d - b) / (a - c)
Q_eq = ...   # a * P_eq + b

print(f"Analytical equilibrium: price = {P_eq:.2f}, quantity = {Q_eq:.2f}")
