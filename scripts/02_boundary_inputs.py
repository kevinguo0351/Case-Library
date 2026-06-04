"""
Build a slim "boundary input" per book from its digest.

The boundaries workflow only needs enough to locate case starts/ends and
exhibit pages: the printed table-of-contents text, embedded bookmarks, and a
one-line-per-page index (page number, title, short snippet, exhibit flag).
This is ~5-10 KB/book vs the 50-130 KB full digest, which keeps the per-book
agent call cheap.

Usage: python 02_boundary_inputs.py [filter]
"""
import json
import sys
from pathlib import Path

DIGESTS = Path(r"C:/Users/guowenjie/casebook-drill/data/digests")
OUT = Path(r"C:/Users/guowenjie/casebook-drill/data/boundary_inputs")


def build(digest: dict) -> dict:
    lines = []
    for p in digest["pages"]:
        title = (p["title"] or "").replace("\n", " ")[:55]
        snip = p["snippet"][:60]
        flags = []
        if p["has_exhibit_kw"]:
            flags.append("EXH")
        if p["n_images"] >= 3:
            flags.append(f"img{p['n_images']}")
        flag = ",".join(flags)
        # Compact, grep-able single line per page.
        lines.append(f"p{p['pdf_page']}\t[{p['title_size']}] {title}\t{snip}\t{flag}")
    return {
        "school": digest["school"],
        "file": digest["file"],
        "rel_path": digest["rel_path"],
        "page_count": digest["page_count"],
        "bookmarks": digest["bookmarks"],
        "toc_pages": digest["toc_pages"],
        "toc_text": digest["toc_text"],
        "page_index": lines,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    flt = sys.argv[1].lower() if len(sys.argv) > 1 else None
    n = 0
    for jf in sorted(DIGESTS.glob("*.json")):
        if flt and flt not in jf.name.lower():
            continue
        digest = json.loads(jf.read_text(encoding="utf-8"))
        out = build(digest)
        (OUT / jf.name).write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
        n += 1
    print(f"Built {n} boundary inputs -> {OUT}")


if __name__ == "__main__":
    main()
