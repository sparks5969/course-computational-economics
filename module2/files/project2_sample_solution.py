"""
Project 2 Sample Solution. The Gale-Shapley Algorithm
"""

# Section 1. Preparation

# 1-1. import necessary modules and record start time
import json
import time

start_time = time.time()

# 1-2. load the dataset from the JSON file
with open('project2_data.json') as f:
    data = json.load(f)


# Section 2. Set up data structures

# 2-1. men's preference dictionary
guyprefers = data['men_preference']

# 2-2. women's preference dictionary
galprefers = data['women_preference']

# 2-3. list of free men, sorted alphabetically
free_guys = list(guyprefers.keys())
free_guys.sort()

# 2-4. empty dictionary to store the matching results
engage_book = {}

# 2-5. working copies of preference lists (deep copies so originals are preserved)
guypreference = {k: v[:] for k, v in guyprefers.items()}
galpreference = {k: v[:] for k, v in galprefers.items()}


# Section 3. Implement the Gale-Shapley algorithm

while free_guys:
    # 3-1. pick the first free man and get his working preference list
    guy      = free_guys.pop(0)
    his_list = guypreference[guy]

    while his_list:
        # 3-2. propose to the top woman on his list
        girl = his_list.pop(0)

        # 3-3. proposal logic
        if girl not in engage_book:
            # she is free — accept immediately
            engage_book[girl] = guy    # record the match
            break                      # this man is now engaged
        else:
            # she is already engaged — compare the two suitors
            current_guy = engage_book[girl]
            her_list    = galpreference[girl]
            if her_list.index(guy) < her_list.index(current_guy):
                # she prefers the new proposer
                engage_book[girl] = guy          # update the match
                free_guys.append(current_guy)    # displaced man goes back to pool
                break
            # else: she prefers her current partner — guy continues proposing

# 3-4. print the final matching
for woman, man in engage_book.items():
    print(f"Woman: {woman}  -->  Man: {man}")
print(f"Total pairs matched: {len(engage_book)}")


# Section 4. Report runtime

# 4-1. calculate and print elapsed time
elapsed = time.time() - start_time
print(f"Total runtime: {elapsed:.4f} seconds")


# Section 5 (Optional). Stability check

def is_stable(engage_book, guyprefers, galprefers):
    # reverse lookup: each man's current partner
    guy_partner = {guy: girl for girl, guy in engage_book.items()}

    for guy in guyprefers:
        for girl in galprefers:
            if guy_partner[guy] == girl:
                continue    # already matched to each other, not a blocking pair

            his_current = guy_partner[guy]
            her_current = engage_book[girl]

            guy_prefers_girl  = guyprefers[guy].index(girl) < guyprefers[guy].index(his_current)
            girl_prefers_guy  = galprefers[girl].index(guy) < galprefers[girl].index(her_current)

            if guy_prefers_girl and girl_prefers_guy:
                print(f"Blocking pair found: {guy} and {girl}")
                return False

    print("No blocking pair found.")
    return True

is_stable(engage_book, guyprefers, galprefers)
