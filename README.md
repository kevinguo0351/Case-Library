# Casebook Drill Extraction Pipeline

Turns a folder of consulting **casebook PDFs** (organized by business school / year)
into structured, AI-readable **drill JSON** — one self-contained file per practice
case, with the **prompt (what the candidate sees) split from the solution (answer key)**
and exhibits/charts rendered to PNG.

> **Want to practice with it (get an AI to interview you)?** See **[HOW_TO_USE.md](HOW_TO_USE.md)**.
> **Want the patterns mined from all 2,141 cases** (trigger→action heuristics, per-type frameworks, the math/exhibit playbook, grounded with counts)? See **[PATTERNS.md](PATTERNS.md)**.
> **Want the first-principles essence** (the 10 laws that generate every heuristic, the single most-rewarding bucket per type, and the exact "money lines")? See **[PRINCIPLES.md](PRINCIPLES.md)**.
> **Want what separates an *outstanding* candidate** (second-order thinking + the behaviors the answer keys reward most)? See **[OUTSTANDING.md](OUTSTANDING.md)**.
> 中文: [PATTERNS.zh.md](PATTERNS.zh.md) · [PRINCIPLES.zh.md](PRINCIPLES.zh.md) · [OUTSTANDING.zh.md](OUTSTANDING.zh.md)
> Note: case interviews have **no single right answer** — the `solution` blocks are a reference, not a grading key.

Source corpus: `C:\Users\guowenjie\Desktop\Prep\Top Business School Casebook_2023 Version`
(17 schools, ~100 books).

## Architecture (4 phases)

Mechanical work is deterministic Python (PyMuPDF). The two genuinely semantic
steps — finding case boundaries across wildly different TOC layouts, and splitting
each case into prompt vs. answer key — run as **Claude workflows** (one agent per
book / per case, Sonnet).

| Phase | Tool | Script / Workflow | Output |
|---|---|---|---|
| 0. Digest | Python | `scripts/01_digest.py` | `data/digests/*.json` — per-page text, fonts, image/exhibit flags, bookmarks, TOC text |
| (prep) | Python | `scripts/02_boundary_inputs.py` | `data/boundary_inputs/*.json` — slim per-book input for the boundary agent |
| 1. Boundaries | Claude | `workflows/boundaries.js` | `data/case_maps/*.json` — each case's page range + exhibit pages |
| 2. Slice | Python | `scripts/03_slice.py` | `data/cases/<School>/<year>/<NN_slug>/` + `data/manifest.json` |
| 3. Extract | Claude | `workflows/extract.js` | `drill.json` in each case folder (split prompt/solution) |

## Per-case output

```
data/cases/<School>/<year>/<NN>_<slug>/
  meta.json     # school, year, case_name, type, round, industry, page range, exhibit refs
  raw.txt       # full page-marked text of the case
  exhibits/     # exhibit_pNNN.png — only chart/exhibit/math pages, rendered at 170 DPI
  drill.json    # the structured drill (see shape below)
```

### `drill.json` shape

```jsonc
{
  "case_id": "...",
  "meta": { school, year, case_name, case_type, round, industry, difficulty },
  "prompt": {                 // ONLY what the candidate may see/hear
    "context": "...",         // interviewer's opening
    "question": "...",        // the task to solve
    "clarifying_info": [{ q, a }],   // revealed only when asked
    "exhibits": [{ id, title, image, shows, data }]  // image = rendered PNG; no interpretation
  },
  "solution": {               // the answer key — reveal after attempting
    "framework": ["bullet", ...],
    "questions": [{ prompt, guidance, math: { setup, steps[], answer }, exhibit_ref }],
    "brainstorming": { prompt, categories: [{ name, ideas[] }] },
    "recommendation": { recommendation[], risks[], next_steps[] }
  },
  "tags": [...],
  "math_intensity": "low|medium|high"
}
```

## How to run

Python venv: `C:/Users/guowenjie/market-monitor/.venv/Scripts/python.exe` (has PyMuPDF).
Always set `PYTHONIOENCODING=utf-8` on Windows.

```bash
PY="C:/Users/guowenjie/market-monitor/.venv/Scripts/python.exe"

# Phase 0 + prep (all books)
PYTHONIOENCODING=utf-8 "$PY" scripts/01_digest.py
PYTHONIOENCODING=utf-8 "$PY" scripts/02_boundary_inputs.py

# Phase 1 — boundaries (Claude workflow). Bake the book list, then run:
#   gen_run.py turns a list.json into a standalone script so Workflow needs no big args.
"$PY" scripts/gen_run.py workflows/boundaries.js data/_boundary_args.json workflows/boundaries_run.js BOOKS
#   -> Workflow({ scriptPath: "workflows/boundaries_run.js" })
"$PY" scripts/04_validate_maps.py            # writes data/_boundary_rerun.json for failures
#   re-bake from _boundary_rerun.json and re-run until "Need rerun: 0"

# Phase 2 — slice (all valid maps)
PYTHONIOENCODING=utf-8 "$PY" scripts/03_slice.py

# Phase 3 — extract (Claude workflow), batched (<1000 agents/run)
"$PY" scripts/05_extract_args.py             # all cases  -> data/_extract_args.json
#   (or:  05_extract_args.py Darden          # one school
#         05_extract_args.py --missing       # only cases lacking a valid drill.json)
"$PY" scripts/gen_run.py workflows/extract.js data/_extract_args.json workflows/extract_run.js CASES
#   -> Workflow({ scriptPath: "workflows/extract_run.js" })
```

### Drilling chunk-by-chunk

`05_extract_args.py <school>` builds a batch for just one school; `--missing`
restricts to cases not yet extracted. So you can drill / extract incrementally
instead of all at once.

## Notes

- **Why a boundary agent instead of a TOC parser?** The 17 schools use ~3 different
  TOC formats (column tables, bare numbered lists, embedded bookmarks). An agent that
  reads the TOC + page index generalizes without 17 hand-written parsers.
- **Exhibits are vector charts**: their numbers extract as text but the visual is lost,
  so chart/math pages are rendered to PNG and referenced by `prompt.exhibits[].image`.
- Both workflows self-validate their JSON (re-read + `json.load`) before returning;
  `04_validate_maps.py` and the `--missing` flag catch any stragglers for a clean re-run.
