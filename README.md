# Computational Economics — Course Website

Static course website for Modules 1 and 2 (Anaconda + Spyder workflow).

## Landing page

**[index.html](index.html)** is the course home. Module entry points:

| Module | URL path |
|--------|----------|
| Home | `/index.html` |
| Module 1 parts | `/module1/part1-installation.html` … `part5-programming.html` |
| Module 1 practice | `/module1/practice1.html` |
| Module 2 overview | `/module2/index.html` |
| Module 2 practice | `/module2/practice2.html` |

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
├── module2/
│   ├── index.html
│   ├── part1-1-list-functions.html
│   ├── part1-2-dict-functions.html
│   ├── part2-logic-operators.html
│   ├── part3-loops.html
│   ├── part4-json-comments.html
│   ├── practice2.html
│   ├── files/                  # Project 2 downloads
│   └── from_canvas/            # Canvas source HTML (not published)
└── scripts/
    ├── build_module1.py        # Legacy Word → HTML pipeline
    ├── build_module2.py        # Canvas → Module 2 pages
    └── convert_html_source.py  # Canvas HTML → site HTML
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

**Module 1** pages live in `module1/*.html`. **Module 2** pages are built from Canvas exports:

```bash
python3 scripts/build_module2.py
```

To convert a single Canvas file:

```bash
python3 scripts/convert_html_source.py SOURCE.html OUTPUT.html --module 2 --title "Page Title" --active page.html
```

See `.cursor/skills/canvas-to-site/SKILL.md` for conversion patterns.

## Student setup (default)

Install **Anaconda**, open **Anaconda Navigator**, install and launch **Spyder**. See Part 1 on the website for full instructions.
