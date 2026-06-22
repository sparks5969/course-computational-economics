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

# ── helpers ──────────────────────────────────────────────────────────────────

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
    is_input = "In" in label_text
    cell_cls = "code-input" if is_input else "code-output"
    # parse label number
    m = re.search(r"\[(\d+)\]", label_text)
    num = m.group(1) if m else "1"
    prefix = "In" if is_input else "Out"
    label_html = f'<div class="code-label">{prefix} [{num}]:</div>'
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

def convert(src_html: str) -> str:
    soup = BeautifulSoup(src_html, "html.parser")

    # Remove the outer Canvas wrapper divs we don't need, work on their children
    root = soup.find("div", id="kl_banner") or soup

    output_blocks: list[str] = []
    skip_next: set[int] = set()

    children = list(root.children)

    i = 0
    while i < len(children):
        tag = children[i]

        if id(tag) in skip_next:
            i += 1
            continue

        # ── NavigableString (whitespace / stray text) ──
        if isinstance(tag, NavigableString):
            text = str(tag).strip()
            if text and text not in ("&nbsp;", "\xa0"):
                output_blocks.append(f"<p>{html_mod.escape(text)}</p>")
            i += 1
            continue

        # ── Skip: images, iframes, horizontal-rule paragraphs, &nbsp; paras ──
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

        # ── Headings ──
        if tag.name in ("h1", "h2", "h3", "h4", "h5"):
            txt = inner_text(tag)
            # Skip generic outline/video headings
            if txt.lower() in ("outline", "video instruction"):
                i += 1
                continue
            # Map h3 → h2, h4 → h3 for site hierarchy
            level = {"h1": 2, "h2": 2, "h3": 2, "h4": 3, "h5": 3}.get(tag.name, 3)
            output_blocks.append(f"<h{level}>{html_mod.escape(txt)}</h{level}>")
            i += 1
            continue

        # ── Unordered / ordered lists ──
        if tag.name in ("ul", "ol"):
            items = []
            for li in tag.find_all("li", recursive=False):
                items.append(f"<li>{clean_inline(li)}</li>")
            if items:
                list_tag = tag.name
                output_blocks.append(
                    f"<{list_tag}>{''.join(items)}</{list_tag}>"
                )
            i += 1
            continue

        # ── Content table (border="1", data table) ──
        if tag.name == "table" and tag.get("border") == "1":
            output_blocks.append(clean_content_table(tag))
            i += 1
            continue

        # ── In[]/Out[] label table followed by code table ──
        if is_label_table(tag):
            label_text = inner_text(tag)
            # find the next sibling that is a code table
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

        # ── Standalone code table (code appears without a separate label row) ──
        if tag.name == "table" and is_code_table(tag):
            # Check if table itself has a label + pre in same structure
            label_td = None
            for td in tag.find_all("td"):
                if re.search(r"(In|Out)\s*\[\d+\]", inner_text(td)):
                    label_td = td
                    break
            pre = tag.find("pre")
            if label_td and pre:
                label_text = inner_text(label_td)
                code_text = extract_pre_code(pre)
                if code_text:
                    output_blocks.append(make_code_cell(label_text, code_text))
            elif pre:
                code_text = extract_pre_code(pre)
                if code_text:
                    output_blocks.append(f"<pre><code>{html_mod.escape(code_text)}</code></pre>")
            i += 1
            continue

        # ── Paragraph with inline In[]/Out[] label ──
        if tag.name == "p":
            txt = inner_text(tag)
            # If the para contains ONLY an In/Out label, peek ahead for code
            label_match = re.match(r"^(In|Out)\s*\[\d+\]:?\s*$", txt.replace("\xa0", "").strip())
            if label_match:
                j = i + 1
                while j < len(children) and isinstance(children[j], NavigableString):
                    j += 1
                if j < len(children) and isinstance(children[j], Tag) and is_code_table(children[j]):
                    pre = children[j].find("pre")
                    code_text = extract_pre_code(pre) if pre else ""
                    if code_text:
                        output_blocks.append(make_code_cell(txt, code_text))
                        skip_next.add(id(children[j]))
                        i += 1
                        continue

            # Regular paragraph
            cleaned = clean_inline(tag)
            cleaned = re.sub(r"(&nbsp;|\xa0)+", " ", cleaned).strip()
            if cleaned:
                output_blocks.append(f"<p>{cleaned}</p>")
            i += 1
            continue

        # ── Other block-level tags: div etc. ──
        if tag.name == "div":
            # Recurse into divs that hold more content
            inner_html = convert(str(tag))
            if inner_html.strip():
                output_blocks.append(inner_html)
            i += 1
            continue

        i += 1

    return "\n".join(output_blocks)


# ── site wrapper ──────────────────────────────────────────────────────────────

SIDEBAR = """
        <div class="sidebar-label">Module 1</div>
        <a href="../index.html">Overview</a>
        <a href="part1-installation.html">Part 1: Installation</a>
        <a href="part2-language.html">Part 2: Python Language</a>
        <a href="part3-packages.html">Part 3: Packages &amp; Modules</a>
        <a href="part4-data-structures.html" class="active">Part 4: Data Structures</a>
        <a href="part5-programming.html">Part 5: Programming</a>
"""


def wrap_page(body_html: str, title: str) -> str:
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
        <p class="site-subtitle">Module 1 — Python Foundations</p>
      </div>
    </div>
  </header>
  <div class="layout">
    <aside class="sidebar">
      <nav>
{SIDEBAR}
      </nav>
    </aside>
    <main>
      <h1>{html_mod.escape(title)}</h1>
{body_html}
    </main>
  </div>
</body>
</html>"""


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "module1/part4_exp.html"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "module1/new_source.html"

    src_html = src.read_text(encoding="utf-8")
    body = convert(src_html)
    page = wrap_page(body, "Part 4. Data Structures in Python")
    dst.write_text(page, encoding="utf-8")
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()
