# Practice Project 3 Prompt Book — Market Demand & Supply Simulation

## What is a Prompt Book?

A **prompt book** is a collection of plain-language instructions that you give to an AI model
(such as Claude or ChatGPT) one section at a time. Each prompt describes *what* you want the
code to do — the AI writes the actual Python. Your job is to:

1. Copy the **Prompt** into the AI chat.
2. Read the code the AI produces and check that it makes sense.
3. Paste the code into `practice_project3.py` in the right place.
4. Run the file after each section to catch errors early.

Each entry follows this format:

> **Intention** — what this step is trying to achieve and why it matters.
>
> **Prompt** — the exact text you send to the AI.

---

## Background

This project applies **object-oriented programming (OOP)** to economics. You will model a
market made up of individual consumers and producers, simulate their decisions at different
prices, and find the **equilibrium price** — where the gap between quantity demanded and
quantity supplied is less than 5 units.

The project has three layers of increasing complexity:

1. **Define the agents** (consumers and producers as classes)
2. **Simulate the market** (instantiate many agents, search for equilibrium)
3. **Visualize and analyse** (demand/supply curves, technology shock, econometric estimation)

---

## Section 0 — Preparation

### 0-1 · Import libraries and set the random seed

**Intention:** We load all the libraries this project needs upfront. `numpy` handles
random draws and array operations. `matplotlib` draws the graphs. `math` provides `floor()`
for rounding quantities down to whole numbers. Setting a fixed random seed ensures every
student gets the same "random" agents, making results comparable.

**Prompt:**
> Write Python import statements for the following: `numpy` (as `np`), `matplotlib.pyplot`
> (as `plt`), and `math`. Then set the NumPy random seed to 380 using `np.random.seed(380)`.
> Place all of this at the top of the script.

---

## Section 1 — Define Classes

### 1-1 · Base class: `Econ_agent`

