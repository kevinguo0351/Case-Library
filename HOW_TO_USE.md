# How to Use the Case Library

This library turns 100 MBA casebooks into 2,141 practice cases, each split into a
**candidate-facing prompt** and a **reference solution**, so an AI can act as your
interviewer: pose the case, withhold the answer, reveal exhibits/clarifications on
request, then debrief you.

## ⚠️ There is no single right answer

Case interviews are **not** graded on matching a model answer. The `solution` block
in each `drill.json` is **one reference path** — the casebooks themselves say their
frameworks are *"only provided as possible suggestions."* A different-but-sound
structure, a different recommendation backed by good logic, or a creative branch the
casebook never listed can all be **excellent**.

So when an AI runs a case for you, it should evaluate your **process**, not answer-matching:

- **Structure** — is the framework MECE, tailored to *this* case (not a memorized template)?
- **Hypothesis-driven** — do you state a hypothesis and drive toward it?
- **Quantitative** — is the math set up correctly and computed accurately? (This is the
  one place there *is* a right number — check `solution.questions[].math`.)
- **Business judgment** — are insights and trade-offs sensible?
- **Synthesis** — a crisp recommendation + risks + next steps, even if different from the reference.
- **Communication** — structured, top-down, concise.

Treat `solution` as a **rubric and a sanity check**, not a grading key.

## What's in each case

```
data/cases/<School>/<year>/<NN>_<slug>/
  meta.json     # school, year, name, type, round, industry
  raw.txt       # full source text (if you want the unprocessed version)
  exhibits/     # exhibit_pNNN.png — charts/data to show at the right moment
  drill.json    # the structured case (below)
```

| `drill.json` field | Who sees it | When |
|---|---|---|
| `prompt.context`, `prompt.question` | you | opening |
| `prompt.clarifying_info[]` (`{q, a}`) | you | only when you ask a relevant clarifying question |
| `prompt.exhibits[]` (`image`, `shows`, `data`) | you | when the case reaches that exhibit |
| `solution.framework[]` | reference | during debrief — as *a* structure, not *the* structure |
| `solution.questions[]` (incl. `math`) | reference | math answers are the real check; logic is a guide |
| `solution.brainstorming`, `solution.recommendation` | reference | compare ideas, don't expect a match |

## Three ways to run a case

### 1. In Claude Code (best — it can display the exhibit PNGs)

Just say, e.g.:

> Use `data/cases/Wharton/2017/05_chicago-parking-meters` and run a full mock case with me. You're the interviewer.

Claude reads the `drill.json`, opens with the prompt, answers clarifications only when
asked, shows the exhibit images when relevant, lets you work, then debriefs against the
reference. Pair it with the `management-consultant` skill for sharper structure feedback.

### 2. Any chatbot (web Claude / ChatGPT / DeepSeek)

Open a `drill.json`, paste it in, and prepend this **interviewer prompt**:

```
You are a top-firm (MBB) case interviewer. In the JSON below, `prompt` is what the
candidate may see; `solution` is a REFERENCE ONLY — there is no single correct answer,
so NEVER reveal it early and NEVER grade by matching it.

Run it like a real interview:
1. Read out only prompt.context and prompt.question, then stop and wait for me.
2. When I ask a clarifying question, answer ONLY from clarifying_info if relevant; otherwise say it's not specified.
3. When I'm ready for data, present the relevant exhibit (its `shows` + `data`); let me interpret it.
4. Make me drive each step. After each, give brief feedback on STRUCTURE (MECE, tailored),
   HYPOTHESIS, MATH ACCURACY (the math answers are the real check), BUSINESS JUDGMENT,
   and COMMUNICATION. Reward sound alternatives the reference didn't list.
5. At the end, ask me to synthesize a recommendation, then debrief: compare my structure
   and recommendation to the reference as one possible path, and score 1–5 per dimension
   with concrete, actionable notes.

[paste the drill.json here]
```

### 3. Pick cases by type / difficulty

`data/index.json` is the full inventory; each row has `case_id, school, year, case_name,
case_type, round, industry, math_intensity, n_exhibits, tags, dir`. Filter it to target
your weak spots, e.g.:

```bash
# all high-math Profitability cases
node -e "require('./data/index.json').filter(c=>c.case_type=='Profitability'&&c.math_intensity=='high').forEach(c=>console.log(c.case_id, '->', c.dir))"

# all Market Sizing cases
node -e "require('./data/index.json').filter(c=>/sizing/i.test(c.case_type)).forEach(c=>console.log(c.dir))"
```

`data/index.md` has the counts (Profitability 573, Market Entry 359, Operations 214,
Growth 197, M&A 138, Investment 113, Market Sizing 84, Pricing 70; math: medium 1241 /
low 455 / high 430).

## Practice tips

- **Time yourself** — ~30–40 min/case; structure in the first 2 min.
- **Don't peek at `solution`** until you've fully committed to your own structure and answer.
- **Drill the math** — set up the calc yourself first, then check the number against
  `solution.questions[].math.answer`. Numbers are the one objective check.
- **Vary the rep** — same case can be redone hypothesis-first, or with a different framework,
  to prove you're not memorizing.
- **Mix sources** — different schools phrase and structure cases differently; that variety is the point.

---

*Source casebooks are the copyright of their respective schools and authors; this library
is for personal interview preparation.*
