# Practice Project 4 — Prompt Book
## The Solow-Swan Growth Model

---

### Background

The Solow-Swan model explains long-run economic growth through capital accumulation.
With a Cobb-Douglas production function:

```
Y = a · K^α · L^(1-α)     (aggregate output)
y = a · k^α                (output per worker, where k = K/L)
```

Capital per worker evolves as:
```
Δk = s·y − (n + δ)·k
```
where `s·y` is investment per worker and `(n + δ)·k` is break-even investment
(the amount of investment needed just to keep k constant as the population grows
and capital depreciates).

The **steady state** is where `Δk = 0`, i.e. `s·y* = (n + δ)·k*`.

---

## Section 1 — Import Libraries

**Intention:** Load the three libraries needed for this project: numerical
computation, plotting, and deep-copying objects.

**Prompt:**
> Import `numpy` as `np`, `matplotlib.pyplot` as `plt`, and the `copy` module.

---

## Section 2 — Define the `Growth_model` Class

### 2-1. `__init__` — Initialise the model

**Intention:** Store parameters and initial states, then derive all other initial
state variables from the production function.

**Prompt:**
> Define a class `Growth_model` with an `__init__` method that accepts two
> dictionaries: `para_dict` (keys: `n`, `s`, `alpha`, `delta`, `a`) and
> `state_dict` (keys: `k`, `L`).
>
> Inside `__init__`:
> 1. Store deep copies of both dictionaries as `self.para_dict` and `self.state_dict`.
> 2. Extract scalar values `a`, `alpha`, `delta`, `s`, `k0`, `L0` from the inputs.
> 3. Compute and add the following to `self.state_dict`:
>    - `y` = income per worker: `a * k0 ** alpha`
>    - `K` = aggregate capital: `k0 * L0`
>    - `Y` = aggregate income: `y * L0`
>    - `d` = depreciation per worker: `delta * k0`
>    - `i` = investment per worker: `s * y`
>    - `I` = aggregate investment: `i * L0`
> 4. Set `self.steady_state = {}`.
> 5. Save `self.init_param` and `self.init_state` as deep copies of the original
>    dictionaries (used to reset the model before each simulation).

---

### 2-2. `check_model` — Inspect the model

**Intention:** Provide a quick way to print all current parameters and state
variables so the user can verify the model is set up correctly.

**Prompt:**
> Add a method `check_model(self)` that prints every key-value pair in
> `self.para_dict` under a `"=== Model Parameters ==="` header, and every
> key-value pair in `self.state_dict` under a `"=== State Variables ==="` header.

---

### 2-3. `growth` — Simulate economic growth

**Intention:** Step the model forward `years` periods using the Solow dynamics,
storing the full history of every state variable as a NumPy array.

**Prompt:**
> Add a method `growth(self, years)` that:
>
> 1. **Resets** the model to initial conditions using `copy.deepcopy` on
>    `self.init_param` and `self.init_state`, then re-derives `y`, `K`, `Y`,
>    `d`, `i`, `I` for period 0 (same formulas as `__init__`).
> 2. Creates a `time_line` using `np.linspace(0, years, num=years+1, dtype=int)`.
> 3. Loops over `time_line`. In each iteration:
>    - Load the five parameters (`n`, `s`, `alpha`, `delta`, `a`) from
>      `self.para_dict`.
>    - Load the current-state arrays (`y_t`, `k_t`, `Y_t`, `L_t`, `K_t`,
>      `i_t`, `I_t`, `d_t`) from `self.state_dict`. Each array grows by
>      one element each period.
>    - Calculate next-period values using the last element (`[-1]`) of each
>      array:
>      - `dk = s * y_t[-1] - (n + delta) * k_t[-1]`
>      - `k_next = k_t[-1] + dk`
>      - `L_next = L_t[-1] * (1 + n)`
>      - `y_next = a * k_next ** alpha`
>      - `K_next = k_next * L_next`
>      - `Y_next = y_next * L_next`
>      - `i_next = s * y_next`
>      - `I_next = i_next * L_next`
>      - `d_next = delta * k_next`
>    - Append each `_next` value to its array with `np.append`, and store back
>      into `self.state_dict`.

---

### 2-4. `find_steady_state` — Locate the steady state

**Intention:** Find the steady-state values of k, y, i, and c both numerically
(grid search) and analytically (closed-form formula), print both for comparison,
and store the results in `self.steady_state`.

**Prompt:**
> Add a method `find_steady_state(self)` that:
>
> 1. Loads all five parameters from `self.para_dict`.
> 2. Creates a grid `k_domain = np.linspace(0, 20, 1000)` and computes:
>    - `y_t = a * k_domain ** alpha`
>    - `i_t = s * y_t`
>    - `break_even = (n + delta) * k_domain`
> 3. Finds the index `steady = np.argmin(np.abs(i_t - break_even))` — the point
>    where investment most closely equals break-even investment.
> 4. Extracts:
>    - `k_star = k_domain[steady]`
>    - `y_star = y_t[steady]`
>    - `i_star = s * y_star`
>    - `c_star = (1 - s) * y_star`
> 5. Computes the analytical steady state and prints both:
>    - `k_star_analytical = (s * a / (n + delta)) ** (1 / (1 - alpha))`
>    - Print `"Steady state (numerical): k* = ..."` and
>      `"Steady state (analytical): k* = ..."`
> 6. Stores results in `self.steady_state` with keys `k_star`, `y_star`,
>    `i_star`, `c_star`.
> 7. Returns `[y_star, i_star, c_star]`.

