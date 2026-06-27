#!/usr/bin/env python3
"""Replace sidebar navigation in all site HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

from convert_html_source import ROOT, home_sidebar_html, sidebar_html, wrap_home_page, home_body_html

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
    # Rebuild home page body + sidebar together
    index.write_text(wrap_home_page(home_body_html()), encoding="utf-8")
    print(f"Updated {index}")

    module1_index = ROOT / "module1" / "index.html"
    if module1_index.exists():
        html = replace_nav(module1_index.read_text(encoding="utf-8"), sidebar_html(1, "index.html"))
        module1_index.write_text(html, encoding="utf-8")
        print(f"Updated {module1_index}")

    for filename, active in MODULE1_ACTIVE.items():
        path = ROOT / "module1" / filename
        html = replace_nav(path.read_text(encoding="utf-8"), sidebar_html(1, active))
        path.write_text(html, encoding="utf-8")
        print(f"Updated {path}")

    for mod in (2, 3, 4, 5):
        mod_dir = ROOT / f"module{mod}"
        if not mod_dir.exists():
            continue
        for path in sorted(mod_dir.glob("*.html")):
            active = path.name
            html = replace_nav(path.read_text(encoding="utf-8"), sidebar_html(mod, active))
            path.write_text(html, encoding="utf-8")
            print(f"Updated {path}")


if __name__ == "__main__":
    main()
