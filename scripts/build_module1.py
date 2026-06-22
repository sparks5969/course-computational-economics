#!/usr/bin/env python3
"""Generate Module 1 HTML pages from module1-content.md."""

from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "module1-content.md"
OUT_DIR = ROOT / "module1"

PARTS = [
    {
        "slug": "part1-installation",
        "title": "Part 1. Installation of Python and Anaconda",
        "nav": "Part 1: Installation",
        "start": "**Part 1. Installation**",
        "end": "Part 2. The Python programming language",
    },
    {
        "slug": "part2-language",
        "title": "Part 2. The Python Programming Language",
        "nav": "Part 2: Python Language",
        "start": "**Part 2. The Python Programming Language**",
        "end": "Part 3. Python modules and packages",
    },
    {
        "slug": "part3-packages",
        "title": "Part 3. Python Packages and Modules",
        "nav": "Part 3: Packages & Modules",
        "start": "**Part 3. Python Packages and Modules**",
        "end": "Part 4. Data structures in python",
    },
    {
        "slug": "part4-data-structures",
        "title": "Part 4. Data Structures in Python",
        "nav": "Part 4: Data Structures",
        "start": "**Part 4. Data Structures in Python**",
        "end": "Part 5. Some basic programming techniques",
    },
    {
        "slug": "part5-programming",
        "title": "Part 5. Basic Programming Techniques",
        "nav": "Part 5: Programming",
        "start": "**Part 5. Some Basic Programming Techniques**",
        "end": None,
    },
]

SIDEBAR = """
        <div class="sidebar-label">Module 1</div>
        <a href="../index.html">Overview</a>
        <a href="part1-installation.html"{p1}>Part 1: Installation</a>
        <a href="part2-language.html"{p2}>Part 2: Python Language</a>
        <a href="part3-packages.html"{p3}>Part 3: Packages &amp; Modules</a>
        <a href="part4-data-structures.html"{p4}>Part 4: Data Structures</a>
        <a href="part5-programming.html"{p5}>Part 5: Programming</a>
"""


def load_markdown() -> str:
    return MD_PATH.read_text(encoding="utf-8")


def extract_section(text: str, start: str, end: str | None) -> str:
    match = re.search(re.escape(start), text)
    if not match:
        raise ValueError(f"Could not find section start: {start}")
    start_idx = match.start()
    if end:
        end_match = re.search(re.escape(end), text[start_idx + len(start) :])
        if not end_match:
            raise ValueError(f"Could not find section end: {end}")
        end_idx = start_idx + len(start) + end_match.start()
        return text[start_idx:end_idx]
    return text[start_idx:]


