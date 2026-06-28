#!/usr/bin/env python3
"""Build Module 4 site pages from Canvas HTML sources."""
from __future__ import annotations

from convert_html_source import ROOT, convert, wrap_page

SRC_DIR = ROOT / "module4" / "from_canvas"
OUT_DIR = ROOT / "module4"

PAGES = [
    (
        "part1.1_generate_vectors.html",
        "part1-1-generate-vectors.html",
        "Part 1.1 — Generate Vectors",
        "part1-1-generate-vectors.html",
    ),
    (
        "part1.2_calculation with vectors.html",
        "part1-2-vector-addition.html",
        "Part 1.2 — Vector Addition",
        "part1-2-vector-addition.html",
    ),
    (
        "part1.3_calculation with multiplication.html",
        "part1-3-vector-multiplication.html",
        "Part 1.3 — Vector Multiplication",
        "part1-3-vector-multiplication.html",
    ),
    (
        "part2.1_generate_matrices.html",
        "part2-1-generate-matrices.html",
        "Part 2.1 — Generate Matrices",
        "part2-1-generate-matrices.html",
    ),
    (
        "part2.2_transposing.html",
        "part2-2-transposing.html",
        "Part 2.2 — Transposing",
        "part2-2-transposing.html",
    ),
    (
        "part2.3_calculation with vectors_addition.html",
        "part2-3-matrix-addition.html",
        "Part 2.3 — Matrix Addition",
        "part2-3-matrix-addition.html",
    ),
    (
        "part2.4_calculation with vectors_multiplication.html",
        "part2-4-matrix-multiplication.html",
        "Part 2.4 — Matrix Multiplication",
        "part2-4-matrix-multiplication.html",
    ),
    (
        "part2.5_element-wise production.html",
        "part2-5-element-wise-product.html",
        "Part 2.5 — Element-wise Product",
        "part2-5-element-wise-product.html",
    ),
    (
        "part2.6_accessing elements in a matrix. html",
        "part2-6-accessing-matrix-elements.html",
        "Part 2.6 — Accessing Matrix Elements",
        "part2-6-accessing-matrix-elements.html",
    ),
]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for src_name, out_name, title, active in PAGES:
        src = SRC_DIR / src_name
        body = convert(src.read_text(encoding="utf-8"))
        page = wrap_page(body, title, module=4, active_href=active, page_heading=title)
        dst = OUT_DIR / out_name
        dst.write_text(page, encoding="utf-8")
        print(f"Wrote {dst}")


if __name__ == "__main__":
    main()
