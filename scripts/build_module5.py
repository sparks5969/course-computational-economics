#!/usr/bin/env python3
"""Build Module 5 site pages.

Module 5 combines two old modules (Pandas + Machine Learning).
Pages are built with custom bodies rather than the Canvas converter
because the source files use Colab-notebook HTML rather than the
standard Canvas kl_wrapper structure.
"""
from __future__ import annotations

from convert_html_source import ROOT, wrap_page

OUT_DIR = ROOT / "module5"

# ── Colab link helper ─────────────────────────────────────────────────────────

def _colab_block(url: str) -> str:
    return f"""
      <div class="callout">
        <div class="callout-title">Hands-on Notebook</div>
        <p>
          <a href="{url}" target="_blank" rel="noopener" class="download-link">
            &#x1F4D3; Open in Google Colab
          </a>
        </p>
        <p style="margin-top:0.6rem; font-size:0.9rem;">
          Once opened, click <strong>Copy to Drive</strong> to save your own
          editable copy before you start.
        </p>
      </div>"""


# ── Part 1: Pandas ────────────────────────────────────────────────────────────

def pandas_1_basics() -> None:
    body = """
      <h2>What You'll Learn</h2>
      <p>This section teaches the fundamentals of Pandas — Python's core library for
      data manipulation. You will work with real sports datasets to practice the
      building blocks of data analysis.</p>

      <ul>
        <li><strong>Pandas Data Structures</strong> — understand Series and DataFrames</li>
        <li><strong>Access and Slice Data</strong> — indexing, <code>.loc</code>, and <code>.iloc</code></li>
        <li><strong>Combine Datasets</strong> — merge and concatenate with <code>.concat()</code> and <code>.merge()</code></li>
        <li><strong>Work with Real Data</strong> — football club statistics and European soccer match data</li>
      </ul>

      <h2>Learning Approach</h2>
      <p>The notebook contains clear explanations, hands-on tasks with specific instructions,
      and empty code cells where you write your solutions. Concepts build on each other
      progressively.</p>

      <h2>Download</h2>
      <p><a class="download-link" href="Pandas_basics.ipynb" download>
        &#x1F4E5; Download notebook (Pandas_basics.ipynb)
      </a></p>
""" + _colab_block("https://colab.research.google.com/drive/1c8GGdZPyybGDCLO73tfxFBiTCwhKsPYg?usp=sharing")

    page = wrap_page(body, "Part 1.1 — Pandas Basics", module=5,
                     active_href="pandas-1-basics.html",
                     page_heading="Part 1.1 — Pandas Basics")
    dst = OUT_DIR / "pandas-1-basics.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


def pandas_2_exploration() -> None:
    body = """
      <h2>Mastering Pandas for Data Exploration</h2>
      <p>This hands-on session focuses on comprehensive data exploration and analysis
      using a rich dataset of soccer game statistics. You will uncover insights into
      team performance, match outcomes, and key metrics.</p>

      <h2>Learning Objectives</h2>
      <ul>
        <li><strong>Load and Inspect Data</strong> — <code>.head()</code>, <code>.info()</code>, <code>.describe()</code></li>
        <li><strong>Query and Filter</strong> — select rows and columns, filter by conditions</li>
        <li><strong>Feature Engineering</strong> — create new columns such as <code>total_goals</code> and <code>goal_difference</code></li>
        <li><strong>Data Cleaning</strong> — handle missing values and rename columns</li>
        <li><strong>Group and Aggregate</strong> — <code>groupby()</code> to compute team statistics and winning rates</li>
        <li><strong>Visualize Data</strong> — basic plots for key findings and trends</li>
        <li><strong>AI-Assisted Workflow</strong> — break tasks down, translate intentions into prompts, iterate</li>
      </ul>

      <h2>Dataset</h2>
      <p>The <code>soccer_data.csv</code> dataset contains detailed match information
      including competition details, team names, goal counts, formations, and final scores.</p>

      <h2>Download</h2>
      <p><a class="download-link" href="Pandas_data_exploration_ipynb.ipynb" download>
        &#x1F4E5; Download notebook (Pandas_data_exploration_ipynb.ipynb)
      </a></p>
""" + _colab_block("https://colab.research.google.com/drive/1VEll6LSSQGF8RoyRJXslE0Q8XyUPmhLK#scrollTo=ce305322")

    page = wrap_page(body, "Part 1.2 — Data Exploration", module=5,
                     active_href="pandas-2-exploration.html",
                     page_heading="Part 1.2 — Data Exploration with Pandas")
    dst = OUT_DIR / "pandas-2-exploration.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