def clean_markdown(section: str) -> str:
    section = re.sub(r"^\*\*Part \d+\.[^\n]*\*\*\s*\n", "", section, count=1)
    section = re.sub(r"={10,}", "", section)
    section = re.sub(
        r"from:\s*\[\[https://www\.anaconda\.com/products/individual[^\]]*\]\([^\)]+\)\]",
        "from [Anaconda Individual Edition](https://www.anaconda.com/download)",
        section,
    )
    section = re.sub(
        r"\[https://www\.anaconda\.com/products/individual[^\]]*Links to an external site\.\]",
        "Anaconda Individual Edition",
        section,
    )
    section = re.sub(r"\[please follow these simple steps and use\s*Spyder as your IDE\]", "please follow these simple steps and use Spyder as your IDE", section)
    section = re.sub(r"\[machine languages\s*\]", "machine languages", section)
    section = re.sub(
        r"\[\[check here[^\]]*\]\([^\)]+\)\]",
        "[check here](https://www.w3schools.com/python/python_ref_string.asp)",
        section,
    )
    section = re.sub(r"\[Links to an external site\.\]\{\.underline\}", "", section)
    section = re.sub(r"\{\.underline\}", "", section)
    section = re.sub(r"\\'", "'", section)
    section = re.sub(r'\\"', '"', section)
    section = re.sub(r"\\>", ">", section)
    section = re.sub(r"\\<", "<", section)
    section = re.sub(r"\\#", "#", section)
    section = re.sub(r"\\\*", "*", section)
    section = re.sub(r"\\\[", "[", section)
    section = re.sub(r"\\\]", "]", section)
    section = re.sub(r"\\,", ",", section)
    section = re.sub(r"\\ ", " ", section)
    section = re.sub(r"^\+[-=]+\+\s*$", "", section, flags=re.MULTILINE)
    section = re.sub(r"^\|\s*[-=]+\s*\|\s*$", "", section, flags=re.MULTILINE)
    section = section.replace(
        "gradebook = rgba(64, 64, 64, 1)",
        "gradebook = {",
    )
    # Replace the Word-style Notation comparison table with a clean markdown pipe table
    section = re.sub(
        r"\s*-{10,}\s*\n\s*\*?\*?Notation\*?\*?[\s\S]{100,1500}?undead[^\n]{0,10}\n\s*-{10,}",
        "\n\n| Notation | Ordered | Changeable | Allow Duplicates | Example |\n"
        "|----------|---------|------------|------------------|--------|\n"
        "| `[ ]` List | Yes | Yes | Yes | `[human, bat, orc, human, elf, undead, orc]` |\n"
        "| `( )` Tuple | Yes | No | Yes | `(human, bat, orc, human, elf, undead, orc)` |\n"
        "| `{ }` Set | No | No | No | `{elf, human, bat, orc, undead}` |\n\n",
        section,
        flags=re.DOTALL,
    )
    # Replace the Word-style Key/Value dictionary table with a clean markdown pipe table
    section = re.sub(
        r"\s*-{10,}\s*\n\s*\*?\*?Key\*?\*?[\s\S]{0,300}?archer[\s\S]{0,40}?-{10,}",
        "\n\n| Key | Value |\n"
        "|-----|-------|\n"
        '| `"human"` | `"cavalier"` |\n'
        '| `"bat"` | `"vampire"` |\n'
        '| `"orc"` | `"warrior"` |\n'
        '| `"elf"` | `"archer"` |\n\n',
        section,
        flags=re.DOTALL,
    )
    # Replace the Word-style comparison operators table with a clean markdown pipe table
    section = re.sub(
        r"\s*-{70,}\s*\n\s*\*?\*?Operator\*?\*?[\s\S]{100,5000}?\n\s*-{70,}",
        "\n\n| Operator | Description |\n"
        "|----------|-------------|\n"
        "| `==` | Equal: condition is true if both operands are equal |\n"
        "| `!=` | Not equal: condition is true if operands are not equal |\n"
        "| `>` | Greater than: condition is true if left operand is greater than right |\n"
        "| `<` | Less than: condition is true if left operand is less than right |\n"
        "| `>=` | Greater than or equal to |\n"
        "| `<=` | Less than or equal to |\n\n",
        section,
        flags=re.DOTALL,
    )
    section = section.replace("spider", "Spyder")
    section = section.replace("PTYHON", "PYTHON")
    section = section.replace("need o first", "need to first")
    section = section.replace("agin.", "again.")
    section = section.replace("machine languagesor", "machine languages or")
    section = convert_md_code_boxes(section)
    section = convert_boxed_code(section)
    section = strip_trailing_outline(section)
    # Only remove pure-dash lines (no spaces in the middle) so pandoc table separators survive
    section = re.sub(r"^\s*-{10,}\s*$", "", section, flags=re.MULTILINE)
    section = re.sub(r"\n{3,}", "\n\n", section)
    return section.strip()


