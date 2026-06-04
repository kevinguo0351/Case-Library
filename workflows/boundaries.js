export const meta = {
  name: 'casebook-boundaries',
  description: 'Detect per-case page ranges and exhibit pages for each casebook PDF',
  phases: [{ title: 'Boundaries', detail: 'one agent per book parses TOC, writes case_map' }],
}

// args: [{ in, out, school, file }, ...]  (one entry per book)
const BOOKS = Array.isArray(args) ? args : []

const SUMMARY = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    n_cases: { type: 'integer' },
    page_offset: { type: ['integer', 'null'] },
    method: { type: 'string', description: 'bookmarks | toc | hybrid' },
    notes: { type: 'string' },
  },
  required: ['ok', 'n_cases', 'method'],
}

function prompt(b) {
  return `You map a consulting casebook PDF into its individual practice cases.

Read this boundary-input JSON file with the Read tool:
${b.in}

It contains: school, file, page_count, embedded bookmarks, printed table-of-contents text (toc_text), and a one-line-per-page index (page_index) where each line is:
  "pN  [fontSize] title <TAB> snippet <TAB> flags"
The flag EXH means that page's text mentions "exhibit".

GOAL: identify every practice CASE. Skip front matter, the interview-process / "how to case" guides, industry overviews, and pure feedback-form appendices. For each case give its PDF page range and which PDF pages hold exhibits/charts/heavy-math worth screenshotting.

METHOD:
1. Prefer the printed Table of Contents (toc_text), which usually lists case name + printed page. If embedded bookmarks cleanly mark each case, use those instead.
2. Printed page numbers usually differ from PDF page numbers by a FIXED offset. Find the offset: locate the PDF page in page_index whose large-font title matches the FIRST case name; offset = that_pdf_page - first_case_printed_page. Apply the same offset to every case's printed page.
3. A case spans from its start page to the page just before the next case starts (the final case ends before any closing appendix, else at page_count).
4. exhibit_pdf_pages: within each case range, list PDF pages flagged EXH, or whose title/snippet shows a chart, exhibit, data table, or dense numbers.

Write the result as STRICT minified JSON (UTF-8) to EXACTLY this path with the Write tool:
${b.out}

JSON shape:
{"school":"${b.school}","file":"${b.file}","page_count":<int>,"page_offset":<int|null>,
 "cases":[{"idx":1,"case_name":"...","case_type":"Profitability|Market Entry|Growth|Pricing|M&A|Investment|Market Sizing|Operations|Other|null","round":"1|2|null","industry":"...|null","difficulty":"...|null","pdf_page_start":<int>,"pdf_page_end":<int>,"exhibit_pdf_pages":[<int>...]}],
 "notes":"anything uncertain"}

Pages are 1-based PDF pages. Do NOT invent cases that aren't present.

CRITICAL — validate before finishing: after writing the file, verify it is valid JSON by running this Bash command:
  C:/Users/guowenjie/market-monitor/.venv/Scripts/python.exe -c "import json,sys; json.load(open(r'${b.out}',encoding='utf-8')); print('VALID')"
If it does not print VALID (common slips: a doubled bracket like []], a trailing comma, or an unescaped " inside a string), fix the JSON and rewrite the file, then re-check. Only return the summary once it prints VALID.

Return the summary (ok, n_cases, page_offset, method, notes).`
}

phase('Boundaries')
const results = await parallel(BOOKS.map((b) => () =>
  agent(prompt(b), { label: `${b.school}/${b.file}`, phase: 'Boundaries', schema: SUMMARY, model: 'sonnet' })
    .then((r) => ({ ...r, school: b.school, file: b.file }))
    .catch(() => null)
))

const ok = results.filter(Boolean)
const totalCases = ok.reduce((s, r) => s + (r.n_cases || 0), 0)
log(`Boundaries: ${ok.length}/${BOOKS.length} books mapped, ~${totalCases} cases total`)
return {
  books_done: ok.length,
  books_total: BOOKS.length,
  total_cases: totalCases,
  per_book: ok.map((r) => ({ school: r.school, file: r.file, n_cases: r.n_cases, offset: r.page_offset, method: r.method })),
}
