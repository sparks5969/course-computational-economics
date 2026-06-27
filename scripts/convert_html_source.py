#!/usr/bin/env python3
"""
Convert a Canvas-exported HTML fragment into a styled site page.

Usage:
    python3 scripts/convert_html_source.py module1/part4_exp.html module1/new_source.html
"""
from __future__ import annotations

import html as html_mod
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]

IO_LABEL_RE = re.compile(r"^(in|out)\s*\[\d+\]\s*:?\s*$", re.IGNORECASE)

# ── helpers ──────────────────────────────────────────────────────────────────

def is_io_label(text: str) -> bool:
    return IO_LABEL_RE.match(text.replace("\xa0", " ").strip()) is not None


def peek_next_tag(children: list, start: int) -> int | None:
    j = start
    while j < len(children):
        if isinstance(children[j], NavigableString):
            j += 1
            continue
        if isinstance(children[j], Tag) and children[j].name == "br":
            j += 1
            continue
        return j
    return None


def collect_canvas_children(soup: BeautifulSoup) -> list:
    """Flatten Canvas wrapper/banner/custom blocks into a tag stream."""
    wrapper = soup.find("div", id=re.compile(r"kl_wrapper"))
    if not wrapper:
        root = soup.find("div", id="kl_banner") or soup
        return [c for c in root.children if isinstance(c, Tag) or str(c).strip()]

    tags: list = []
    for block in wrapper.children:
        if not isinstance(block, Tag):
            continue
        block_id = block.get("id", "")
        if block_id in ("kl_custom_block_0", "kl_custom_block_1"):
            continue
        if block_id == "kl_banner":
            h2 = block.find("h2")
            if h2 and "overview" in inner_text(h2).lower():
                continue
            tags.extend(block.children)
        else:
            tags.extend(block.children)
    return tags

def inner_text(tag: Tag) -> str:
    """Extract clean plain text from a tag, collapsing whitespace."""
    return re.sub(r"\s+", " ", tag.get_text(" ", strip=True)).strip()


def _collect_text(tag: Tag) -> str:
    """Recursively collect raw text from a tag, turning <br> into newlines."""
    parts: list[str] = []
    for child in tag.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            if child.name == "br":
                parts.append("\n")
            else:
                parts.append(_collect_text(child))
    return "".join(parts)


def extract_pre_code(tag: Tag) -> str:
    """
    Pull code text out of a <pre> (possibly wrapping <strong>/<span> nodes).
    Returns plain text with internal newlines preserved.
    """
    raw = _collect_text(tag)
    # Fix Canvas colour-picker artifact
    raw = raw.replace("rgba(64, 64, 64, 1)", "{")
    # Normalise: strip trailing spaces per line, collapse 3+ blank lines
    cleaned_lines = [ln.rstrip() for ln in raw.splitlines()]
    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def make_code_cell(label_text: str, code_text: str) -> str:
    """Produce the .code-cell div used by the site."""
    m = re.search(r"(in|out)\s*\[(\d+)\]", label_text, re.IGNORECASE)
    if m:
        prefix = "In" if m.group(1).lower() == "in" else "Out"
        num = m.group(2)
        label_html = f'<div class="code-label">{prefix} [{num}]:</div>'
        cell_cls = "code-input" if prefix == "In" else "code-output"
    else:
        label_html = f'<div class="code-label">{html_mod.escape(label_text)}</div>'
        cell_cls = "code-input"
    escaped = html_mod.escape(code_text)
    return (
        f'<div class="code-cell {cell_cls}">'
        f"{label_html}"
        f"<pre><code>{escaped}</code></pre>"
        f"</div>"
    )


def is_label_table(tag: Tag) -> bool:
    """True if this table is just an In[]/Out[] label."""
    if tag.name != "table":
        return False
    style = tag.get("style", "")
    text = inner_text(tag)
    return ("float: left" in style or "float:left" in style) and re.search(
        r"(In|Out)\s*\[\d+\]", text
    ) is not None


def is_code_table(tag: Tag) -> bool:
    """True if this table wraps a <pre> code block."""
    if tag.name != "table":
        return False
    return bool(tag.find("pre"))


def is_content_table(tag: Tag) -> bool:
    """True if this is a real data/content table (has visible border)."""
    if tag.name != "table":
        return False
    return tag.get("border", "0") not in ("", "0") or "border-color" not in tag.get(
        "style", ""
    )