def convert_md_code_boxes(section: str) -> str:
    """Convert Word-style bold code boxes into proper fenced code blocks.

    The Word→pandoc pipeline produces this structure in the markdown:
        ----
        **In [N]: **
        ----
        ----
        **code line1\\
        code line2\\
        ...**
        ----

    We do two passes:
    Pass 1 – collapse label dash-boxes to bare bold labels.
    Pass 2 – convert code dash-boxes to fenced code blocks.
    """

    # Pass 1: collapse "----\n**In [N]: **\n----" → "\n**In [N]:**\n"
    section = re.sub(
        r"\s*-{10,}\s*\n\s*(\*\*(?:In|Out)\s*\[\d+\]:?\s*\*\*)\s*\n\s*-{10,}\s*\n",
        r"\n\1\n",
        section,
        flags=re.MULTILINE,
    )

    # Pass 2: convert remaining "----\n**code**\n----" to fenced blocks
    def extract_lines(bold_block: str) -> str:
        content = re.sub(r"^\*\*|\*\*\s*$", "", bold_block.strip())
        lines = []
        for raw in content.split("\\\n"):
            raw = raw.rstrip("\\").rstrip()
            # Strip the 2-space Word block indent; preserve additional indent
            if raw.startswith("  "):
                raw = raw[2:]
            # Strip any remaining ** bold markers (from per-line-bold format)
            raw = raw.replace("**", "")
            # Replace non-breaking spaces (from Word) with regular spaces
            raw = raw.replace("\xa0", " ")
            lines.append(raw)
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(lines)

    def repl_code_box(m: re.Match[str]) -> str:
        bold = m.group(1)
        # Only convert if it uses backslash-newline continuations (Word code format).
        # Prose tables (operators table, etc.) have actual \n\n blank lines between
        # entries but no \\\n continuations; code boxes use \\\n, not \n\n.
        if "\\\n" not in bold or "\n\n" in bold:
            return m.group(0)
        if not re.search(r"[a-zA-Z0-9_(=]", bold):
            return "\n"
        code = extract_lines(bold)
        if not code.strip():
            return "\n"
        return f"\n```python\n{code}\n```\n\n"

    section = re.sub(
        r"(?:\s*-{10,}\s*\n)+\s*(\*\*[\s\S]+?\*\*)\s*\n(?:\s*-{10,}\s*\n)+",
        repl_code_box,
        section,
        flags=re.MULTILINE,
    )

    return section


def strip_trailing_outline(section: str) -> str:
    return re.sub(r"\nPart \d+\.[^\n]*\n(?:\*\*Outline\*\*\n)?(?:- .+\n)+", "\n", section)


def convert_boxed_code(section: str) -> str:
    """Convert Word/pandoc code box artifacts into fenced code blocks."""

    def repl(match: re.Match[str]) -> str:
        code = match.group(1)
        code = re.sub(r"\*\*", "", code)
        code = code.replace("\\", "")
        code = re.sub(r"\n{3,}", "\n\n", code.strip())
        if not code:
            return ""
        return f"\n```python\n{code}\n```\n"

    section = re.sub(
        r"(?:^|\n)(?:[- ]{10,}\n)+((?:\*\*[^\n]+\*\*(?:\\?\n|\n)?)+?)(?:\n(?:[- ]{10,}\n))+",
        repl,
        section,
        flags=re.MULTILINE,
    )

    def inline_repl(match: re.Match[str]) -> str:
        lines = []
        for line in match.group(0).splitlines():
            line = re.sub(r"^\*\*|\*\*$", "", line.strip())
            line = line.replace("\\", "")
            if line and not re.match(r"^In \[\\?\d+\]:?$", line) and not re.match(r"^Out \[\\?\d+\]:?$", line):
                lines.append(line)
        if not lines:
            return match.group(0)
        return "\n```python\n" + "\n".join(lines) + "\n```\n"

    section = re.sub(
        r"(?:^\*\*In \[\\?\d+\]:\*\*\s*\n(?:\*\*[^\n]+\*\*(?:\\?\n|\n)?)+)+",
        inline_repl,
        section,
        flags=re.MULTILINE,
    )
    section = re.sub(
        r"^\*\*Out \[\\?\d+\]:\*\*\s*\n(?:\*\*[^\n]+\*\*(?:\\?\n|\n)?)+",
        lambda m: "\n```\n" + re.sub(r"\*\*", "", m.group(0)).replace("Out [1]:", "").replace("Out [2]:", "").strip() + "\n```\n",
        section,
        flags=re.MULTILINE,
    )
    section = re.sub(
        r"^\*\*In\[\\?\d+\]\*\*\s*\n(?:\*\*[^\n]+\*\*(?:\\?\n|\n)?)+",
        inline_repl,
        section,
        flags=re.MULTILINE,
    )
    return section


