#!/usr/bin/env python3
"""Replace sidebar navigation in all site HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

from convert_html_source import ROOT, home_sidebar_html, sidebar_html

NAV_RE = re.compile(r"<nav>.*?</nav>", re.DOTALL)

MODULE1_ACTIVE = {
    "part1-installation.html": "part1-installation.html",
    "part2-language.html": "part2-language.html",
    "part3-packages.html": "part3-packages.html",
    "part4-data-structures.html": "part4-data-structures.html",
    "part5-programming.html": "part5-programming.html",
    "practice1.html": "practice1.html",
}


def replace_nav(html: str, nav: str) -> str:
    return NAV_RE.sub(f"<nav>\n{nav}\n      </nav>", html, count=1)


def main() -> None:
    index = ROOT / "index.html"
    index.write_text(
        replace_nav(index.read_text(encoding="utf-8"), home_sidebar_html()),
        encoding="utf-8",
    )
    print(f"Updated {index}")

    for filename, active in MODULE1_ACTIVE.items():
        path = ROOT / "module1" / filename
        html = replace_nav(path.read_text(encoding="utf-8"), sidebar_html(1, active))
        path.write_text(html, encoding="utf-8")
        print(f"Updated {path}")

    module2_dir = ROOT / "module2"
    for path in sorted(module2_dir.glob("*.html")):
        active = path.name
        html = replace_nav(path.read_text(encoding="utf-8"), sidebar_html(2, active))
        path.write_text(html, encoding="utf-8")
        print(f"Updated {path}")

    module3_dir = ROOT / "module3"
    for path in sorted(module3_dir.glob("*.html")):
        active = path.name
        html = replace_nav(path.read_text(encoding="utf-8"), sidebar_html(3, active))
        path.write_text(html, encoding="utf-8")
        print(f"Updated {path}")


if __name__ == "__main__":
    main()