def clean_content_table(tag: Tag) -> str:
    """Render a content table cleanly, stripping Canvas inline styles."""
    rows_html: list[str] = []
    for tr in tag.find_all("tr"):
        cells: list[str] = []
        for cell in tr.find_all(["td", "th"]):
            text = inner_text(cell)
            tag_name = "th" if cell.name == "th" else "td"
            cells.append(f"<{tag_name}>{html_mod.escape(text)}</{tag_name}>")
        if cells:
            rows_html.append(f"<tr>{''.join(cells)}</tr>")
    return f"<table>\n{''.join(rows_html)}\n</table>"


def clean_inline(tag: Tag) -> str:
    """
    Convert a <p> or list item to HTML, stripping Canvas colour/size spans
    but preserving <strong>, <em>, <code>, <a>.
    """
    keep = {"strong", "em", "code", "a", "br"}
    parts: list[str] = []
    for child in tag.children:
        if isinstance(child, NavigableString):
            parts.append(html_mod.escape(str(child)))
        elif isinstance(child, Tag):
            if child.name in keep:
                if child.name == "a":
                    href = child.get("href", "#")
                    parts.append(
                        f'<a href="{href}" target="_blank">'
                        f"{html_mod.escape(inner_text(child))}</a>"
                    )
                elif child.name == "br":
                    parts.append("<br>")
                else:
                    inner = clean_inline(child)
                    parts.append(f"<{child.name}>{inner}</{child.name}>")
            else:
                # strip tag, keep text
                parts.append(clean_inline(child))
    return "".join(parts)


# ── main conversion ───────────────────────────────────────────────────────────

def _attach_pre_code(
    children: list,
    i: int,
    label_text: str,
    skip_next: set[int],
    output_blocks: list[str],
) -> bool:
    j = peek_next_tag(children, i + 1)
    if j is None:
        return False
    nxt = children[j]
    if isinstance(nxt, Tag) and nxt.name == "pre":
        code_text = extract_pre_code(nxt)
        if code_text:
            output_blocks.append(make_code_cell(label_text, code_text))
            skip_next.add(id(nxt))
            return True
    if isinstance(nxt, Tag) and nxt.name == "div":
        pre = nxt.find("pre")
        if pre:
            code_text = extract_pre_code(pre)
            if code_text:
                output_blocks.append(make_code_cell(label_text, code_text))
                skip_next.add(id(nxt))
                return True
    if isinstance(nxt, Tag) and is_code_table(nxt):
        pre = nxt.find("pre")
        code_text = extract_pre_code(pre) if pre else ""
        if code_text:
            output_blocks.append(make_code_cell(label_text, code_text))
            skip_next.add(id(nxt))
            return True
    return False


def _skip_outline(children: list, i: int) -> int:
    while i < len(children):
        if isinstance(children[i], NavigableString):
            i += 1
            continue
        nxt = children[i]
        if nxt.name == "br":
            i += 1
            continue
        if nxt.name in ("ul", "ol"):
            i += 1
            continue
        if nxt.name == "p":
            txt = inner_text(nxt)
            if txt.startswith("==="):
                return i + 1
            i += 1
            continue
        break
    return i


