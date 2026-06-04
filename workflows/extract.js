export const meta = {
  name: 'casebook-extract',
  description: 'Turn each sliced case into split prompt/solution drill JSON',
  phases: [{ title: 'Extract', detail: 'one agent per case writes drill.json' }],
}

// args: [{ dir, raw, meta, out, case_id }, ...]  (one entry per case)
const CASES = Array.isArray(args) ? args : []

const SUMMARY = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    case_id: { type: 'string' },
    case_type: { type: 'string' },
    n_questions: { type: 'integer' },
    has_math: { type: 'boolean' },
    n_exhibits: { type: 'integer' },
    notes: { type: 'string' },
  },
  required: ['ok', 'case_id'],
}

function prompt(c) {
  return `You convert ONE consulting interview case into a structured "drill" JSON for self-practice.

Read these two files with the Read tool:
- raw case text:  ${c.raw}
- metadata:       ${c.meta}    (school, year, case_name, case_type, round, industry, exhibit_images[])

The raw text is the full text of the case's PDF pages (page-marked "===== PDF pN ====="). Casebooks interleave what the INTERVIEWER says, the candidate-facing prompt, exhibits, and the ANSWER KEY (suggested framework, guidance, math solutions, brainstorming answers, recommendation). Your job is to SPLIT these cleanly so the user can attempt the case, then reveal the answer.

Produce drill JSON with this exact shape (omit a field only if truly absent):
{
  "case_id": "${c.case_id}",
  "meta": {"school":"","year":"","case_name":"","case_type":"","round":"","industry":"","difficulty":""},
  "prompt": {
    "context": "the background the interviewer reads aloud to open the case",
    "question": "the explicit task/question the candidate must solve (verbatim or tightly paraphrased)",
    "clarifying_info": [{"q":"question a candidate might ask","a":"answer the interviewer gives only if asked"}],
    "exhibits": [{"id":"Exhibit 1","title":"","image":"<one of meta.exhibit_images or null>","shows":"what the exhibit displays, WITHOUT interpreting it for the candidate","data":"key numbers/labels visible in the exhibit"}]
  },
  "solution": {
    "framework": ["bullet point", "bullet point"],
    "questions": [{"prompt":"sub-question / step","guidance":"what a strong answer covers","math":{"setup":"","steps":["",""],"answer":""},"exhibit_ref":"Exhibit 1 or null"}],
    "brainstorming": {"prompt":"the brainstorm question","categories":[{"name":"bucket","ideas":["",""]}]},
    "recommendation": {"recommendation":["",""],"risks":["",""],"next_steps":["",""]}
  },
  "tags": ["industry/topic tags"],
  "math_intensity": "low|medium|high"
}

RULES:
- prompt.* = ONLY what the candidate may see/hear up front (plus clarifying_info, which is revealed on request). Never leak the answer into prompt.*.
- solution.* = the answer key. Put ALL framework suggestions, guidance, math, brainstorm answers, and recommendation here.
- framework MUST be bullet points (array of short strings), mirroring the casebook's suggested structure.
- For exhibits, copy the matching filename from meta.exhibit_images into "image". Describe what it shows but do NOT solve it in prompt.exhibits — the working/answer goes in solution.questions[].math.
- Preserve real numbers from the math. If a calculation appears, capture setup, steps, and final answer.
- Keep it faithful to THIS case; do not invent content.

Write STRICT minified JSON (UTF-8) to EXACTLY this path with the Write tool:
${c.out}

Then VALIDATE by running this Bash command:
  C:/Users/guowenjie/market-monitor/.venv/Scripts/python.exe -c "import json; json.load(open(r'${c.out}',encoding='utf-8')); print('VALID')"
If it does not print VALID, fix the JSON (watch for doubled brackets, trailing commas, unescaped quotes) and rewrite until it does. Only then return the summary.`
}

phase('Extract')
const results = await parallel(CASES.map((c) => () =>
  agent(prompt(c), { label: c.case_id, phase: 'Extract', schema: SUMMARY, model: 'sonnet' })
    .then((r) => ({ ...r, case_id: c.case_id }))
    .catch(() => null)
))

const ok = results.filter(Boolean)
log(`Extract: ${ok.length}/${CASES.length} cases done`)
return {
  cases_done: ok.length,
  cases_total: CASES.length,
  with_math: ok.filter((r) => r.has_math).length,
}
