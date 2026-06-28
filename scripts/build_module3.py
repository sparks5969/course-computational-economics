#!/usr/bin/env python3
"""Build Module 3 site pages from Canvas HTML sources."""
from __future__ import annotations

from pathlib import Path

from convert_html_source import ROOT, convert, wrap_page

FILES_DIR = ROOT / "module3" / "files"

SRC_DIR = ROOT / "module3" / "from_canvas"
OUT_DIR = ROOT / "module3"

PAGES = [
    (
        "part1. programming paradigm",
        "part1-programming-paradigm.html",
        "Part 1 — Programming Paradigm",
        "part1-programming-paradigm.html",
    ),
    (
        "part 2.1 and part 2.2.html",
        "part2-1-2-functions.html",
        "Part 2.1–2.2 — What & Why Functions",
        "part2-1-2-functions.html",
    ),
    (
        "part2.3.html",
        "part2-user-functions.html",
        "Part 2.3 — User-Defined Functions",
        "part2-user-functions.html",
    ),
    (
        "part3.1_class.html",
        "part3-1-class.html",
        "Part 3.1 — Class",
        "part3-1-class.html",
    ),
    (
        "part3.2_object.html",
        "part3-2-object.html",
        "Part 3.2 — Object",
        "part3-2-object.html",
    ),
    (
        "part3.3_inheritance",
        "part3-3-inheritance.html",
        "Part 3.3 — Inheritance & Subclasses",
        "part3-3-inheritance.html",
    ),
]

OVERVIEW_BODY = """
      <p>This module introduces <strong>programming paradigms</strong>, how to write
      <strong>user-defined functions</strong>, and the foundations of
      <strong>object-oriented programming (OOP)</strong> in Python.</p>

      <h2>Topics</h2>
      <ul>
        <li><strong>Part 1</strong> — Imperative, functional, and OOP paradigms</li>
        <li><strong>Part 2</strong> — What functions are, why to use them, and how to define your own</li>
        <li><strong>Part 3</strong> — Classes, objects, and inheritance with an Animal/Bird example</li>
      </ul>

      <h2>Workshop</h2>
      <p>Work through the workshop pages in order. Parts 3.1–3.3 build on each other — complete them sequentially in Spyder.</p>
"""


def build_overview() -> None:
    page = wrap_page(
        OVERVIEW_BODY,
        "Module 3 Overview",
        module=3,
        active_href="index.html",
        page_heading="Module 3 Overview",
    )
    (OUT_DIR / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'index.html'}")


def build_practice3() -> None:
    FILES_DIR.mkdir(exist_ok=True)

    body = """
      <p>In this project, you will apply <strong>object-oriented programming</strong> to
      simulate the market demand and supply model — and find the equilibrium price computationally.</p>

      <h2>Downloads</h2>
      <ul>
        <li><a href="files/practice_project3.py" download>practice_project3.py</a> — incomplete starter script</li>
        <li><a href="files/practice_project3_promptbook.md" download>practice_project3_promptbook.md</a> — prompt book</li>
      </ul>"""

    page = wrap_page(
        body,
        "Practice Project 3 — Market Simulation",
        module=3,
        active_href="practice3.html",
        page_heading="Practice Project 3 — Market Simulation",
    )
    dst = OUT_DIR / "practice3.html"
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_overview()

    for src_name, out_name, title, active in PAGES:
        src = SRC_DIR / src_name
        body = convert(src.read_text(encoding="utf-8"))
        page = wrap_page(body, title, module=3, active_href=active, page_heading=title)
        dst = OUT_DIR / out_name
        dst.write_text(page, encoding="utf-8")
        print(f"Wrote {dst}")

    build_practice3()


if __name__ == "__main__":
    main()
