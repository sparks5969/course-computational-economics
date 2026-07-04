"""
Practice Project 4 — The Solow-Swan Growth Model

Production function (Cobb-Douglas):
    Y = a * K^alpha * L^(1-alpha)
Per-worker form:
    y = a * k^alpha    (where k = K/L)
"""

# Section 1. Preparation — import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import copy


# Section 2. Define the Growth model as a class

class Growth_model:
    """
    Solow-Swan growth model with Cobb-Douglas production.

    Arguments
    ----------
    para_dict : dict
        n     – population growth rate
        s     – saving rate
        alpha – capital share in production
        delta – depreciation rate
        a     – total factor productivity
    state_dict : dict
        k – initial capital per worker
        L – initial population (labour force)
    """

    def __init__(self,
                 para_dict={'n':     np.array([0.002]),
                            's':     np.array([0.15]),
                            'alpha': np.array([1/3]),
                            'delta': np.array([0.05]),
                            'a':     np.array([1])},
                 state_dict={'k': np.array([1]),
                             'L': np.array([100])}):

        self.para_dict  = ...   # store a deep copy of para_dict
        self.state_dict = ...   # store a deep copy of state_dict

        # extract scalars for initial calculations
        a     = para_dict['a'][0]
        alpha = para_dict['alpha'][0]
        delta = para_dict['delta'][0]
        s     = para_dict['s'][0]
        k0    = state_dict['k'][0]
        L0    = state_dict['L'][0]

        # derive and store initial state variables
        self.state_dict['y'] = ...   # income per worker:        a * k0^alpha
        self.state_dict['K'] = ...   # aggregate capital:        k0 * L0
        self.state_dict['Y'] = ...   # aggregate income:         y * L0
        self.state_dict['d'] = ...   # depreciation per worker:  delta * k0
        self.state_dict['i'] = ...   # investment per worker:    s * y
        self.state_dict['I'] = ...   # aggregate investment:     i * L0

        self.steady_state = {}

        # save originals for resetting in growth()
        self.init_param = copy.deepcopy(para_dict)
        self.init_state = copy.deepcopy(state_dict)

    def check_model(self):
        """Print all current parameters and state variables."""
        ...

    def get_param(self):
        return self.para_dict

    def get_state(self):
        return self.state_dict

    def growth(self, years):
        """Simulate economic growth for a given number of years."""

        # reset to initial status
        self.para_dict  = copy.deepcopy(self.init_param)
        self.state_dict = copy.deepcopy(self.init_state)

        # re-derive initial state variables after reset
        a     = self.init_param['a'][0]
        alpha = self.init_param['alpha'][0]
        delta = self.init_param['delta'][0]
        s     = self.init_param['s'][0]
        k0    = self.init_state['k'][0]
        L0    = self.init_state['L'][0]
        y0    = a * k0 ** alpha
        self.state_dict['y'] = np.array([y0])
        self.state_dict['K'] = np.array([k0 * L0])
        self.state_dict['Y'] = np.array([y0 * L0])
        self.state_dict['d'] = np.array([delta * k0])
        self.state_dict['i'] = np.array([s * y0])
        self.state_dict['I'] = np.array([s * y0 * L0])

        # step 1. define the time line
        time_line = np.linspace(0, years, num=years + 1, dtype=int)

        # step 2. simulate growth period by period
        for t in time_line:

            # 2.1 load parameters
            n     = self.para_dict.get('n')[0]
            s     = ...
            alpha = ...
            delta = ...
            a     = ...

            # 2.2 load current states
            y_t = self.state_dict.get('y')
            k_t = ...
            Y_t = ...
            L_t = ...
            K_t = ...
            i_t = ...
            I_t = ...
            d_t = ...

            # 2.3 calculate next-period states
            dk     = ...   # change in capital per worker:  s*y_t[-1] - (n+delta)*k_t[-1]
            k_next = ...   # k_t[-1] + dk
            L_next = ...   # L_t[-1] * (1 + n)
            y_next = ...   # a * k_next^alpha
            K_next = ...   # k_next * L_next
            Y_next = ...   # y_next * L_next
            i_next = ...   # s * y_next
            I_next = ...   # i_next * L_next
            d_next = ...   # delta * k_next

            # 2.4 append new states to history arrays
            self.state_dict['k'] = np.append(k_t, k_next)
            self.state_dict['y'] = np.append(y_t, y_next)
            self.state_dict['Y'] = np.append(Y_t, Y_next)
            self.state_dict['K'] = np.append(K_t, K_next)
            self.state_dict['L'] = np.append(L_t, L_next)
            self.state_dict['i'] = np.append(i_t, i_next)
            self.state_dict['I'] = np.append(I_t, I_next)
            self.state_dict['d'] = np.append(d_t, d_next)

    def find_steady_state(self):
        """Find steady state numerically and verify with analytical formula."""

        # step 1. load parameters
        n     = self.para_dict.get('n')[0]
        s     = ...
        alpha = ...
        delta = ...
        a     = ...

        # step 2. numerical grid search
        k_domain   = np.linspace(0, 20, 1000)
        y_t        = ...                       # income per worker over k grid: a * k_domain^alpha
        i_t        = ...                       # investment per worker: s * y_t
        break_even = (n + delta) * k_domain   # break-even investment

        # find the index where i_t is closest to break_even
        diff   = i_t - break_even
        steady = ...   # np.argmin(np.abs(diff))

        # step 3. extract steady-state values
        k_star = k_domain[steady]
        y_star = ...
        i_star = ...
        c_star = ...   # (1 - s) * y_star

        # step 4. verify with analytical formula
        k_star_analytical = ...   # (s * a / (n + delta)) ** (1 / (1 - alpha))
        print(f"Steady state (numerical):  k* = {k_star:.4f}")
        print(f"Steady state (analytical): k* = {k_star_analytical:.4f}")

        self.steady_state = {
            'k_star': k_star,
            'y_star': y_star,
            'i_star': i_star,
            'c_star': c_star,
        }
        return [y_star, i_star, c_star]

    def plot_growth(self, ax):
        """Solow diagram: y, i, and break-even investment against k."""
        ...

    def plot_income_growth(self, ax):
        """Plot aggregate income Y over time."""
        ...


