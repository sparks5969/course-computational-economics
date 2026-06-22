# Computational Economics — Course Website

Static course website for Module 1 (Anaconda + Spyder workflow).

## Landing page

**[index.html](index.html)** is the entry point. Students open:

| Page | URL path |
|------|----------|
| Overview | `/index.html` |
| Part 1–5 | `/module1/part1-installation.html` … `part5-programming.html` |
| Practice Project 1 | `/module1/practice1.html` |

## Local preview

```bash
python3 -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000).

## Site structure (what gets published)

```
├── index.html                      # Landing page — start here
├── assets/css/style.css            # Shared styles
├── module1/
│   ├── part1-installation.html
│   ├── part2-language.html
│   ├── part3-packages.html
│   ├── part4-data-structures.html
│   ├── part5-programming.html
│   └── practice1.html
└── scripts/                        # Build tools (not needed to view the site)
    ├── build_module1.py            # Legacy Word → HTML pipeline
    └── convert_html_source.py      # Canvas HTML → site HTML
```

## Deploy with GitHub Pages

1. Push this repo to GitHub.
2. In the repo: **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Choose branch **`main`** (or `master`) and folder **`/ (root)`**.
5. Save. After a minute or two, the site is live at:

   `https://<your-username>.github.io/<repo-name>/`

`index.html` at the repo root becomes the public homepage automatically. No build step is required — all pages are plain HTML.

## Updating content

**Published pages** live directly in `module1/*.html`. Edit those files, or convert new Canvas exports:

```bash
python3 scripts/convert_html_source.py <canvas-export.html> <output.html>
```

See `.cursor/skills/canvas-to-site/SKILL.md` for conversion patterns.

## Student setup (default)

Install **Anaconda**, open **Anaconda Navigator**, install and launch **Spyder**. See Part 1 on the website for full instructions.