def markdown_to_html(md: str) -> str:
    proc = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html", "--wrap=none", "--no-highlight"],
        input=md,
        text=True,
        capture_output=True,
        check=True,
    )
    body = proc.stdout.strip()
    body = re.sub(r"<p>\s*</p>", "", body)
    body = re.sub(r"<p>\s*&nbsp;\s*</p>", "", body)
    body = postprocess_html(body)
    return body


def _data_type_table(body: str) -> str:
    """Replace the List/Tuple/Set comparison pre/code block with a proper table."""
    pattern = re.compile(
        r'<pre><code>\s*\*?\*?Notation\*?\*?[\s\S]{20,400}?Duplicates[\s\S]{0,30}?</code></pre>',
        re.DOTALL,
    )
    if not pattern.search(body):
        return body
    table = (
        "<table>\n"
        "<thead><tr>"
        "<th>Notation</th><th>Ordered</th><th>Changeable</th>"
        "<th>Allow Duplicates</th><th>Example</th>"
        "</tr></thead>\n"
        "<tbody>\n"
        "<tr><td><code>[ ]</code> List</td><td>Yes</td><td>Yes</td><td>Yes</td>"
        "<td><code>[human, bat, orc, human, elf, undead, orc]</code></td></tr>\n"
        "<tr><td><code>( )</code> Tuple</td><td>Yes</td><td>No</td><td>Yes</td>"
        "<td><code>(human, bat, orc, human, elf, undead, orc)</code></td></tr>\n"
        "<tr><td><code>{ }</code> Set</td><td>No</td><td>No</td><td>No</td>"
        "<td><code>{elf, human, bat, orc, undead}</code></td></tr>\n"
        "</tbody>\n</table>"
    )
    # Also remove the stray text paragraphs for List/Tuple/Set rows that pandoc made
    body = pattern.sub(table, body)
    body = re.sub(
        r"<p>(?:List|Tuple|Set)\s+[\[\(\{].*?[\]\)\}]\s+(?:Yes|No)[\s\S]{0,200}?</p>",
        "",
        body,
    )
    return body


def _dict_kv_table(body: str) -> str:
    """Replace the Key/Value dictionary pre/code block with a proper table."""
    pattern = re.compile(
        r'<pre><code>\s*\*?\*?Key\*?\*?[\s\S]{0,300}?archer[\s\S]{0,30}?</code></pre>',
        re.DOTALL,
    )
    if not pattern.search(body):
        return body
    table = (
        "<table>\n"
        "<thead><tr><th>Key</th><th>Value</th></tr></thead>\n"
        "<tbody>\n"
        '<tr><td><code>"human"</code></td><td><code>"cavalier"</code></td></tr>\n'
        '<tr><td><code>"bat"</code></td><td><code>"vampire"</code></td></tr>\n'
        '<tr><td><code>"orc"</code></td><td><code>"warrior"</code></td></tr>\n'
        '<tr><td><code>"elf"</code></td><td><code>"archer"</code></td></tr>\n'
        "</tbody>\n</table>"
    )
    return pattern.sub(table, body)


