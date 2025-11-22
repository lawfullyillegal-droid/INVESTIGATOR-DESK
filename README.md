# INVESTIGATOR-DESK
INVESTIGATE THE SOURCE
# Investigator Desk

A lightweight, client-side investigative toolkit:
- Case overview and JSON export/import
- Evidence ingest (files/URLs) with SHA-256 hashing
- Entities and link graph (vis-network)
- Timeline with event counts (Chart.js)
- Public records request generator (generic template)
- Chain-of-custody logging

## Quick start
1. Create a new GitHub repository and add these files.
2. Enable GitHub Pages: Settings → Pages → Build and deployment → Source: GitHub Actions.
3. Commit and push. The workflow will build and deploy automatically.
4. Your app persists locally via `localStorage`. Use JSON export/import for portability.

## Local dev
Open `index.html` in a browser, or run a static server:
```bash
python -m http.server 8080
