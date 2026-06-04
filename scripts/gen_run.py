"""
Bake a book/case list into a standalone runnable copy of a workflow script,
so Workflow can be invoked with just {scriptPath} (no giant args payload) and
remains resumable.

Usage:
    python gen_run.py <template.js> <list.json> <out.js> <CONST_NAME>
e.g. python gen_run.py workflows/boundaries.js data/_boundary_rerun.json \
        workflows/boundaries_run.js BOOKS
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/guowenjie/casebook-drill")


def main():
    template, list_json, out_js, const = sys.argv[1:5]
    src = (ROOT / template).read_text(encoding="utf-8")
    data = json.loads((ROOT / list_json).read_text(encoding="utf-8"))
    baked = f"const {const} = {json.dumps(data, ensure_ascii=False)}"
    # Replace the line that assigns the const from args.
    pat = re.compile(rf"const {const} = .*")
    if not pat.search(src):
        print(f"ERROR: no 'const {const} = ...' line in {template}")
        sys.exit(1)
    out = pat.sub(baked, src, count=1)
    (ROOT / out_js).write_text(out, encoding="utf-8")
    print(f"Wrote {out_js} with {len(data)} items baked into {const}")


if __name__ == "__main__":
    main()
