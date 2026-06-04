"""
Phase 2 - Slice each case out of its source PDF.

Reads the case_map JSON files produced by the `boundaries` workflow and, for
every case, writes a self-contained case folder:

    data/cases/<School>/<year>/<NN>_<slug>/
        meta.json          # metadata + page range + exhibit refs
        raw.txt            # full text of the case's pages, page-marked
        exhibits/exhibit_pNNN.png   # rendered exhibit/math pages only

Also writes a global manifest.json inventorying every case.

Usage: python 03_slice.py [filter]
"""
import json
import re
import sys
from pathlib import Path

import fitz

PREP = Path(r"C:/Users/guowenjie/Desktop/Prep/Top Business School Casebook_2023 Version")
CASE_MAPS = Path(r"C:/Users/guowenjie/casebook-drill/data/case_maps")
CASES = Path(r"C:/Users/guowenjie/casebook-drill/data/cases")
MANIFEST = Path(r"C:/Users/guowenjie/casebook-drill/data/manifest.json")
EXHIBIT_DPI = 170


def slug(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", (s or "case").strip().lower())
    return s.strip("-")[:50] or "case"


def year_of(filename: str) -> str:
    m = re.search(r"(19|20)\d{2}", filename)
    return m.group(0) if m else "n.d."


def slice_book(cmap: dict, manifest: list):
    school = cmap["school"]
    fname = cmap["file"]
    year = year_of(fname)
    pdf_path = PREP / school / fname
    if not pdf_path.exists():
        print(f"  MISSING PDF: {pdf_path}")
        return
    doc = fitz.open(pdf_path)
    pc = doc.page_count
    for case in cmap.get("cases", []):
        idx = case.get("idx", 0)
        start = max(1, int(case["pdf_page_start"]))
        end = min(pc, int(case["pdf_page_end"]))
        if end < start:
            continue
        case_dir = CASES / school / year / f"{idx:02d}_{slug(case.get('case_name'))}"
        ex_dir = case_dir / "exhibits"
        case_dir.mkdir(parents=True, exist_ok=True)

        # Full page-marked text of the case.
        parts = []
        for p in range(start, end + 1):
            parts.append(f"===== PDF p{p} =====\n{doc[p-1].get_text()}")
        (case_dir / "raw.txt").write_text("\n\n".join(parts), encoding="utf-8")

        # Render only the flagged exhibit/math pages.
        ex_imgs = []
        ex_pages = sorted({p for p in case.get("exhibit_pdf_pages", []) if start <= p <= end})
        if ex_pages:
            ex_dir.mkdir(exist_ok=True)
            for p in ex_pages:
                name = f"exhibit_p{p:03d}.png"
                doc[p - 1].get_pixmap(dpi=EXHIBIT_DPI).save(str(ex_dir / name))
                ex_imgs.append(f"exhibits/{name}")

        case_id = f"{school}_{year}_{idx:02d}_{slug(case.get('case_name'))}"
        meta = {
            "case_id": case_id,
            "school": school, "year": year, "source_pdf": str(pdf_path),
            "idx": idx,
            "case_name": case.get("case_name"),
            "case_type": case.get("case_type"),
            "round": case.get("round"),
            "industry": case.get("industry"),
            "difficulty": case.get("difficulty"),
            "pdf_page_start": start, "pdf_page_end": end,
            "n_pages": end - start + 1,
            "exhibit_pdf_pages": ex_pages,
            "exhibit_images": ex_imgs,
            "dir": str(case_dir),
        }
        (case_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest.append({
            "case_id": case_id, "school": school, "year": year,
            "case_name": case.get("case_name"), "case_type": case.get("case_type"),
            "round": case.get("round"), "industry": case.get("industry"),
            "n_pages": meta["n_pages"], "n_exhibits": len(ex_imgs),
            "dir": str(case_dir),
        })
    doc.close()


def main():
    flt = sys.argv[1].lower() if len(sys.argv) > 1 else None
    manifest = []
    n_books = 0
    for cm in sorted(CASE_MAPS.glob("*.json")):
        if flt and flt not in cm.name.lower():
            continue
        try:
            cmap = json.loads(cm.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  BAD case_map {cm.name}: {e}")
            continue
        slice_book(cmap, manifest)
        n_books += 1
        print(f"[{n_books}] {cm.stem}: {len(cmap.get('cases', []))} cases")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSliced {n_books} books -> {len(manifest)} cases. Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
