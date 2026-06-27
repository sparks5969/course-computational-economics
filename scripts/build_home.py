#!/usr/bin/env python3
"""Build course home page and ALL module overview pages (consistent 3-section layout)."""
from __future__ import annotations

import html as html_mod
from pathlib import Path

from convert_html_source import (
    ROOT,
    MODULE2_WORKSHOP,
    MODULE3_WORKSHOP,
    home_body_html,
    wrap_home_page,
    wrap_page,
)

# ── per-module config ─────────────────────────────────────────────────────────

MODULES = {
    1: {
        "title": "Module 1 — Python Foundations",
        "subtitle": "Module 1 — Python Foundations",
        "description": (
            "Install Anaconda and Spyder, then work through Python basics, "
            "data structures, and complete your first practice project."
        ),
        "slides": "module1_introduction.pptx",
        "workshop_cards": [
            ("part1-installation.html",    "Part 1",    "Installation",          "Install Anaconda and Spyder."),
            ("part2-language.html",        "Part 2",    "Python Language",        "Why Python is used in economics."),
            ("part3-packages.html",        "Part 3",    "Packages &amp; Modules", "Import packages and use others' code."),
            ("part4-data-structures.html", "Part 4",    "Data Structures",        "Lists, dictionaries, and more."),
            ("part5-programming.html",     "Part 5",    "Programming",            "Conditionals, indentation, and loops."),
            ("practice1.html",             "Practice",  "Practice Project 1",     "Lists, dictionaries, loops, and timing."),
        ],
    },
    2: {
        "title": "Module 2 Overview",
        "subtitle": "Module 2 — Stable Matching",
        "description": (
            "Implement and execute the Gale–Shapley Algorithm to solve stable "
            "matching problems. Explore real-world applications such as medical "
            "residency programs and school admissions."
        ),
        "slides": "module2_gale_shapley.pptx",
        "workshop_cards": [
            ("part1-1-list-functions.html",  "Part 1.1", "List Functions",             "Dot-syntax methods for lists."),
            ("part1-2-dict-functions.html",  "Part 1.2", "Dictionary Functions",       "Methods for working with dicts."),
            ("part2-logic-operators.html",   "Part 2",   "Logical Operators",          "<code>and</code>, <code>or</code>, <code>not</code>."),
            ("part3-loops.html",             "Part 3",   "Loops",                      "Nested loops, break, and continue."),
            ("part4-json-comments.html",     "Part 4–5", "JSON &amp; Comments",        "Read JSON files and document code."),
            ("practice2.html",               "Practice", "Practice Project 2",         "Gale–Shapley stable matching."),
        ],
    },
    3: {
        "title": "Module 3 Overview",
        "subtitle": "Module 3 — OOP &amp; Functions",
        "description": (
            "Learn programming paradigms, write user-defined functions, and "
            "explore object-oriented programming through classes, objects, and inheritance."
        ),
        "slides": None,
        "workshop_cards": [
            ("part1-programming-paradigm.html", "Part 1",   "Programming Paradigm",        "Imperative, functional, and OOP styles."),
            ("part2-1-2-functions.html",        "Part 2.1–2.2", "What &amp; Why Functions", "DRY principle and function basics."),
            ("part2-user-functions.html",       "Part 2.3", "User-Defined Functions",       "Write your own functions with <code>def</code>."),
            ("part3-1-class.html",              "Part 3.1", "Class",                        "Blueprints with <code>__init__</code> and methods."),
            ("part3-2-object.html",             "Part 3.2", "Object",                       "Create and use objects from a class."),
            ("part3-3-inheritance.html",        "Part 3.3", "Inheritance",                  "Subclasses, superclasses, and overriding."),
        ],
    },
    4: {
        "title": "Module 4 Overview",
        "subtitle": "Module 4",
        "description": None,
        "slides": None,
        "workshop_cards": [],
    },
    5: {
        "title": "Module 5 Overview",
        "subtitle": "Module 5",
        "description": None,
        "slides": None,
        "workshop_cards": [],
    },
}

# ── shared section builder ────────────────────────────────────────────────────

PLACEHOLDER = (
    '<p class="placeholder">Material not yet available — check back soon.</p>'
)


def _slides_section(slides: str | None, module: int) -> str:
    if slides:
        return f"""
      <section>
        <h2>Lecture Slides</h2>
        <p><a class="download-link" href="{slides}" download>
          &#x1F4E5; Download {slides}
        </a></p>
      </section>"""
    return f"""
      <section>
        <h2>Lecture Slides</h2>
        {PLACEHOLDER}
      </section>"""


def _workshop_section(cards: list[tuple], *, is_coming_soon: bool) -> str:
    if is_coming_soon:
        return f"""
      <section>
        <h2>Workshop</h2>
        {PLACEHOLDER}
      </section>"""
    card_html = "\n".join(
        f'        <a class="card" href="{href}">\n'
        f'          <div class="card-step">{step}</div>\n'
        f"          <h3>{title}</h3>\n"
        f"          <p>{desc}</p>\n"
        f"        </a>"
        for href, step, title, desc in cards
    )
    return f"""
      <section>
        <h2>Workshop</h2>
        <div class="card-grid">
{card_html}
        </div>
      </section>"""


def module_overview_body(num: int) -> str:
    cfg = MODULES[num]
    desc = cfg["description"]
    coming_soon = not desc

    overview_section = f"""
      <section>
        <h2>Overview</h2>
        {"<p>" + html_mod.escape(desc) + "</p>" if desc else PLACEHOLDER}
      </section>"""

    slides_section = _slides_section(cfg["slides"], num)
    workshop_section = _workshop_section(cfg["workshop_cards"], is_coming_soon=coming_soon)

    return overview_section + slides_section + workshop_section


# ── build ─────────────────────────────────────────────────────────────────────

def main() -> None:
    (ROOT / "index.html").write_text(wrap_home_page(home_body_html()), encoding="utf-8")
    print(f"Wrote {ROOT / 'index.html'}")

    for num, cfg in MODULES.items():
        mod_dir = ROOT / f"module{num}"
        mod_dir.mkdir(exist_ok=True)
        page = wrap_page(
            module_overview_body(num),
            cfg["title"],
            module=num,
            active_href="index.html",
            page_heading=cfg["subtitle"],
        )
        (mod_dir / "index.html").write_text(page, encoding="utf-8")
        print(f"Wrote {mod_dir / 'index.html'}")


if __name__ == "__main__":
    main()