---

### 2-5. `plot_growth` — Solow diagram

**Intention:** Visualise the classic Solow diagram showing how income per worker,
investment per worker, and break-even investment relate to capital per worker.
The crossing point of investment and break-even is the steady state.

**Prompt:**
> Add a method `plot_growth(self, ax)` that:
> 1. Loads parameters from `self.para_dict`.
> 2. Creates a k grid (`np.linspace(0, 20, 500)`) and computes `y`, `i`, and
>    `break_even` over it.
> 3. Plots on `ax`:
>    - `y` vs `k` labelled `"Income per worker (y)"`
>    - `i` vs `k` labelled `"Investment per worker (i)"`
>    - `break_even` vs `k` labelled `"Break-even investment"`
> 4. Adds a vertical dashed line at `k_star` (if `self.steady_state` is
>    non-empty) to mark the steady state.
> 5. Labels the axes (`"Capital per worker (k)"`, `"Per-worker quantities"`),
>    adds a legend and a title `"Solow Diagram"`.

---

### 2-6. `plot_income_growth` — Income over time

**Intention:** Show how aggregate income Y evolves period by period, illustrating
convergence to the steady state growth path.

**Prompt:**
> Add a method `plot_income_growth(self, ax)` that:
> 1. Retrieves the stored `Y` array from `self.state_dict`.
> 2. Plots `Y` against a time index (0 to `len(Y)-1`) on `ax`.
> 3. Labels the axes (`"Time"`, `"Aggregate Income (Y)"`), and adds a title
>    `"Income Growth over Time"`.

---

## Section 3 — Simulate and Examine Growth

### 3-1. Instantiate and simulate

**Intention:** Create a `Growth_model` instance with the given parameters and run
a 100-period simulation.

**Prompt:**
> Define two dictionaries using the values below and instantiate `Growth_model`,
> then call `.growth(100)`:
> ```python
> parameters = {'n': np.array([0.002]), 's': np.array([0.15]),
>               'alpha': np.array([1/3]), 'delta': np.array([0.05]),
>               'a': np.array([1])}
> states = {'k': np.array([1]), 'L': np.array([100])}
> model = Growth_model(parameters, states)
> model.growth(100)
> ```

---

### 3-2. Visualise growth

**Intention:** Display both the Solow diagram and the aggregate income time path
side-by-side in one figure.

**Prompt:**
> Create a figure with two side-by-side subplots (`plt.subplots(1, 2,
> figsize=(12, 5))`). Call `model.plot_growth(axes[0])` and
> `model.plot_income_growth(axes[1])`. Add `plt.tight_layout()` and
> `plt.show()`.

---

### 3-3. Find and print the steady state

**Intention:** Locate the economy's long-run equilibrium values of k, y, i, and c,
and verify the numerical answer against the analytical formula.

**Prompt:**
> Call `model.find_steady_state()` and then `print(model.steady_state)` to
> display k*, y*, i*, and c*.

---

## Section 4 — What-If Analysis: Saving Rate and Steady-State Consumption

### 4-1. Raising the saving rate to 33%

**Intention:** Test how a higher saving rate changes the long-run consumption per
worker. Copy the baseline parameters and update only the saving rate.

**Prompt:**
> Use `copy.deepcopy(parameters)` to create `parameters_33`, then set
> `parameters_33['s'] = np.array([0.33])`. Instantiate `model_33 =
> Growth_model(parameters_33, states)`, simulate 100 periods, and call
> `model_33.find_steady_state()`.

---

### 4-2. Raising the saving rate to 50%

**Intention:** Push the saving rate well above the baseline to observe diminishing
or even negative returns to saving at the steady state.

**Prompt:**
> Repeat the steps from 4-1 with `s = np.array([0.50])`, naming the instance
> `model_50`.

---

### 4-3. Compare and explain

**Intention:** Print a summary table of c* across all three saving rates and use
economic reasoning to interpret the pattern.

**Prompt:**
> Print the value of `c_star` from `model.steady_state`, `model_33.steady_state`,
> and `model_50.steady_state`. Then write a brief comment in the script explaining
> your finding.
>
> **Economic hint:** With α = 1/3, the Golden Rule saving rate is exactly s = α = 1/3.
> - At s = 15% (below the Golden Rule): the economy is under-saving; raising s
>   increases c*.
> - At s = 33% (at the Golden Rule): steady-state consumption c* is maximised.
> - At s = 50% (above the Golden Rule): the economy is over-saving; workers
>   sacrifice too much current consumption; c* falls. This is called
>   **dynamic inefficiency**.
