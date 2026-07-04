"""
Weekly project 2. The Gale-Shapley algorithm
"""

# ── Section 1. Preparation ───────────────────────────────────────────────────

# 1-1. import the json module and the time module
#      record the current time in start_time
import json
import time

start_time = time.time()

# 1-2. open 'project2_data.json' and load it into a variable called 'data'
with open('project2_data.json') as f:
    data = json.load(f)


# ── Section 2. Set up data structures ────────────────────────────────────────

# 2-1. extract men's preferences from data → store in 'guyprefers'
guyprefers = data['men_preference']

# 2-2. extract women's preferences from data → store in 'galprefers'
galprefers = data['women_preference']

# 2-3. create a list of all men who are currently free, sorted alphabetically
#      → store in 'free_guys'
free_guys = list(guyprefers.keys())
free_guys.sort()

# 2-4. create an empty dictionary to store engagement results → 'engage_book'
engage_book = {}

# 2-5. make deep copies of guyprefers and galprefers for use during the algorithm
#      (the algorithm will modify these copies, not the originals)
guypreference = {k: v[:] for k, v in guyprefers.items()}
galpreference = {k: v[:] for k, v in galprefers.items()}


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
        if girl not in engage_book:
            engage_book[girl] = guy
            break
        else:
            current_guy = engage_book[girl]
            her_list = galpreference[girl]
            if her_list.index(guy) < her_list.index(current_guy):
                engage_book[girl] = guy
                free_guys.append(current_guy)
                break
            # else: she prefers current partner, guy stays free, tries next girl


# 3-4. print the result: one matched pair per line, then total count
for girl, guy in engage_book.items():
    print(f"Woman: {girl}  -->  Man: {guy}")
print(f"Total pairs matched: {len(engage_book)}")


# ── Section 4. Report runtime ─────────────────────────────────────────────────

# calculate elapsed time using start_time and print it
elapsed = time.time() - start_time
print(f"Total runtime: {elapsed:.4f} seconds")


# ── Section 5. Stability check ────────────────────────────────────

# define stability: there are no two people of opposite sex who would both
# rather have each other than their current partners.
def is_stable(engage_book, guyprefers, galprefers):
    guy_partner = {guy: girl for girl, guy in engage_book.items()}

    for guy in guyprefers:
        for girl in galprefers:
            if guy_partner.get(guy) == girl:
                continue

            his_current = guy_partner[guy]
            her_current = engage_book[girl]

            guy_prefers_girl = (
                guyprefers[guy].index(girl) < guyprefers[guy].index(his_current)
            )
            girl_prefers_guy = (
                galprefers[girl].index(guy) < galprefers[girl].index(her_current)
            )

            if guy_prefers_girl and girl_prefers_guy:
                print(f"Blocking pair found: {guy} and {girl}")
                return False

    print("No blocking pair found.")
    return True


stable = is_stable(engage_book, guyprefers, galprefers)
print(f"Matching is stable: {stable}")
