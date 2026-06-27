# Project 2 Prompt Book — The Gale-Shapley Algorithm

## What is a Prompt Book?

A **prompt book** is a collection of plain-language instructions that you give to an AI model
(such as Claude or ChatGPT) one section at a time. Each prompt describes *what* you want the
code to do — the AI writes the actual Python. 

Each interaction follows this format:

> **Intention** — what this step is trying to achieve and why it matters.
>
> **Prompt** — the exact text you send to the AI.

You do not need to memorize Python syntax. You need to understand what each step *means*.

---

## Background

The **Gale-Shapley algorithm** finds a *stable matching* between two equal-sized groups —
in this project, 30 men and 30 women. Each person has a ranked preference list over everyone
in the other group. The algorithm guarantees that the final matching is stable: no man and
woman would both prefer each other over their current partners.

---

## Data File

The file `project2_data.json` has this structure:

```json
{
  "men_preference": {
    "Ismael": ["Annabelle", "Paula", "Carol", ...],
    "Kenneth": ["Jillian", "Susan", "Annabelle", ...],
    ...
  },
  "women_preference": {
    "Leslie": ["Devin", "Johnnie", "Sammy", ...],
    "Erica": ["Johnnie", "Erwin", "Kevin", ...],
    ...
  }
}
```

Each key is a person's name. Each value is a list of names ranked from most to least preferred.
There are 30 men and 30 women.

---

## Section 1 — Preparation

### 1-1 · Import modules

**Intention:** Before writing any logic, we load the tools we will need. The `json` module
lets Python read `.json` files. The `time` module lets us measure how long the script takes
to run — useful for comparing the efficiency of different algorithms.

**Prompt:**
> Write two Python import statements at the top of the script: one to import the built-in
> `json` module, and one to import the built-in `time` module. Then add a line that records
> the current time into a variable called `start_time` using `time.time()`.

---

### 1-2 · Load the dataset

**Intention:** The preference data lives in an external file. We open it and parse its
contents into a Python dictionary so the rest of the script can work with it as a normal
data structure.

**Prompt:**
> Open the file `project2_data.json` for reading using a `with open(...) as f:` block.
> Inside the block, use `json.load(f)` to parse the file and store the result in a variable
> called `data`. The variable `data` will be a Python dictionary.

---

## Section 2 — Set Up the Data Structures

### 2-1 · Men's preference dictionary

**Intention:** The raw dataset has two sections mixed together. Here we pull out just the
men's preferences and give it a clear name so the algorithm can refer to it directly.

**Prompt:**
> From the dictionary `data`, extract the value stored under the key `'men_preference'`
> and save it in a variable called `guyprefers`. This is a dictionary where each key is
> a man's name (string) and each value is a list of women's names ordered from most to
> least preferred.

---

### 2-2 · Women's preference dictionary

**Intention:** Same as above, but for women's preferences. The algorithm needs both sides
to decide whether a woman would accept a new proposal or stay with her current partner.

**Prompt:**
> From the dictionary `data`, extract the value stored under the key `'women_preference'`
> and save it in a variable called `galprefers`. This is a dictionary where each key is
> a woman's name (string) and each value is a list of men's names ordered from most to
> least preferred.

---

### 2-3 · List of free men

**Intention:** The algorithm works by tracking which men have not yet been matched. We start
with all men unmatched. Sorting alphabetically just makes the output easier to read and the
behavior easier to predict.

**Prompt:**
> Create a list called `free_guys` that contains all the keys from the `guyprefers`
> dictionary. Sort the list alphabetically (A to Z) in place using the `.sort()` method.

---

### 2-4 · Empty engagement book

**Intention:** We need a place to record the current state of the matching as the algorithm
runs. An empty dictionary works well: the woman's name is the key, and the man she is
engaged to is the value.

**Prompt:**
> Create an empty dictionary called `engage_book`. This dictionary will store the evolving
> matching results. The key will be a woman's name and the value will be the name of the
> man she is currently engaged to.

---

### 2-5 · Working copies of preference lists

**Intention:** The algorithm will remove names from preference lists as proposals are made.
If we modify the originals, we lose the data permanently. By working on copies, we keep
`guyprefers` and `galprefers` intact in case we need them later (e.g. for the stability check).
A simple `.copy()` is not enough here because the values are lists — we need a deep copy.

**Prompt:**
> Create two working copies of the preference dictionaries so the algorithm can modify them
> without changing the originals.
>
> - Create `guypreference` as a deep copy of `guyprefers` using the dictionary comprehension
>   `{k: v[:] for k, v in guyprefers.items()}`.
> - Create `galpreference` as a deep copy of `galprefers` the same way.
>
> The algorithm will pop names off these working lists as proposals are made.

---

## Section 3 — Implement the Gale-Shapley Algorithm

### 3-1 · Outer loop — free men keep proposing

**Intention:** The algorithm repeats as long as any man remains unmatched. In each round,
we pick one free man and let him make his next best proposal. The loop ends naturally once
every man has been matched.

