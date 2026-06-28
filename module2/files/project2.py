"""
Weekly project 2. The Gale-Shapley algorithm
"""

# ── Section 1. Preparation ───────────────────────────────────────────────────

# 1-1. import the json module and the time module
#      record the current time in start_time


# 1-2. open 'project2_data.json' and load it into a variable called 'data'
with open('project2_data.json') as f:
    data = ...


# ── Section 2. Set up data structures ────────────────────────────────────────

# 2-1. extract men's preferences from data → store in 'guyprefers'
guyprefers = ...

# 2-2. extract women's preferences from data → store in 'galprefers'
galprefers = ...

# 2-3. create a list of all men who are currently free, sorted alphabetically
#      → store in 'free_guys'
free_guys = ...

# 2-4. create an empty dictionary to store engagement results → 'engage_book'
engage_book = ...

# 2-5. make deep copies of guyprefers and galprefers for use during the algorithm
#      (the algorithm will modify these copies, not the originals)
guypreference = ...
galpreference = ...


# ── Section 3. Implement the Gale-Shapley algorithm ──────────────────────────

# Outer loop: keep going while there are free men
while free_guys:

    # pop the first man from free_guys → call him 'guy'
    guy = free_guys.pop(0)

    # get his current working preference list → call it 'his_list'
    his_list = guypreference[guy]

    # Inner loop: guy proposes one by one until he is engaged
    while his_list:

        # pop the top woman from his list → call her 'girl'
        girl = his_list.pop(0)

        # YOUR CODE HERE:
        # if girl is free → engage her with guy, break
        # if girl is already engaged → compare her preference
        #     if she prefers guy → update engage_book, return old partner to free_guys, break
        #     if she prefers current partner → do nothing, continue to next woman


# 3-4. print the result: one matched pair per line, then total count


# ── Section 4. Report runtime ─────────────────────────────────────────────────

# calculate elapsed time using start_time and print it


# ── Section 5. Stability check ────────────────────────────────────

# define stability: there are no two people of opposite sex who would both
# rather have each other than their current partners.
