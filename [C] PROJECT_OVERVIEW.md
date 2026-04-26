# ECE 4330 problem drill

## Goal
Provide a clean browser-based drill app for ECE 4330 problems, solutions, and diagrams.

## Entrypoint
Open `study.html` or serve the folder and open `index.html`.

## How To Run
Run `py -3 -m http.server 8000` in this folder and open `http://localhost:8000`.

## Current Constraints
- The source PDFs still live under `02 Projects/Schoolwork/Linear Material`.
- `output/problems.json` is the live dataset used by the site.
- Any data repair should preserve the current UI contract: `source`, `topic`, `problem`, `has_solution`, `solution`, `images`, `solution_images`.
