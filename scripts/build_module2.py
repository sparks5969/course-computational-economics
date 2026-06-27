#!/usr/bin/env python3
"""Build Module 2 site pages from Canvas HTML sources."""
from __future__ import annotations

import shutil
from pathlib import Path

from convert_html_source import ROOT, convert, wrap_page

SRC_DIR = ROOT / "module2" / "from_canvas"
OUT_DIR = ROOT / "module2"
FILES_DIR = OUT_DIR / "files"

PAGES = [
    (
        "module2_overview.html",
        "index.html",
        "Module 2 Overview",
        "index.html",
    ),
    (
        "module2_part1.1.functions associated with list.html",
        "part1-1-list-functions.html",
        "Part 1.1 — List Functions",
        "part1-1-list-functions.html",
    ),
    (
        "module2_part1.2.functions associated with dictionary.html",
        "part1-2-dict-functions.html",
        "Part 1.2 — Dictionary Functions",
        "part1-2-dict-functions.html",
    ),
    (
        "module2_part2_logic operators.html",
        "part2-logic-operators.html",
        "Part 2 — Logical Operators",
        "part2-logic-operators.html",
    ),
    (
        "module2_part3_more about loops.html",
        "part3-loops.html",
        "Part 3 — More About Loops",
        "part3-loops.html",
    ),
    (
        "module2_part4 and part5.html",
        "part4-json-comments.html",
        "Part 4 & 5 — JSON & Comments",
        "part4-json-comments.html",
    ),
]


def build_practice2() -> None:
    starter_py = (SRC_DIR / "project2.py").read_text(encoding="utf-8")
    page = wrap_page(
        f"""
      <p>In this project, you will work with a given dataset and apply the
      <strong>Gale–Shapley algorithm</strong> to solve a stable-matching problem.</p>

      <div class="starter-note">
        <strong>Before you start:</strong> Download the dataset and starter script below.
        Place <code>project2_data.json</code> in the same folder as your script.
        Upload your completed Python script on Canvas before the deadline.
      </div>

      <h2>Downloads</h2>
      <ul>
        <li><a href="files/project2_data.json" download>project2_data.json</a> — preference dataset</li>
        <li><a href="files/project2.py" download>project2.py</a> — incomplete starter script</li>
      </ul>

      <h2>Background</h2>
      <p>The dataset contains simplified information from a dating website:</p>
      <ul>
        <li>There are 30 men and 30 women.</li>
        <li>Each woman has met all the men; each man has met all the women.</li>
        <li>Each person has a preference list of potential partners, ranked from most ideal (index 0) to least ideal (index 29).</li>
      </ul>
      <p>Your task is to find a <strong>stable matching</strong>: there must be no two people of opposite sex who would both rather have each other than their current partners.</p>

      <h2>Section 1 — Preparation</h2>
      <div class="task-block">
        <div class="task-number">1-1</div>
        <p>Import all necessary Python modules. You will need the built-in <code>json</code> module.</p>
      </div>
      <div class="task-block">
        <div class="task-number">1-2</div>
        <p>Import the given dataset (the JSON file).</p>
      </div>

      <h2>Section 2 — Extract Information</h2>
      <p>Create the Python objects you need from the dataset:</p>
      <ul>
        <li><code>guyprefers</code> — men's preferences</li>
        <li><code>galprefers</code> — women's preferences</li>
        <li><code>free_guy</code> — men who are currently not engaged, sorted alphabetically</li>
        <li><code>engage_book</code> — empty dictionary to store results</li>
        <li>Make copies of <code>guyprefers</code> and <code>galprefers</code> for use during the algorithm</li>
      </ul>

      <h2>Section 3 — Gale–Shapley Algorithm</h2>
      <p>Implement the algorithm. The starter script includes the first steps — pop a free man, get his preference list, and begin proposing. Complete the loop logic.</p>

      <h2>Section 4 — Verify the Solution (optional)</h2>
      <p>Check stability: confirm there are no two people of opposite sex who would both prefer each other over their current partners.</p>

      <h2>Starter Script</h2>
      <p>The incomplete script is provided below for reference:</p>
      <div class="code-cell code-input">
        <div class="code-label">project2.py</div>
        <pre><code>{_escape(starter_py)}</code></pre>
      </div>
""",
        "Practice Project 2 — Gale-Shapley Algorithm",
        module=2,
        active_href="practice2.html",
        page_heading="Practice Project 2",
    )
    # Inject practice-page styles
    page = page.replace(
        "</head>",
        """  <style>
    .starter-note {
      background: var(--color-accent-light);
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin: 1.5rem 0;
      font-size: 0.92rem;
    }
    .task-block {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      border-left: 4px solid var(--color-accent);
      border-radius: 8px;
      padding: 1.2rem 1.4rem;
      margin: 1.5rem 0;
    }
    .task-block .task-number {
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--color-accent);
      margin-bottom: 0.4rem;
    }
    .task-block p { margin: 0.3rem 0 0; }
  </style>
</head>""",
    )
    (OUT_DIR / "practice2.html").write_text(page, encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'practice2.html'}")


def _escape(text: str) -> str:
    import html as html_mod

    return html_mod.escape(text)


def main() -> None:
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    for name in ("project2.py", "project2_data.json"):
        shutil.copy2(SRC_DIR / name, FILES_DIR / name)
        print(f"Copied {name} → {FILES_DIR / name}")

    for src_name, out_name, title, active in PAGES:
        src = SRC_DIR / src_name
        dst = OUT_DIR / out_name
        body = convert(src.read_text(encoding="utf-8"))
        page = wrap_page(body, title, module=2, active_href=active, page_heading=title)
        dst.write_text(page, encoding="utf-8")
        print(f"Wrote {dst}")

    build_practice2()


if __name__ == "__main__":
    main()
