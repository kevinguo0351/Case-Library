"""
Phase 0 - Per-book page digest.

Walks every casebook PDF and emits a compact JSON digest per book describing
each page (text snippet, largest title-like span, image/drawing counts, exhibit
flag) plus embedded bookmarks and detected table-of-contents pages.

This digest is the input to the `boundaries` Claude workflow, which decides each
case's page range without us hand-writing a TOC parser per school.

Usage:
    python 01_digest.py            # process all books
    python 01_digest.py Darden     # only books whose path contains "Darden"
"""
import json
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

PREP = Path(r"C:/Users/guowenjie/Desktop/Prep/Top Business School Casebook_2023 Version")
OUT = Path(r"C:/Users/guowenjie/casebook-drill/data/digests")

SNIPPET_CHARS = 220          # leading chars of each page kept for the digest
EXHIBIT_RE = re.compile(r"\bexhibit\b", re.IGNORECASE)
TOC_HINTS = ("table of contents", "contents")


def page_max_span(page):
    """Return (text, size) of the largest single text span on the page.

    The biggest span on a slide is almost always the case/section title, which
    the boundary agent uses to anchor a case's first page.
    """
    best_text, best_size = "", 0.0
    try:
        d = page.get_text("dict")
    except Exception:
        return "", 0.0
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                size = float(span.get("size", 0))
                text = span.get("text", "").strip()
                if size > best_size and text:
                    best_size, best_text = size, text
    return best_text, round(best_size, 1)


def digest_book(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    school = pdf_path.parent.name
    pages = []
    toc_pages = []
    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text() or ""
        norm = " ".join(text.split())
        title_text, title_size = page_max_span(page)
        snippet = norm[:SNIPPET_CHARS]
        low = norm.lower()
        is_toc = any(h in low for h in TOC_HINTS) and len(norm) < 2500
        if is_toc:
            toc_pages.append(i + 1)
        pages.append({
            "pdf_page": i + 1,                       # 1-based, matches Read/render
            "title": title_text[:120],
            "title_size": title_size,
            "snippet": snippet,
            "chars": len(norm),
            "n_images": len(page.get_images(full=True)),
            "n_drawings": len(page.get_drawings()),
            "has_exhibit_kw": bool(EXHIBIT_RE.search(norm)),
        })
    bookmarks = [
        {"level": lvl, "title": title, "pdf_page": pg}
        for (lvl, title, pg) in doc.get_toc()
    ]
    # Full text of detected TOC pages, handy for the boundary agent.
    toc_text = {str(p): (doc[p - 1].get_text() or "")[:3000] for p in toc_pages}
    doc.close()
    return {
        "school": school,
        "file": pdf_path.name,
        "rel_path": str(pdf_path),
        "page_count": len(pages),
        "n_bookmarks": len(bookmarks),
        "bookmarks": bookmarks,
        "toc_pages": toc_pages,
        "toc_text": toc_text,
        "pages": pages,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    flt = sys.argv[1].lower() if len(sys.argv) > 1 else None
    pdfs = sorted(PREP.rglob("*.pdf"))
    done = 0
    for pdf in pdfs:
        if flt and flt not in str(pdf).lower():
            continue
        try:
            d = digest_book(pdf)
        except Exception as e:  # keep going across the whole corpus
            print(f"ERROR {pdf.name}: {e}")
            continue
        out_name = f"{d['school']}__{pdf.stem}.json"
        (OUT / out_name).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        done += 1
        print(f"[{done}] {d['school']:12} {pdf.name:34} pages={d['page_count']:3} "
              f"bookmarks={d['n_bookmarks']:3} toc_pages={d['toc_pages']}")
    print(f"\nDigested {done} books -> {OUT}")


if __name__ == "__main__":
    main()