def process_children(children: list, output_blocks: list[str], skip_next: set[int]) -> None:
    i = 0
    while i < len(children):
        tag = children[i]

        if not isinstance(tag, Tag):
            i += 1
            continue

        if id(tag) in skip_next:
            i += 1
            continue

        if tag.name == "img":
            i += 1
            continue
        if tag.name == "iframe":
            i += 1
            continue
        if tag.name == "p":
            txt = inner_text(tag)
            if not txt or txt in ("\xa0", "&nbsp;") or txt.startswith("==="):
                i += 1
                continue

        if tag.name in ("h1", "h2", "h3", "h4", "h5"):
            txt = inner_text(tag)
            if txt.lower() == "outline":
                i = _skip_outline(children, i + 1)
                continue
            if txt.lower() == "video instruction":
                i += 1
                while i < len(children):
                    if isinstance(children[i], NavigableString):
                        i += 1
                        continue
                    nxt = children[i]
                    if nxt.name in ("p", "iframe", "br"):
                        i += 1
                        continue
                    break
                continue
            level = {"h1": 2, "h2": 2, "h3": 2, "h4": 3, "h5": 3}.get(tag.name, 3)
            output_blocks.append(f"<h{level}>{html_mod.escape(txt)}</h{level}>")
            i += 1
            continue

        if tag.name in ("ul", "ol"):
            items = []
            for li in tag.find_all("li", recursive=False):
                items.append(f"<li>{clean_inline(li)}</li>")
            if items:
                output_blocks.append(f"<{tag.name}>{''.join(items)}</{tag.name}>")
            i += 1
            continue

        if tag.name == "table" and tag.get("border") == "1":
            output_blocks.append(clean_content_table(tag))
            i += 1
            continue

        if is_label_table(tag):
            label_text = inner_text(tag)
            j = i + 1
            while j < len(children) and isinstance(children[j], NavigableString):
                j += 1
            if j < len(children) and isinstance(children[j], Tag) and is_code_table(children[j]):
                pre = children[j].find("pre")
                code_text = extract_pre_code(pre) if pre else ""
                if code_text:
                    output_blocks.append(make_code_cell(label_text, code_text))
                skip_next.add(id(children[j]))
            i += 1
            continue

        if tag.name == "table" and is_code_table(tag):
            label_td = None
            for td in tag.find_all("td"):
                if re.search(r"(in|out)\s*\[\d+\]", inner_text(td), re.IGNORECASE):
                    label_td = td
                    break
            pre = tag.find("pre")
            if label_td and pre:
                output_blocks.append(
                    make_code_cell(inner_text(label_td), extract_pre_code(pre))
                )
            elif pre:
                code_text = extract_pre_code(pre)
                if code_text:
                    output_blocks.append(f"<pre><code>{html_mod.escape(code_text)}</code></pre>")
            i += 1
            continue

        if tag.name == "span" and is_io_label(inner_text(tag)):
            if _attach_pre_code(children, i, inner_text(tag), skip_next, output_blocks):
                i += 1
                continue

        if tag.name == "pre":
            code_text = extract_pre_code(tag)
            if code_text:
                output_blocks.append(
                    f'<div class="code-cell code-input"><pre><code>{html_mod.escape(code_text)}</code></pre></div>'
                )
            i += 1
            continue

        if tag.name == "p":
            txt = inner_text(tag)
            if is_io_label(txt):
                if _attach_pre_code(children, i, txt, skip_next, output_blocks):
                    i += 1
                    continue

            cleaned = clean_inline(tag)
            cleaned = re.sub(r"(&nbsp;|\xa0)+", " ", cleaned).strip()
            cleaned = re.sub(r"\s*=+\s*$", "", cleaned).strip()
            if cleaned:
                output_blocks.append(f"<p>{cleaned}</p>")
            i += 1
            continue

        if tag.name == "div":
            process_children(list(tag.children), output_blocks, skip_next)
            i += 1
            continue

        i += 1


def convert(src_html: str) -> str:
    soup = BeautifulSoup(src_html, "html.parser")
    output_blocks: list[str] = []
    skip_next: set[int] = set()
    process_children(collect_canvas_children(soup), output_blocks, skip_next)
    return "\n".join(output_blocks)


# ── site wrapper ──────────────────────────────────────────────────────────────

MODULE1_LECTURE = [
    ("index.html", "Overview"),
]

MODULE1_WORKSHOP = [
    ("part1-installation.html", "Part 1: Installation"),
    ("part2-language.html", "Part 2: Python Language"),
    ("part3-packages.html", "Part 3: Packages &amp; Modules"),
    ("part4-data-structures.html", "Part 4: Data Structures"),
    ("part5-programming.html", "Part 5: Programming"),
    ("practice1.html", "Practice Project 1"),
]

MODULE2_LECTURE = [
    ("index.html", "Overview"),
]

MODULE2_WORKSHOP = [
    ("part1-1-list-functions.html", "Part 1.1: List Functions"),
    ("part1-2-dict-functions.html", "Part 1.2: Dict Functions"),
    ("part2-logic-operators.html", "Part 2: Logic Operators"),
    ("part3-loops.html", "Part 3: Loops"),
    ("part4-json-comments.html", "Part 4 &amp; 5: JSON &amp; Comments"),
    ("practice2.html", "Practice Project 2"),
]

MODULE3_LECTURE = [
    ("index.html", "Overview"),
]

MODULE3_WORKSHOP = [
    ("part1-programming-paradigm.html", "Part 1: Programming Paradigm"),
    ("part2-1-2-functions.html", "Part 2.1–2.2: What &amp; Why Functions"),
    ("part2-user-functions.html", "Part 2.3: User-Defined Functions"),
    ("part3-1-class.html", "Part 3.1: Class"),
    ("part3-2-object.html", "Part 3.2: Object"),
    ("part3-3-inheritance.html", "Part 3.3: Inheritance"),
]

