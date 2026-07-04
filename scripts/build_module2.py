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
    body = """
      <h2>Background</h2>
      <p>In this project you will implement the <strong>Gale-Shapley algorithm</strong>
      to find a stable matching between 30 men and 30 women from a preference dataset.</p>
      <p>A matching is <em>stable</em> if no man and woman both prefer each other over
      their current partners. The algorithm guarantees a stable result.</p>

      <h2>Downloads</h2>
      <p>
        <a class="download-link" href="files/project2_data.json" download>
          &#x1F4E5; Download dataset (project2_data.json)
        </a>
      </p>
      <p>
        <a class="download-link" href="files/project2.py" download>
          &#x1F4E5; Download starter script (project2.py)
        </a>
      </p>
      <p>
        <a class="download-link" href="files/project2_promptbook.md" download>
          &#x1F4E5; Download prompt book (project2_promptbook.md)
        </a>
      </p>"""

    page = wrap_page(body, "Practice Project 2 — Gale-Shapley Algorithm",
                     module=2, active_href="practice2.html",
                     page_heading="Practice Project 2 — Gale-Shapley Algorithm")
    (OUT_DIR / "practice2.html").write_text(page, encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'practice2.html'}")


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
