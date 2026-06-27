#!/usr/bin/env python3
"""Build course home page and module overview pages."""
from __future__ import annotations

from pathlib import Path

from convert_html_source import (
    ROOT,
    home_body_html,
    wrap_home_page,
    wrap_page,
)

MODULE1_CARDS = [
    ("part1-installation.html", "Part 1", "Installation", "Install Anaconda and Spyder."),
    ("part2-language.html", "Part 2", "Python Language", "Why Python is used in economics."),
    ("part3-packages.html", "Part 3", "Packages & Modules", "Import packages and modules."),
    ("part4-data-structures.html", "Part 4", "Data Structures", "Lists, dictionaries, and more."),
    ("part5-programming.html", "Part 5", "Programming", "Conditionals, indentation, and loops."),
    ("practice1.html", "Practice", "Practice Project 1", "Lists, dictionaries, loops, and timing."),
]


def module1_body() -> str:
    cards = "\n".join(
        f'          <a class="card" href="{href}">\n'
        f'            <div class="card-step">{step}</div>\n'
        f"            <h3>{title}</h3>\n"
        f"            <p>{desc}</p>\n"
        f"          </a>"
        for href, step, title, desc in MODULE1_CARDS
    )
    return f"""
      <p>Install Anaconda and Spyder, then work through Python basics, data structures,
      and your first practice project.</p>

      <div class="callout">
        <div class="callout-title">Before you start</div>
        <p>Complete <strong>Part 1: Installation</strong> before class if you have not used Python before.</p>
      </div>

      <h2>Workshop</h2>
      <div class="card-grid">
{cards}
      </div>"""


def coming_soon_body(module: int) -> str:
    return f"""
      <div class="callout">
        <div class="callout-title">Coming soon</div>
        <p>Module {module} materials are not yet published. Check back later or return to the
        <a href="../index.html">course home</a>.</p>
      </div>"""


def main() -> None:
    (ROOT / "index.html").write_text(wrap_home_page(home_body_html()), encoding="utf-8")
    print(f"Wrote {ROOT / 'index.html'}")

    m1_dir = ROOT / "module1"
    m1_dir.mkdir(exist_ok=True)
    page = wrap_page(
        module1_body(),
        "Module 1 Overview",
        module=1,
        active_href="index.html",
        page_heading="Module 1 — Python Foundations",
    )
    (m1_dir / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote {m1_dir / 'index.html'}")

    for num in (4, 5):
        mod_dir = ROOT / f"module{num}"
        mod_dir.mkdir(exist_ok=True)
        page = wrap_page(
            coming_soon_body(num),
            f"Module {num} Overview",
            module=num,
            active_href="index.html",
            page_heading=f"Module {num}",
        )
        (mod_dir / "index.html").write_text(page, encoding="utf-8")
        print(f"Wrote {mod_dir / 'index.html'}")


if __name__ == "__main__":
    main()