MODULE4_LECTURE = [
    ("index.html", "Overview"),
]

MODULE4_WORKSHOP: list[tuple[str, str]] = []

MODULE5_LECTURE = [
    ("index.html", "Overview"),
]

MODULE5_WORKSHOP: list[tuple[str, str]] = []

MODULE_META = {
    1: ("Module 1 — Python Foundations", MODULE1_LECTURE, MODULE1_WORKSHOP),
    2: ("Module 2 — Stable Matching", MODULE2_LECTURE, MODULE2_WORKSHOP),
    3: ("Module 3 — OOP & Functions", MODULE3_LECTURE, MODULE3_WORKSHOP),
    4: ("Module 4", MODULE4_LECTURE, MODULE4_WORKSHOP),
    5: ("Module 5", MODULE5_LECTURE, MODULE5_WORKSHOP),
}

MODULE_HUB = [
    (1, "Python Foundations", "Install Anaconda, learn Python basics, and complete Practice Project 1.", "module1/index.html", True),
    (2, "Stable Matching", "List and dictionary methods, loops, JSON, and the Gale–Shapley algorithm.", "module2/index.html", True),
    (3, "OOP & Functions", "Programming paradigms, user-defined functions, classes, objects, and inheritance.", "module3/index.html", True),
    (4, "Module 4", "Materials coming soon.", "module4/index.html", False),
    (5, "Module 5", "Materials coming soon.", "module5/index.html", False),
]


def _nested_section(
    sublabel: str,
    links: list[tuple[str, str]],
    active_href: str,
    *,
    indent: str = "        ",
) -> list[str]:
    lines = [
        f'{indent}<div class="sidebar-group">',
        f'{indent}  <div class="sidebar-sublabel">{sublabel}</div>',
        f'{indent}  <div class="sidebar-nested">',
    ]
    for href, label in links:
        cls = ' class="active"' if href == active_href else ""
        lines.append(f'{indent}    <a href="{href}"{cls}>{label}</a>')
    lines.extend([f"{indent}  </div>", f"{indent}</div>"])
    return lines


def _workshop_blocks(
    workshop: list[tuple[str, str]],
    active_href: str,
    link_prefix: str,
    indent: str,
) -> list[str]:
    if workshop:
        links = [(f"{link_prefix}{href}", label) for href, label in workshop]
        return _nested_section("Workshop", links, active_href, indent=indent)
    return [
        f"{indent}<div class=\"sidebar-group\">",
        f"{indent}  <div class=\"sidebar-sublabel\">Workshop</div>",
        f"{indent}  <div class=\"sidebar-nested\">",
        f"{indent}    <span class=\"sidebar-muted\">Coming soon</span>",
        f"{indent}  </div>",
        f"{indent}</div>",
    ]


def _module_fold(
    num: int,
    active_href: str,
    *,
    open: bool,
    link_prefix: str,
    indent: str = "        ",
) -> list[str]:
    _, lecture, workshop = MODULE_META[num]
    open_attr = " open" if open else ""
    i = indent + "  "
    lines = [
        f'{indent}<details class="sidebar-fold"{open_attr}>',
        f'{indent}  <summary class="sidebar-fold-title">Module {num}</summary>',
        f'{indent}  <div class="sidebar-fold-body">',
    ]
    all_links = [
        (f"{link_prefix}{href}", label)
        for href, label in (lecture + workshop)
    ]
    for href, label in all_links:
        cls = ' class="active"' if href == active_href else ""
        lines.append(f'{i}  <a href="{href}"{cls}>{label}</a>')
    if not all_links:
        lines.append(f'{i}  <span class="sidebar-muted">Coming soon</span>')
    lines.extend([f"{indent}  </div>", f"{indent}</details>"])
    return lines


def sidebar_html(module: int, active_href: str) -> str:
    lines = [
        '        <div class="sidebar-label">Course</div>',
        '        <a href="../index.html">Home</a>',
    ]
    for num in MODULE_META:
        prefix = "" if num == module else f"../module{num}/"
        lines.extend(
            _module_fold(num, active_href, open=(num == module), link_prefix=prefix)
        )
    return "\n".join(lines)