def postprocess_html(body: str) -> str:
    # Normalize pandoc fenced-block markup (<pre class="python">) to plain <pre><code>
    body = re.sub(r'<pre class="[^"]*">', "<pre>", body)
    body = re.sub(r'<code class="[^"]*">', "<code>", body)

    body = re.sub(
        r'<a href="https://www\.anaconda\.com/products/individual[^"]*">\[[^\]]+\]</a>',
        '<a href="https://www.anaconda.com/download">Anaconda Individual Edition</a>',
        body,
    )
    body = re.sub(
        r"\[please follow these simple steps and use\s*Spyder as your IDE\]",
        "please follow these simple steps and use Spyder as your IDE",
        body,
    )

    # Extract inline In[]/Out[] labels that appear at the END of a paragraph
    # e.g. <p>...such as: <strong>In [1]: </strong></p>  →  split into two elements
    body = re.sub(
        r'<p>([\s\S]*?)\s*<strong>((?:In|Out)\s*\[\d+\]:?\s*(?:\xa0)?)</strong></p>',
        lambda m: (
            f'<p>{m.group(1).strip()}</p>\n'
            f'<p><strong>{m.group(2).strip()}</strong></p>'
        ) if m.group(1).strip() else f'<p><strong>{m.group(2).strip()}</strong></p>',
        body,
    )

    # Per-line bold code: <p><strong>line1</strong><br/><strong>line2</strong>...</p>
    # where the bold content looks like code (variable assignments)
    def bold_lines_to_code(m: re.Match[str]) -> str:
        inner = m.group(1)
        text = re.sub(r"<br\s*/?>", "\n", inner)
        text = re.sub(r"</?strong>", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text).strip()
        return f"<pre><code>{html.escape(text)}</code></pre>"

    body = re.sub(
        r'<p>(<strong>[^<>]*</strong>(?:<br\s*/?>[\s\n]*<strong>[^<>]*</strong>)+)</p>',
        bold_lines_to_code,
        body,
    )

    def extract_bold_code(paragraphs: list[str]) -> str:
        lines: list[str] = []
        for para in paragraphs:
            text = re.sub(r"</?strong>", "", para)
            text = re.sub(r"<br\s*/?>", "\n", text)
            text = re.sub(r"<[^>]+>", "", text)
            for line in text.splitlines():
                line = line.strip()
                if line:
                    lines.append(line)
        return html.escape("\n".join(lines))

    def repl_in(match: re.Match[str]) -> str:
        num = match.group(1)
        paras = re.findall(r"<p><strong>(.*?)</strong></p>", match.group(2), flags=re.DOTALL)
        code = extract_bold_code(paras)
        return (
            f'<div class="code-cell code-input">'
            f'<div class="code-label">In [{num}]:</div>'
            f"<pre><code>{code}</code></pre></div>"
        )

    body = re.sub(
        r'<p><strong>In \[(\d+)\]:\s*</strong></p>\s*((?:<p><strong>[\s\S]*?</strong></p>\s*)+)',
        repl_in,
        body,
    )

    def repl_out(match: re.Match[str]) -> str:
        num = match.group(1)
        paras = re.findall(r"<p><strong>(.*?)</strong></p>", match.group(2), flags=re.DOTALL)
        code = extract_bold_code(paras)
        return (
            f'<div class="code-cell code-output">'
            f'<div class="code-label">Out [{num}]:</div>'
            f"<pre><code>{code}</code></pre></div>"
        )

    body = re.sub(
        r'<p><strong>Out \[(\d+)\]:\s*</strong></p>\s*((?:<p><strong>[\s\S]*?</strong></p>\s*)+)',
        repl_out,
        body,
    )

    body = re.sub(
        r"<p>(hrbook=\s*\{[\s\S]*?\})</p>",
        lambda m: f"<pre><code>{html.escape(re.sub(r'<br\s*/?>', chr(10), m.group(1)))}</code></pre>",
        body,
    )

    # Section sub-headings: **4.1. Foo** / **5.1. Foo** → <h3>
    body = re.sub(
        r"<p><strong>(\d+\.\d+\.?\d*\.?\s[^<*]{3,60}?)\s*</strong></p>",
        r"<h3>\1</h3>",
        body,
    )

    # Convert line-block divs (Word table code cells) into plain code blocks
    def lineblock_to_code(match: re.Match[str]) -> str:
        content = match.group(1)
        text = re.sub(r"<br\s*/?>", "\n", content)
        text = re.sub(r"</?strong>", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
        lines = []
        for line in text.splitlines():
            line = line.strip().rstrip("|").rstrip().lstrip("|").strip()
            if line:
                lines.append(line)
        return (f'<pre><code>{html.escape(chr(10).join(lines))}</code></pre>' if lines else "")

    body = re.sub(r'<div class="line-block">(.*?)</div>', lineblock_to_code, body, flags=re.DOTALL)

    # Remove ++ artefacts, empty code blocks, merge adjacent ones
    body = re.sub(r"<p>\+\+</p>", "", body)
    body = re.sub(r"<pre><code>\s*</code></pre>", "", body)
    body = re.sub(r"</code></pre>\s*<pre><code>", "\n", body)

    # Strip ** and fix double-escaped HTML entities inside all code blocks
    def clean_code_block(match: re.Match[str]) -> str:
        c = match.group(1)
        c = re.sub(r"\*\*", "", c)
        c = c.replace("&amp;lt;", "&lt;").replace("&amp;gt;", "&gt;").replace("&amp;amp;", "&amp;")
        return f"<pre><code>{c}</code></pre>"

    body = re.sub(r"<pre><code>(.*?)</code></pre>", clean_code_block, body, flags=re.DOTALL)

    # Normalize In[N] (no space/colon) → In [N]:
    body = re.sub(r'<p><strong>In\[(\d+)\]\s*</strong></p>', r'<p><strong>In [\1]: </strong></p>', body)

    # Wrap orphaned In[]/Out[] bold labels that precede a bare <pre><code>
    body = re.sub(
        r'<p><strong>In\s*\[(\d+)\]:?\s*</strong></p>\s*(<pre><code>[\s\S]*?</code></pre>)',
        lambda m: (
            f'<div class="code-cell code-input">'
            f'<div class="code-label">In [{m.group(1)}]:</div>'
            f'{m.group(2)}</div>'
        ),
        body,
    )
    body = re.sub(
        r'<p><strong>Out\s*\[(\d+)\]:?\s*</strong></p>\s*(<pre><code>[\s\S]*?</code></pre>)',
        lambda m: (
            f'<div class="code-cell code-output">'
            f'<div class="code-label">Out [{m.group(1)}]:</div>'
            f'{m.group(2)}</div>'
        ),
        body,
    )

    # Remove any remaining orphaned In[]/Out[] labels that couldn't be wrapped
    body = re.sub(r'<p><strong>(?:In|Out)\s*\[\d+\]:?\s*</strong></p>', "", body)

    # Bold syntax blocks (if/elif/else, while, for templates) → code blocks
    def bold_syntax_to_code(match: re.Match[str]) -> str:
        inner = match.group(1)
        # Replace <br /> then collapse the literal newline that follows it
        text = re.sub(r"<br\s*/?>\s*\n?", "\n", inner)
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text).strip()
        # Collapse any accidental double blank lines
        text = re.sub(r"\n{2,}", "\n", text)
        # Auto-indent branch lines that follow a keyword header ending with ':'
        header_pat = re.compile(r"^\s*(if|elif|else|while|for)\b.*:\s*$")
        lines = text.splitlines()
        out: list[str] = []
        for i, line in enumerate(lines):
            if out and header_pat.match(out[-1]) and not header_pat.match(line) and line.strip():
                out.append("    " + line.lstrip())
            else:
                out.append(line)
        return f"<pre><code>{html.escape(chr(10).join(out))}</code></pre>"

    body = re.sub(
        r'<p><strong>((?:if|elif|else|while|for)\s[^<]*?<br\s*/?>[\s\S]{5,600}?)</strong></p>',
        bold_syntax_to_code,
        body,
    )

    # Remove duplicate consecutive identical code blocks
    body = re.sub(
        r'(<pre><code>[^<]{5,}?</code></pre>)\s*\1',
        r'\1',
        body,
        flags=re.DOTALL,
    )

    # Strip section-title lines and stray Out[]/True lines swallowed into code blocks
    def strip_noise_from_code(match: re.Match[str]) -> str:
        content = match.group(1)
        lines = content.split("\n")
        cleaned = []
        for l in lines:
            if re.match(r"^\d+\.\d+\.?\s+\w", l):
                continue
            if re.match(r"^Out\s*\[\d+\]:\s*$", l):
                continue
            cleaned.append(l)
        return f"<pre><code>{chr(10).join(cleaned)}</code></pre>"

    body = re.sub(r"<pre><code>([\s\S]*?)</code></pre>", strip_noise_from_code, body)

    # Wrap remaining bold code paragraphs that weren't caught (e.g. In[1] with no label)
    body = re.sub(
        r'<p><strong>((?:a|x|y|output|students|gradebook|current_price|grade\w*)\s*=[\s\S]{5,300}?)</strong></p>',
        lambda m: (
            '<pre><code>'
            + html.escape(html.unescape(re.sub(r"<br\s*/?>", "\n", m.group(1))).strip())
            + '</code></pre>'
        ),
        body,
    )

    # Operators table: replace the messy pre/code block with a proper HTML table
    body = _operators_table(body)
    body = body.replace("<p><strong>Operator</strong> <strong>Description</strong></p>", "")

    # Part 4 tables
    body = _data_type_table(body)
    body = _dict_kv_table(body)

    # Strip backslash-escapes before HTML quotes in code blocks (from \&quot;)
    def fix_code_quotes(m: re.Match[str]) -> str:
        c = m.group(1).replace("\\&quot;", "&quot;").replace('\\"', '"')
        return f"<pre><code>{c}</code></pre>"
    body = re.sub(r"<pre><code>(.*?)</code></pre>", fix_code_quotes, body, flags=re.DOTALL)

    return body


