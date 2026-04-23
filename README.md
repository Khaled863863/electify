# Electify

A student-built directory of easy general-education electives at the American University of Beirut.

- **68 courses** across the AUB GE attributes
- Aggregates several student-collected guides and a curated master list — all student-sourced; raw input files are kept private
- **Live community section** where any student can suggest a course; trending suggestions get promoted to the main list

## Quick start

```bash
# Build data from PDFs + xlsx in your Downloads folder
python scripts/build_data.py

# Render the static site to dist/
python scripts/build_site.py

# Preview locally
cd dist && python -m http.server 8000
```

## Deploy

See **DEPLOY.md** for the step-by-step (GitHub → Cloudflare Pages → custom domain).

## Visual design

See **CLAUDE_DESIGN_PROMPT.md** to spin up polished mockups in claude.ai/design.

## Stack

- **Generator:** Python 3 + Jinja2
- **Styling:** Tailwind CSS (CDN)
- **Hosting:** Cloudflare Pages (free)
- **Submissions:** Google Form → public Google Sheet → fetched live by the Community page