**Prompt:**
> Write a `while` loop that runs as long as the list `free_guys` is not empty.
> At the start of each iteration, remove and store the first man in `free_guys` using
> `.pop(0)` — call him `guy`. Then retrieve his current working preference list from
> `guypreference[guy]` — call it `his_list`.

---

### 3-2 · Inner loop — one man works through his list

**Intention:** Each free man proposes to women one by one, starting from the top of his
list, until he either gets accepted or runs out of candidates. The inner loop drives this
process: remove the top name from his list and try her next.

**Prompt:**
> Inside the outer `while` loop, write another `while` loop that runs as long as `his_list`
> is not empty. At the start of each iteration, remove and store the first woman in
> `his_list` using `.pop(0)` — call her `girl`.

---

### 3-3 · Proposal logic — accept, reject, or replace

**Intention:** This is the core decision rule of the algorithm. If the woman is free, she
accepts immediately. If she is already engaged, she compares the new proposer to her current
partner and keeps whoever she ranks higher. The man she drops returns to the free pool and
will try again in a later round.

**Prompt:**
> Inside the inner loop (after `girl` is chosen), write an `if / else` block:
>
> **If `girl` is not yet in `engage_book`** (she is free):
> - Add her to `engage_book` with `guy` as her partner.
> - Break out of the inner loop — this man is now engaged and stops proposing for now.
>
> **Else** (she is already engaged — call her current partner `current_guy`):
> - Look up her preference list in `galpreference[girl]`.
> - Compare the index (position) of `guy` and `current_guy` in that list.
>   A lower index means she prefers that person more.
> - **If she prefers `guy`** (his index is lower than `current_guy`'s index):
>   - Update `engage_book[girl]` to `guy`.
>   - Add `current_guy` back to `free_guys` — he is now free again.
>   - Break out of the inner loop.
> - **Otherwise** (she prefers her current partner):
>   - Do nothing — `guy` remains free and the inner loop continues to his next choice.

---

### 3-4 · Print the result

**Intention:** Once the algorithm finishes, we display the final matching so we can inspect
it and verify it looks reasonable. We also confirm the total count equals 30.

**Prompt:**
> After both loops finish, print the contents of `engage_book` in a readable format.
> Use a `for` loop over `engage_book.items()` to print each matched pair on its own line,
> formatted as: `Woman: <name>  -->  Man: <name>`.
> Then print a summary line `"Total pairs matched: <n>"` using `len(engage_book)`.

---

## Section 4 — Report Runtime

### 4-1 · Elapsed time

**Intention:** Measuring runtime helps us appreciate algorithm efficiency. The Gale-Shapley
algorithm should finish in a fraction of a second even for 30 pairs — a good talking point
about computational complexity.

**Prompt:**
> At the very end of the script, calculate elapsed time by subtracting `start_time` from
> `time.time()` and storing the result in a variable called `elapsed`. Print a message such
> as: `"Total runtime: X.XXXX seconds"` using an f-string formatted to 4 decimal places.

---

## Section 5 (Optional) — Stability Check

### 5-1 · Define the stability checker

**Intention:** The whole point of the Gale-Shapley algorithm is to produce a *stable*
matching. This step lets us verify the result computationally rather than just trust it.
A blocking pair — two people who would both prefer each other over their current partners —
would prove the matching is unstable.

**Prompt:**
> Write a function called `is_stable(engage_book, guyprefers, galprefers)` that checks
> whether the matching is stable.
>
> First, build a reverse lookup from the matching: for each woman-man pair in `engage_book`,
> record the man's partner as well.
>
> A matching is **unstable** if there exist a man M and a woman W (not matched to each other)
> such that M prefers W over his current partner AND W prefers M over her current partner.
>
> Loop over all possible man-woman pairs not in the current matching and check for this
> condition. If a blocking pair is found, print their names and return `False`. If no
> blocking pair exists, print a confirmation message and return `True`.

---

### 5-2 · Run the check

**Intention:** We call the function on the actual output and print the verdict.

**Prompt:**
> After printing the matched pairs in Section 3, call
> `is_stable(engage_book, guyprefers, galprefers)` and print whether the matching is stable.

---

## Expected Output

When your script runs correctly, you should see:

- 30 matched pairs, each woman appearing exactly once as a key in `engage_book`.
- A runtime of well under 1 second.
- (Optional) A message confirming the matching is stable.

Example lines:
```
Woman: Annabelle  -->  Man: Kenneth
Woman: Paula  -->  Man: Christopher
...
Total pairs matched: 30
Total runtime: 0.0012 seconds
Matching is stable: True
```

---

## Tips for Working with AI

- **Give one prompt at a time.** Pasting all prompts at once often produces tangled code.
- **Paste the code you already have** at the start of each new prompt so the AI knows
  what variable names have already been defined.
- **If the AI output looks wrong**, describe the specific problem: "the inner loop never
  breaks" or "it prints a KeyError on line X" — concrete error descriptions get better fixes.
- **Run after each section.** Catching a bug in Section 2 is much easier than debugging
  a full script in Section 3.