def home_sidebar_html(active_href: str = "index.html") -> str:
    """Sidebar for the course home page — all modules, nested."""
    home_cls = ' class="active"' if active_href == "index.html" else ""
    lines = [
        '        <div class="sidebar-label">Course</div>',
        f'        <a href="index.html"{home_cls}>Home</a>',
    ]
    for num in MODULE_META:
        lines.extend(
            _module_fold(
                num,
                active_href,
                open=False,
                link_prefix=f"module{num}/",
            )
        )
    return "\n".join(lines)


def home_body_html() -> str:
    cards: list[str] = []
    for num, title, desc, href, live in MODULE_HUB:
        if live:
            cards.append(
                f'          <a class="card" href="{href}">\n'
                f'            <div class="card-step">Module {num}</div>\n'
                f"            <h3>{html_mod.escape(title)}</h3>\n"
                f"            <p>{html_mod.escape(desc)}</p>\n"
                f"          </a>"
            )
        else:
            cards.append(
                f'          <div class="card card-soon">\n'
                f'            <div class="card-step">Module {num}</div>\n'
                f"            <h3>{html_mod.escape(title)}</h3>\n"
                f"            <p>{html_mod.escape(desc)}</p>\n"
                f"          </div>"
            )
    return f"""
      <section class="hero">
        <h1>Computational Economics</h1>
        <p>
          Select a module below. Each module has a <strong>Lecture</strong> overview
          and a <strong>Workshop</strong> with hands-on parts and practice projects.
        </p>
      </section>

      <section>
        <h2>Course Modules</h2>
        <div class="card-grid">
{chr(10).join(cards)}
        </div>
      </section>"""


def wrap_home_page(body_html: str) -> str:
    sidebar = home_sidebar_html()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Computational Economics</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="site-header-inner">
      <div>
        <h1 class="site-title"><a href="index.html">Computational Economics</a></h1>
        <p class="site-subtitle">Course materials</p>
      </div>
    </div>
  </header>
  <div class="layout">
    <aside class="sidebar">
      <nav>
{sidebar}
      </nav>
    </aside>
    <main>
{body_html}
    </main>
  </div>
  <footer class="site-footer">Computational Economics</footer>
</body>
</html>"""


def wrap_page(
    body_html: str,
    title: str,
    *,
    module: int = 1,
    active_href: str = "",
    page_heading: str | None = None,
) -> str:
    subtitle, _, _ = MODULE_META[module]
    sidebar = sidebar_html(module, active_href)
    heading = page_heading or title
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_mod.escape(title)}</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      document.querySelectorAll('pre code').forEach(function(block) {{
        if (!block.className) block.className = 'language-python';
        hljs.highlightElement(block);
        var btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.addEventListener('click', function() {{
          navigator.clipboard.writeText(block.innerText).then(function() {{
            btn.textContent = 'Copied!';
            setTimeout(function() {{ btn.textContent = 'Copy'; }}, 1500);
          }});
        }});
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(btn);
      }});
    }});
  </script>
</head>
<body>
  <header class="site-header">
    <div class="site-header-inner">
      <div>
        <h1 class="site-title"><a href="../index.html">Computational Economics</a></h1>
        <p class="site-subtitle">{html_mod.escape(subtitle)}</p>
      </div>
    </div>
  </header>
  <div class="layout">
    <aside class="sidebar">
      <nav>
{sidebar}
      </nav>
    </aside>
    <main>
      <h1>{html_mod.escape(heading)}</h1>
{body_html}
    </main>
  </div>
</body>
</html>"""


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Convert Canvas HTML to site page")
    parser.add_argument("src", nargs="?", help="Source Canvas HTML file")
    parser.add_argument("dst", nargs="?", help="Output site HTML file")
    parser.add_argument("--title", default="Course Page", help="Browser title")
    parser.add_argument("--heading", default=None, help="Page h1 (defaults to title)")
    parser.add_argument("--module", type=int, default=1, choices=(1, 2, 3, 4, 5))
    parser.add_argument("--active", default="", help="Active sidebar href")
    args = parser.parse_args()

    src = Path(args.src) if args.src else ROOT / "module1/part4_exp.html"
    dst = Path(args.dst) if args.dst else ROOT / "module1/new_source.html"

    src_html = src.read_text(encoding="utf-8")
    body = convert(src_html)
    page = wrap_page(
        body,
        args.title,
        module=args.module,
        active_href=args.active,
        page_heading=args.heading,
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()