def pandas_3_preprocessing() -> None:
    body = """
      <h2>Data Preprocessing</h2>
      <p>Real-world data is rarely clean or directly usable for modeling. This section
      walks through each step of transforming the raw <strong>Ames Housing dataset</strong>
      into a fully usable modeling dataset — and explains not only <em>what</em> to do
      but <em>why</em> each operation matters.</p>

      <h2>What You'll Learn</h2>
      <ol>
        <li><strong>Train/Test Split</strong> — make all preprocessing decisions on training data to prevent data leakage</li>
        <li><strong>Identify Missing Values</strong> — quantify and assess missingness across variables</li>
        <li><strong>Drop High-Missingness Features</strong> — remove columns with more than 40% missing data</li>
        <li><strong>Separate Numerical and Categorical Variables</strong> — different types need different strategies</li>
        <li><strong>Impute Missing Values</strong> — median imputation, KNN imputation, and categorical fill</li>
        <li><strong>Ordinal vs. Nominal Encoding</strong> — distinguish ordered scales from unordered labels</li>
        <li><strong>Manual Ordinal Encoding</strong> — map quality ratings to meaningful integers</li>
        <li><strong>One-Hot Encoding</strong> — convert nominal categories into binary indicator variables</li>
      </ol>

      <p>Together these steps form a complete, replicable preprocessing pipeline you can
      apply to any structured dataset in future projects.</p>
""" + _colab_block("https://colab.research.google.com/drive/1EqBzCx5UAYhfabN2VoNzP6E08iyu3dWv?usp=sharing")

    page = wrap_page(body, "Part 2.2 — Data Preprocessing", module=5,
                     active_href="ml-1-preprocessing.html",
                     page_heading="Part 2.2 — Data Preprocessing")
    dst = OUT_DIR / "ml-1-preprocessing.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


# ── Part 2: Machine Learning ──────────────────────────────────────────────────

def ml_1_ai_coding() -> None:
    body = """
      <p>Before diving into machine learning models, this page introduces the
      <strong>AI-assisted coding framework</strong> — a structured way to work with AI
      that keeps you in control of the design, logic, and verification of your code.</p>

      <h2>Mindset Layer — Your Role and Attitude</h2>
      <ol>
        <li><strong>Plan before you code</strong> — AI can't design what you haven't imagined.
        Define inputs, outputs, and logic first: you are the architect.</li>
        <li><strong>Manage your expectations</strong> — AI accelerates progress, not perfection.
        Debugging, reasoning, and problem framing are still your job.</li>
        <li><strong>Reflect on your partnership</strong> — after each session ask:
        <em>What did I rely on AI for? What did I still do myself?</em></li>
      </ol>

      <h2>Process Layer — How You Work with AI</h2>
      <p>Frame every task with <strong>Intention</strong> and <strong>Prompt</strong>:</p>
      <ul>
        <li><strong style="color:#c0392b;">Intention</strong> — what you want to achieve and why it matters</li>
        <li><strong style="color:#c0392b;">Prompt</strong> — how you'll communicate this to AI</li>
      </ul>
      <p>This separation keeps you in the driver's seat of problem design.</p>

      <p>Additional principles:</p>
      <ul>
        <li><strong>Take small steps</strong> — ask for one function or fix at a time, test it, then expand</li>
        <li><strong>Verify the code</strong> — fluent ≠ correct; run, test, and explain before trusting it</li>
        <li><strong>Iterate like a scientist</strong> — predict → prompt → test → reflect → adjust</li>
        <li><strong>Audit for bias and brittleness</strong> — test edge cases: empty data, nulls, extreme values</li>
      </ul>

      <h2>Communication Layer — How You Talk to AI</h2>
      <ul>
        <li><strong>Explain your intent</strong> — describe what you want, why, and how it fits your larger goal</li>
        <li><strong>Spell out names clearly</strong> — use descriptive variable names like <code>customer_purchases</code> not <code>df</code></li>
        <li><strong>Own the context</strong> — remind AI of libraries, data shape, and constraints often</li>
        <li><strong>Document as you go</strong> — use AI to help write comments and docstrings</li>
        <li><strong>Learn from the AI</strong> — don't just accept code; reverse-engineer it and ask why</li>
      </ul>

      <h2>Common Mistakes to Avoid</h2>
      <table>
        <thead>
          <tr><th>Mistake</th><th>Why it happens</th><th>How to fix it</th></tr>
        </thead>
        <tbody>
          <tr><td>Copy-paste without understanding</td><td>AI code looks professional</td><td>Explain it line-by-line before using</td></tr>
          <tr><td>Asking for too much at once</td><td>Trying to save time</td><td>Break into smaller, testable pieces</td></tr>
          <tr><td>Not testing edge cases</td><td>AI shows typical cases only</td><td>Manually test: empty data, nulls, extremes</td></tr>
          <tr><td>Treating AI as oracle</td><td>"The code runs = it's right"</td><td>Verify logic, not just syntax</td></tr>
          <tr><td>Repeating failed prompts</td><td>Hoping for different results</td><td>Rephrase with more context or constraints</td></tr>
        </tbody>
      </table>"""

    page = wrap_page(body, "AI-Assisted Coding", module=5,
                     active_href="ml-1-ai-coding.html",
                     page_heading="AI-Assisted Coding")
    dst = OUT_DIR / "ml-1-ai-coding.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