# Section 3. Specify model parameters and examine economic growth

parameters = {'n':     np.array([0.002]),   # population growth rate
              's':     np.array([0.15]),     # saving rate
              'alpha': np.array([1/3]),      # capital share
              'delta': np.array([0.05]),     # depreciation rate
              'a':     np.array([1])}        # total factor productivity

states = {'k': np.array([1]),     # initial capital per worker
          'L': np.array([100])}   # initial population

# 3-1. instantiate the model and simulate 100 periods
model = Growth_model(parameters, states)
model.growth(100)

# 3-2a. Solow diagram: y, i, and break-even vs k
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
model.plot_growth(axes[0])

# 3-2b. aggregate income over time
model.plot_income_growth(axes[1])
plt.tight_layout()
plt.show()

# 3-3. find and print the steady state
model.find_steady_state()
print(model.steady_state)


# Section 4. What-if analysis — effect of the saving rate on steady-state consumption

# 4-1. s = 33%
parameters_33 = ...   # copy parameters and update 's' to np.array([0.33])
model_33 = Growth_model(parameters_33, states)
model_33.growth(100)
model_33.find_steady_state()

# 4-2. s = 50%
parameters_50 = ...   # copy parameters and update 's' to np.array([0.50])
model_50 = Growth_model(parameters_50, states)
model_50.growth(100)
model_50.find_steady_state()

# 4-3. Compare c* across saving rates and explain the pattern
print("\n=== Steady-State Consumption Comparison ===")
print(f"s = 15%: c* = {model.steady_state['c_star']:.4f}")
print(f"s = 33%: c* = {model_33.steady_state['c_star']:.4f}")
print(f"s = 50%: c* = {model_50.steady_state['c_star']:.4f}")
# Question: Does higher saving always raise steady-state consumption?
# Hint: think about the Golden Rule of capital accumulation.
