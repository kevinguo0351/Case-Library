"""
Build the extract-workflow arg list from the manifest.

Each entry points an extract agent at one sliced case folder:
  {dir, raw, meta, out, case_id}

Usage:
    python 05_extract_args.py [filter] [--missing] [--out NAME.json]
  filter    : only cases whose case_id contains this substring (e.g. "Darden")
  --missing : only cases that do not yet have a valid drill.json
  --out     : output filename under data/ (default _extract_args.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:/Users/guowenjie/casebook-drill/data")
MANIFEST = ROOT / "manifest.json"


def has_valid_drill(out: Path) -> bool:
    if not out.exists():
        return False
    try:
        json.loads(out.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


def main():
    argv = sys.argv[1:]
    out_name = "_extract_args.json"
    if "--out" in argv:
        i = argv.index("--out")
        out_name = argv[i + 1]
        del argv[i:i + 2]
    only_missing = "--missing" in argv
    argv = [a for a in argv if a != "--missing"]
    flt = argv[0].lower() if argv else None

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = []
    for m in manifest:
        if flt and flt not in m["case_id"].lower():
            continue
        d = Path(m["dir"])
        out = d / "drill.json"
        if only_missing and has_valid_drill(out):
            continue
        items.append({
            "dir": str(d).replace("\\", "/"),
            "raw": str(d / "raw.txt").replace("\\", "/"),
            "meta": str(d / "meta.json").replace("\\", "/"),
            "out": str(out).replace("\\", "/"),
            "case_id": m["case_id"],
        })
    (ROOT / out_name).write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(items)} cases -> {ROOT / out_name}"
          + (f"  (filter={flt})" if flt else "")
          + ("  (missing only)" if only_missing else ""))


if __name__ == "__main__":
    main()