**Intention:** `Econ_agent` is the shared blueprint for all market participants. Every
consumer and producer has an ID and a budget, and can introduce themselves. By putting these
shared features in a base class, we avoid repeating them in every child class — this is the
DRY (Don't Repeat Yourself) principle in practice.

**Prompt:**
> Define a Python class called `Econ_agent` with the following:
>
> - `__init__(self, id_number, budget)`: stores `id_number` and `budget` as instance attributes.
> - `introduce_me(self)`: prints a sentence such as
>   `"I am agent 5 with a budget of 320.00."` using the agent's id_number and budget.
>
> No inheritance needed — this is the base class.

---

### 1-2 · Child class: `Consumer`

**Intention:** `Consumer` extends `Econ_agent` to model a buyer. Each consumer has a
`preference` (drawn randomly between 0 and 1), which scales their budget into a
**willingness to pay (wtp)** — the maximum per-unit price they would accept. When the
market price is at or below their wtp, they buy; otherwise they don't.

The quantity purchased reflects both their available funds and their preference:
`wtp / price` tells us how many units they would buy given their preference, capped at 5.

**Prompt:**
> Define a class `Consumer` that inherits from `Econ_agent`:
>
> - `__init__(self, id_number, budget, preference)`:
>   - Call `super().__init__(id_number, budget)` to inherit from `Econ_agent`.
>   - Store `preference` as an attribute.
>   - Compute and store `wtp = self.budget * self.preference`.
>
> - `buying(self, price)`:
>   - If `self.wtp < price`, return 0 (the consumer does not buy).
>   - Otherwise, return `min(5, int(self.wtp / price))` — the number of units bought,
>     capped at 5.

---

### 1-3 · Child class: `Producer`

**Intention:** `Producer` extends `Econ_agent` to model a seller. Each producer has an
`opp_cost` (opportunity cost per unit). They only produce when the market price covers that
cost. The quantity they supply is limited by their budget: a producer with a larger budget
can fund more units of production.

**Prompt:**
> Define a class `Producer` that inherits from `Econ_agent`:
>
> - `__init__(self, id_number, budget, opp_cost)`:
>   - Call `super().__init__(id_number, budget)` to inherit from `Econ_agent`.
>   - Store `opp_cost` as an attribute.
>
> - `selling(self, price)`:
>   - If `self.opp_cost > price`, return 0 (the producer does not sell).
>   - Otherwise, return `int(self.budget / self.opp_cost)` — the quantity supplied,
>     determined by how many units their budget can fund.

---

## Section 2 — Generate Objects

### 2-1 · Create 200 consumers

**Intention:** We populate the market with heterogeneous buyers. Each consumer gets a
unique ID, a budget drawn from a normal distribution (mean 500, s.d. 100 — mimicking
income distribution), and a preference drawn uniformly from [0, 1]. The result is a
list of 200 `Consumer` objects stored in `consumers`.

**Prompt:**
> Create a list called `consumers` containing 200 `Consumer` objects.
> Use a loop with index `i` from 0 to 199:
> - `id_number` = `i`
> - `budget` = a random draw from a normal distribution with mean 500 and standard
>   deviation 100, using `np.random.normal(500, 100)`
> - `preference` = a random draw from a uniform distribution [0, 1],
>   using `np.random.uniform(0, 1)`
>
> Append each new `Consumer` to the `consumers` list.

---

### 2-2 · Create 50 producers

**Intention:** We populate the supply side with heterogeneous sellers. Each producer gets
a unique ID, a budget drawn from a uniform distribution [1000, 2000], and an opportunity
cost drawn from a uniform distribution [100, 200]. The result is a list of 50 `Producer`
objects stored in `producers`.

**Prompt:**
> Create a list called `producers` containing 50 `Producer` objects.
> Use a loop with index `i` from 0 to 49:
> - `id_number` = `i`
> - `budget` = a random draw from a uniform distribution [1000, 2000],
>   using `np.random.uniform(1000, 2000)`
> - `opp_cost` = a random draw from a uniform distribution [100, 200],
>   using `np.random.uniform(100, 200)`
>
> Append each new `Producer` to the `producers` list.

---

## Section 3 — Simulate the Market & Find Equilibrium

### 3-1 · Search for the equilibrium price

**Intention:** In a real market, prices adjust until supply meets demand. We replicate this
with a simulation: start at a low price, compute total demand and total supply by asking
every agent what they would do at that price, then raise the price step by step until the
gap narrows to fewer than 5 units. This is the computational equivalent of Walrasian
tâtonnement.

**Prompt:**
> Write a simulation to find the market equilibrium price.
>
> - Start with `price = 100`.
> - Use a `while` loop that runs as long as the absolute difference between
>   `total_demand` and `total_supply` is greater than 5.
> - Inside the loop:
>   - Compute `total_demand` by summing `c.buying(price)` for every consumer `c`
>     in `consumers`.
>   - Compute `total_supply` by summing `p.selling(price)` for every producer `p`
>     in `producers`.
>   - If `total_demand > total_supply`, increase `price` by 1.
>   - Otherwise, decrease `price` by 1.
> - After the loop ends, print the equilibrium price, total demand, and total supply.

---

## Section 4 — Demand and Supply Curves

### 4-1 · Define the demand function

**Intention:** Rather than a single equilibrium point, we want to trace out how total
demand changes across a range of prices. This is the demand curve. We define it as a
function so it can be reused in Section 5.

**Prompt:**
> Define a function called `demand(price_range)` that takes a list (or array) of prices
> as input. For each price in the list, compute total demand by summing `c.buying(price)`
> for every consumer in `consumers`. Return a list of total demand values, one for each
> price in `price_range`.

---

### 4-2 · Define the supply function

**Intention:** Similarly, we trace how total supply changes across the same price range.

**Prompt:**
> Define a function called `supply(price_range)` that takes a list (or array) of prices
> as input. For each price in the list, compute total supply by summing `p.selling(price)`
> for every producer in `producers`. Return a list of total supply values, one for each
> price in `price_range`.

---

### 4-3 · Visualize demand and supply

**Intention:** Plotting both curves lets us visually verify the model is behaving sensibly:
demand should slope downward, supply should slope upward, and they should cross somewhere
in the price range.

**Prompt:**
> Create a price range from 100 to 200 (inclusive) using `np.arange(100, 201, 1)`.
> Compute demand and supply values by calling `demand(price_range)` and
> `supply(price_range)`.
>
> Plot both curves on the same figure using `matplotlib`:
> - Demand curve: blue line, labeled `"Demand"`.
> - Supply curve: red line, labeled `"Supply"`.
> - Add axis labels (`"Price"` and `"Quantity"`), a title (`"Market Demand and Supply"`),
>   and a legend.
> - Show the plot with `plt.show()`.

---

## Section 5 — Technology Shock

### 5-1 · Simulate the technology improvement

**Intention:** A technological improvement lowers producers' costs. We model this by
reducing every producer's `opp_cost` by 5%. This shifts the supply curve to the right,
which we expect to lower the equilibrium price and increase quantity.

**Prompt:**
> Write a loop over all producers in `producers`. Multiply each producer's `opp_cost`
> by 0.95 (a 5% reduction). Store the modified producers in a new list called
> `producers_new`, or update them in place.
>
> Then repeat the equilibrium search from Section 3 using the updated producers.
> Print the new equilibrium price, total demand, and total supply.
> Compare with the original equilibrium.

---

### 5-2 · Visualize the shift

**Intention:** Visualizing both the old and new supply curves on the same plot makes the
effect of the technology shock immediately visible.

**Prompt:**
> Compute the new supply curve using the updated producers over the same price range
> (100 to 200). Plot three curves on the same figure:
> - Original demand curve: blue, labeled `"Demand"`.
> - Original supply curve: red, labeled `"Supply (before)"`.
> - New supply curve after the technology shock: green dashed line, labeled
>   `"Supply (after tech improvement)"`.
>
> Add axis labels, a title (`"Effect of Technology Improvement"`), and a legend.
> Show the plot.

---

## Section 6 — Estimate Demand and Supply Functions

### 6-1 · Prepare data for regression

**Intention:** The simulated curves are generated from agent behaviour, not a formula.
Here we treat the price-quantity pairs as data and fit a linear regression to each curve,
recovering estimated slope and intercept. This connects the simulation to econometric
methods.

**Prompt:**
> Using the price range (100 to 200) and the demand/supply values computed in Section 4,
> prepare two datasets:
> - `X`: the price values, shaped as a column vector (use `np.array(price_range).reshape(-1, 1)`).
> - `y_demand`: the demand quantities as a NumPy array.
> - `y_supply`: the supply quantities as a NumPy array.

---

### 6-2 · Fit linear regressions

**Intention:** We use NumPy's least-squares solver to estimate the linear relationship
between price and quantity for both demand and supply. The estimated coefficients give us
the slope (how quantity changes per unit of price) and intercept.

**Prompt:**
> Use `np.polyfit(price_range, y_demand, 1)` to fit a linear regression to the demand
> curve. Store the result in `demand_coeffs` — it will contain `[slope, intercept]`.
>
> Do the same for supply: `np.polyfit(price_range, y_supply, 1)`, store in
> `supply_coeffs`.
>
> Print the estimated demand function as: `"Demand: Q = {slope:.4f} * P + {intercept:.2f}"`
> and similarly for supply.

---

### 6-3 · Solve for the analytical equilibrium

**Intention:** With two linear equations (demand and supply as functions of price), we can
solve algebraically for the equilibrium price where quantity demanded equals quantity
supplied. We then compare this calculated equilibrium to the simulated one from Section 3.

**Prompt:**
> The demand function is `Q_d = a*P + b` and supply is `Q_s = c*P + d`,
> where `a, b` come from `demand_coeffs` and `c, d` from `supply_coeffs`.
>
> Solve `a*P + b = c*P + d` for `P`:
> `P_eq = (d - b) / (a - c)`.
>
> Then compute the equilibrium quantity: `Q_eq = a * P_eq + b`.
>
> Print the analytical equilibrium price and quantity. Compare with the simulated result
> from Section 3 and comment on whether they are close.

---

## Expected Output

A successful run should produce:

- A printed equilibrium price (approximately in the range 130–170), with demand and supply
  within 5 units of each other.
- A demand-and-supply chart with two crossing curves (Section 4).
- A printed new equilibrium after the technology shock — a lower price and higher quantity
  than before.
- A chart showing the supply curve shifting right (Section 5).
- Estimated linear coefficients and an analytical equilibrium close to the simulated one
  (Section 6).

---

## Tips for Working with AI

- **Give one prompt at a time.** Paste the code you already have at the start of each new
  prompt so the AI knows what variables and classes exist.
- **Section 3 is the hardest.** If the equilibrium loop doesn't terminate, ask the AI:
  *"The while loop runs forever — what could cause that?"*
- **Check class definitions before Section 2.** Run a quick test after Section 1:
  create one consumer and one producer manually, call their methods, and verify the output
  before generating 200 objects.
- **Section 6 requires Sections 4 data.** Make sure `price_range`, `y_demand`, and
  `y_supply` are still in scope when you run Section 6.