def ml_2_eda() -> None:
    body = """
      <h2>Exploratory Data Analysis (EDA) and Visualization</h2>
      <p>This section covers the fundamental steps for exploratory data analysis.
      Each task reflects the typical process a data analyst would follow to understand
      a dataset before building any predictive model.</p>

      <p>For each task you are given the <strong>Intention</strong> — what it is meant to
      achieve. Your practice is to determine the right prompt to achieve the desired outcome
      using an AI-assisted coding workflow.</p>

      <h2>What You'll Learn</h2>
      <ul>
        <li>Perform standard EDA steps: load, inspect, summarize, and clean data</li>
        <li>Create visualizations using Pandas and Matplotlib</li>
        <li>Apply the Intention → Prompt framework to real data tasks</li>
        <li>Develop habits that prepare data for future modeling steps</li>
      </ul>
""" + _colab_block("https://colab.research.google.com/drive/10z6wVzUupvp0WbkeTpmbM8CUk7mYfJjE#scrollTo=e24fa06d")

    page = wrap_page(body, "Part 2.1 — EDA & Visualization", module=5,
                     active_href="ml-2-eda.html",
                     page_heading="Part 2.1 — EDA &amp; Visualization")
    dst = OUT_DIR / "ml-2-eda.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


def ml_3_models() -> None:
    body = """
      <h2>Building and Evaluating Machine Learning Models</h2>
      <p>This section focuses on building, training, and evaluating machine learning
      regression models for <strong>housing price prediction</strong> using the
      preprocessed Ames Housing data from Part 1.3.</p>

      <h2>Learning Objectives</h2>
      <ol>
        <li><strong>Implement regression models</strong> — Linear Regression, Lasso,
        Decision Trees, Random Forests, and Gradient Boosting</li>
        <li><strong>Interpret model performance</strong> — Mean Squared Error (MSE)
        and R-squared</li>
        <li><strong>Visualize predictions</strong> — plot predicted vs. observed values
        to assess model fit</li>
        <li><strong>Analyze feature importance</strong> — identify which variables drive
        predictions in each model</li>
        <li><strong>Hyperparameter tuning</strong> — use GridSearchCV to optimize performance</li>
        <li><strong>Understand model tradeoffs</strong> — bias-variance tradeoff and overfitting</li>
      </ol>
""" + _colab_block("https://colab.research.google.com/drive/1Oj0rf5BaygRRucYj0Aoa8t7OC1gkY6YU#scrollTo=NFFnSXQNYiMh")

    page = wrap_page(body, "Part 2.3 — Building ML Models", module=5,
                     active_href="ml-3-models.html",
                     page_heading="Part 2.3 — Building ML Models")
    dst = OUT_DIR / "ml-3-models.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pandas_1_basics()
    pandas_2_exploration()
    pandas_3_preprocessing()
    ml_1_ai_coding()
    ml_2_eda()
    ml_3_models()


if __name__ == "__main__":
    main()
