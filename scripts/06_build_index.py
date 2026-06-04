"""
Build a single browseable index of every drilled case, enriched with fields
from each drill.json (case_type, math_intensity, tags). Lets you pick cases to
drill by school / type / industry / math level.

Outputs:
  data/index.json  - array of {case_id, school, year, case_name, case_type,
                      round, industry, math_intensity, n_exhibits, tags, dir}
  data/index.md    - quick human-readable summary table by school

Usage: python 06_build_index.py
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:/Users/guowenjie/casebook-drill/data")
MANIFEST = ROOT / "manifest.json"


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = []
    for m in manifest:
        drill = Path(m["dir"]) / "drill.json"
        d = {}
        if drill.exists():
            try:
                d = json.loads(drill.read_text(encoding="utf-8"))
            except Exception:
                d = {}
        meta = d.get("meta", {})
        rows.append({
            "case_id": m["case_id"],
            "school": m["school"], "year": m["year"],
            "case_name": m["case_name"],
            "case_type": meta.get("case_type") or m.get("case_type"),
            "round": meta.get("round") or m.get("round"),
            "industry": meta.get("industry") or m.get("industry"),
            "math_intensity": d.get("math_intensity"),
            "n_exhibits": m.get("n_exhibits", 0),
            "tags": d.get("tags", []),
            "drilled": bool(d),
            "dir": m["dir"],
        })
    (ROOT / "index.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    by_school = Counter(r["school"] for r in rows)
    by_type = Counter((r["case_type"] or "Unknown") for r in rows)
    by_math = Counter((r["math_intensity"] or "n/a") for r in rows)
    lines = [
        f"# Casebook Drill Index", "",
        f"**{len(rows)} cases** across **{len(by_school)} schools**, "
        f"{sum(r['n_exhibits'] for r in rows)} exhibit images.", "",
        "## By school", "",
        "| School | Cases |", "|---|---|",
    ]
    for s, n in sorted(by_school.items(), key=lambda x: -x[1]):
        lines.append(f"| {s} | {n} |")
    lines += ["", "## By case type", "", "| Type | Cases |", "|---|---|"]
    for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {n} |")
    lines += ["", "## By math intensity", "", "| Level | Cases |", "|---|---|"]
    for t, n in sorted(by_math.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {n} |")
    (ROOT / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Index: {len(rows)} cases -> data/index.json + data/index.md")
    print("Types:", dict(by_type))


if __name__ == "__main__":
    main()