def _operators_table(body: str) -> str:
    pattern = re.compile(
        r'<pre><code>\s*==\s+If the values.*?becomes true\.\s*</code></pre>',
        re.DOTALL,
    )
    if not pattern.search(body):
        return body
    rows = [
        ("==",  "Values of two operands are equal"),
        ("!=",  "Values of two operands are not equal"),
        ("&gt;", "Left operand is greater than right operand"),
        ("&lt;", "Left operand is less than right operand"),
        ("&gt;=", "Left operand is greater than or equal to right operand"),
        ("&lt;=", "Left operand is less than or equal to right operand"),
    ]
    table_rows = "\n".join(
        f"<tr><td><code>{op}</code></td><td>{desc} → condition is true</td></tr>"
        for op, desc in rows
    )
    table = (
        "<table>\n"
        "<thead><tr><th>Operator</th><th>Meaning</th></tr></thead>\n"
        f"<tbody>\n{table_rows}\n</tbody>\n</table>"
    )
    return pattern.sub(table, body)


def wrap_page(title: str, active: int, body: str, prev_href: str | None, next_href: str | None) -> str:
    classes = ["", "", "", "", ""]
    classes[active] = ' class="active"'
    sidebar = SIDEBAR.format(
        p1=classes[0],
        p2=classes[1],
        p3=classes[2],
        p4=classes[3],
        p5=classes[4],
    )
    nav_links = []
    if prev_href:
        nav_links.append(f'<a href="{prev_href}">← Previous</a>')
    else:
        nav_links.append("<span></span>")
    if next_href:
        nav_links.append(f'<a href="{next_href}">Next →</a>')
    else:
        nav_links.append("<span></span>")
    page_nav = f'<div class="page-nav">{nav_links[0]}{nav_links[1]}</div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)} — Computational Economics</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {{
      document.querySelectorAll('pre code').forEach(function(block) {{
        // Normalize class="python" (from pandoc fenced blocks) → language-python
        if (!block.className || block.className === 'python') {{
          block.className = 'language-python';
        }}
        hljs.highlightElement(block);
        // Copy button
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
{sidebar}
      </nav>
    </aside>

    <main>
      <section class="hero">
        <h1>{html.escape(title.split(". ", 1)[-1] if ". " in title else title)}</h1>
      </section>
      {body}
      {page_nav}
    </main>
  </div>

  <footer class="site-footer">
    Computational Economics — Module 1
  </footer>
</body>
</html>
"""


def build_index() -> None:
    cards = [
        ("part1-installation.html", "Part 1", "Installation of Python and Anaconda", "Install Anaconda, set up Spyder, and get ready to code."),
        ("part2-language.html", "Part 2", "The Python Programming Language", "High-level vs. low-level languages and why Python is used in economics."),
        ("part3-packages.html", "Part 3", "Python Packages and Modules", "Import packages like pandas and use other people's code."),
        ("part4-data-structures.html", "Part 4", "Data Structures in Python", "Primitive and collective data types: lists, dictionaries, and more."),
        ("part5-programming.html", "Part 5", "Basic Programming Techniques", "Conditionals, indentation, loops, and Project 1 tasks."),
    ]
    card_html = "\n".join(
        f"""          <a class="card" href="module1/{href}">
            <div class="card-step">{step}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
          </a>"""
        for href, step, title, desc in cards
    )
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Module 1 — Computational Economics</title>
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="site-header-inner">
      <div>
        <h1 class="site-title"><a href="index.html">Computational Economics</a></h1>
        <p class="site-subtitle">Module 1 — Python Foundations</p>
      </div>
    </div>
  </header>

  <div class="layout">
    <aside class="sidebar">
      <nav>
        <div class="sidebar-label">Module 1</div>
        <a href="index.html" class="active">Overview</a>
        <a href="module1/part1-installation.html">Part 1: Installation</a>
        <a href="module1/part2-language.html">Part 2: Python Language</a>
        <a href="module1/part3-packages.html">Part 3: Packages &amp; Modules</a>
        <a href="module1/part4-data-structures.html">Part 4: Data Structures</a>
        <a href="module1/part5-programming.html">Part 5: Programming</a>
      </nav>
    </aside>

    <main>
      <section class="hero">
        <h1>Module 1</h1>
        <p>
          Python foundations for computational economics. Complete Part 1 before class
          if you have not used Python before. Use Anaconda and Spyder as described in
          Part 1.
        </p>
      </section>

      <section>
        <h2>Before You Start</h2>
        <div class="callout">
          <div class="callout-title">Prerequisite setup</div>
          <p>
            Install <strong>Anaconda</strong> and launch <strong>Spyder</strong> through
            Anaconda Navigator. Unless you are very confident about virtual environments,
            follow Part 1 and use Spyder as your IDE.
          </p>
        </div>
      </section>

      <section>
        <h2>Course Materials</h2>
        <div class="card-grid">
{card_html}
        </div>
      </section>
    </main>
  </div>

  <footer class="site-footer">
    Computational Economics — Module 1
  </footer>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def main() -> None:
    text = load_markdown()
    OUT_DIR.mkdir(exist_ok=True)

    for idx, part in enumerate(PARTS):
        section = extract_section(text, part["start"], part["end"])
        cleaned = clean_markdown(section)
        body = markdown_to_html(cleaned)
        prev_href = PARTS[idx - 1]["slug"] + ".html" if idx > 0 else None
        next_href = PARTS[idx + 1]["slug"] + ".html" if idx < len(PARTS) - 1 else None
        page = wrap_page(part["title"], idx, body, prev_href, next_href)
        (OUT_DIR / f"{part['slug']}.html").write_text(page, encoding="utf-8")
        print(f"Wrote {part['slug']}.html")

    build_index()
    print("Wrote index.html")


if __name__ == "__main__":
    main()
