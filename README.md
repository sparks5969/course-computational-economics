# Computational Economics — Course Website

Static course website for a **Summer 2026** course at **China Agriculture University**.
Students use **Anaconda + Spyder** as the default Python environment.

**Instructor:** Sining Wang (王思宁)

**Live site:** [https://sparks5969.github.io/course-computational-economics/](https://sparks5969.github.io/course-computational-economics/)

---

## Course modules

| Module | Title | Status |
|--------|-------|--------|
| 1 | Python Foundations | Complete |
| 2 | Stable Matching | Complete |
| 3 | OOP & Functions | Complete |
| 4 | Economic Growth | Workshop complete; practice project coming soon |
| 5 | Machine Learning in Predictive Modeling | Placeholder |

Each module overview (`moduleX/index.html`) follows the same layout:

1. **Overview** — short description
2. **Lecture Slides** — downloadable `.pptx` (or placeholder if not yet available)
3. **Workshop** — card grid linking to workshop pages

The sidebar uses foldable sections per module. The first link under each module is **Overview & Lecture Slides**.

---

## Local preview

From the repo root:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000). The landing page is `index.html`.

---

## Site structure

```
├── index.html                         # Course home (module hub)
├── assets/css/style.css               # Shared styles
├── module1/                           # Hand-maintained HTML (legacy Word pipeline)
│   ├── index.html
│   ├── part1-installation.html … part5-programming.html
│   ├── practice1.html
│   └── module1_introduction.pptx
├── module2/
│   ├── index.html
│   ├── part*.html, practice2.html
│   ├── module2_gale_shapley.pptx
│   ├── files/                         # Starter script, data, prompt book
│   └── from_canvas/                   # Source HTML (not published)
├── module3/ … module5/                # Same pattern as module2
└── scripts/                           # Build tools (see below)
```

**Published:** everything except `from_canvas/`, `scripts/`, and `.cursor/`.

**Practice projects** use a lightweight page pattern: short background + download links only.
Step-by-step instructions live in the **starter script** and **prompt book** (`.md`), not on the webpage.

---

## Build scripts

All scripts run from the `scripts/` directory:

```bash
cd scripts
```

| Script | Purpose |
|--------|---------|
| `convert_html_source.py` | Core converter: Canvas HTML → site page body |
| `build_module2.py` | Build all Module 2 workshop + practice pages |
| `build_module3.py` | Build all Module 3 workshop + practice pages |
| `build_module4.py` | Build all Module 4 workshop pages |
| `build_home.py` | Rebuild `index.html` and all `moduleX/index.html` overview pages |
| `refresh_sidebars.py` | Update navigation on every HTML page |
| `build_module1.py` | Legacy Word → HTML pipeline (Module 1 only) |

### Typical workflow after editing Canvas sources

```bash
cd scripts
python3 build_module4.py      # or build_module2.py / build_module3.py
python3 build_home.py         # refresh overview pages
python3 refresh_sidebars.py   # sync navigation everywhere
```

### Convert a single Canvas file

```bash
python3 convert_html_source.py \
  ../module4/from_canvas/part1.1_generate_vectors.html \
  ../module4/part1-1-generate-vectors.html \
  --module 4 \
  --title "Part 1.1 — Generate Vectors" \
  --active part1-1-generate-vectors.html
```

Requires `beautifulsoup4` (`pip install beautifulsoup4`).

---

## Adding a new workshop page

1. Place the Canvas export in `moduleX/from_canvas/`.
2. Add an entry to the `PAGES` list in `scripts/build_moduleX.py`.
3. Add the link to `MODULEX_WORKSHOP` in `scripts/convert_html_source.py`.
4. Add a workshop card to the module config in `scripts/build_home.py`.
5. Run the build workflow above.

---

## Adding a practice project

1. Put files in `moduleX/files/`:
   - incomplete starter script (e.g. `project2.py`)
   - optional data files
   - prompt book (e.g. `project2_promptbook.md`)
2. Add a `build_practiceX()` function in `scripts/build_moduleX.py` (see Module 2 or 3 for examples).
3. Add `"practiceX.html"` to `MODULEX_WORKSHOP` in `convert_html_source.py`.
4. Add a workshop card in `build_home.py`.
5. Rebuild and refresh sidebars.

### Prompt book format

Each step uses two parts:

- **Intention** — what the step achieves and why (for the student)
- **Prompt** — exact text to paste into an AI chat

See `module2/files/project2_promptbook.md` or `module3/files/practice_project3_promptbook.md`.

---

## Navigation configuration

Central definitions in `scripts/convert_html_source.py`:

- `MODULE_META` — module subtitles and sidebar link lists
- `MODULE_HUB` — course home page cards (set `live=False` for “coming soon”)

Overview page content (description, slides filename, workshop cards) is in `scripts/build_home.py` under `MODULES`.

After changing navigation, always run `build_home.py` and `refresh_sidebars.py`.

---

## Deploy (GitHub Pages)

1. Push to GitHub (`main` branch).
2. Repo **Settings → Pages → Deploy from branch → `main` → `/ (root)`**.
3. Site updates within 1–2 minutes. No build step on GitHub — pages are plain HTML.

---

## Student setup

Install **Anaconda**, open **Anaconda Navigator**, install and launch **Spyder**.
Full instructions are on the website: Module 1 → Part 1: Installation.

---

## Notes for maintainers / AI agents

- **Source of truth for Canvas conversion:** `scripts/convert_html_source.py`
- **Canvas conversion patterns** are also documented locally at `.cursor/skills/canvas-to-site/SKILL.md` (not in git; `.cursor/` is gitignored)
- Module 1 pages were built from Word and are edited directly; Modules 2–4 use the Canvas pipeline
- Lecture slide files (`.pptx`) sit in each `moduleX/` folder; reference the filename in `build_home.py`
