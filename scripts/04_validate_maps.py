"""
Validate case_map files and emit the list of books still needing a (re)run.

A book is OK iff its case_map exists, parses as JSON, and has >=1 case with the
required page fields. Writes the rerun arg list (same shape as _boundary_args)
for any book that is missing or invalid, so the boundaries workflow can be
re-invoked on just those.

Usage: python 04_validate_maps.py
Exit status is informational; it always writes _boundary_rerun.json.
"""
import json
from pathlib import Path

INPUTS = Path(r"C:/Users/guowenjie/casebook-drill/data/boundary_inputs")
MAPS = Path(r"C:/Users/guowenjie/casebook-drill/data/case_maps")
RERUN = Path(r"C:/Users/guowenjie/casebook-drill/data/_boundary_rerun.json")

REQ = ("pdf_page_start", "pdf_page_end", "case_name")


def valid_map(p: Path) -> tuple[bool, str]:
    if not p.exists():
        return False, "missing"
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"bad json: {e}"
    cases = d.get("cases")
    if not isinstance(cases, list) or not cases:
        return False, "no cases"
    for c in cases:
        if not all(k in c for k in REQ):
            return False, "case missing required field"
    return True, f"{len(cases)} cases"


def main():
    rerun = []
    ok = bad = 0
    for jf in sorted(INPUTS.glob("*.json")):
        d = json.loads(jf.read_text(encoding="utf-8"))
        mp = MAPS / jf.name
        good, msg = valid_map(mp)
        if good:
            ok += 1
        else:
            bad += 1
            print(f"  RERUN {jf.stem}: {msg}")
            rerun.append({
                "in": str(jf).replace("\\", "/"),
                "out": str(mp).replace("\\", "/"),
                "school": d["school"], "file": d["file"],
            })
    RERUN.write_text(json.dumps(rerun, ensure_ascii=False), encoding="utf-8")
    print(f"\nValid: {ok}  |  Need rerun: {bad}  ->  {RERUN}")


if __name__ == "__main__":
    main()
