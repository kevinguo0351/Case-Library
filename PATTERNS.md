# Case-Cracking Pattern Playbook

*中文版见 [PATTERNS.zh.md](PATTERNS.zh.md)*


**Mined from all 2,141 cases in this library** — not generic prep advice. Every claim is grounded:
percentages and "lift" come from a deterministic scan of every `drill.json`; the per-type heuristics
come from agents that read hundreds of real answer keys. "Lift 1.7×" means *given that trigger, the
answer key is 1.7× more likely than baseline to do that move* — i.e. it's genuinely distinctive, not just common.

> Reminder: there is **no single right answer**. These are the moves the answer keys reward *most often*.
> A sound alternative is still great. Use this as pattern-recognition, not a script.

---

## 0. The numbers at a glance (n = 2,141)

| Metric | Value |
|---|---|
| Cases with quantitative math | **87.5%** — assume there will be math |
| Cases with an exhibit | **55.8%** |
| Framework size | avg **5.2** buckets/levers (median 5) |
| Clarifying questions rewarded | avg **5.2** per case (median 5) |
| Brainstorm structure | avg **4.2 buckets** (median 4) — **dist: 4 (33%), 5 (25%), 3 (15%), 2 (8%), 6 (6%)** |
| Type mix | Profitability 626 · Market Entry 386 · Investment/PE 354 · Growth 238 · M&A 149 · Market Sizing 94 · Pricing 71 · Operations ~214 |

**Two myths corrected by the data:**
- Brainstorming is **not** "usually two buckets" — it's **3–5, most often 4**. Plan for ~4 MECE buckets, 3–5 ideas each.
- Math is nearly universal (87.5%); the most common calc is **per-unit economics** (53% of math cases) and **margin/profit** (50%), *not* fancy NPV (19%).

---

## 1. Universal flow (works for every case type)

**The opening (do this every time):**
1. **Restate the objective + quantify it.** If a target is given ("double in 5y", "10% ROI", "$1B"), say the implied number out loud immediately and keep it as your North Star.
2. **Ask 2–4 clarifying questions** (see §2) — then take a moment to structure.
3. **Lay out a MECE framework** of ~5 buckets tailored to *this* case (not a memorized template).
4. **State a hypothesis** before you're asked. Answer keys praise hypothesis-led candidates in the majority of cases; they penalize "let me gather more data before forming a view."

**The exhibit protocol (56% of cases have one) — 4 mandatory moves:**
1. **Say what it shows** in one sentence. 2. **Normalize** (turn absolutes into %, per-unit, or ratios so things are comparable). 3. **Find the gap / outlier** (the one number that's different). 4. **"So what"** — state the implication *before* being asked. The #1 logged failure is stopping after step 1.

**The brainstorm protocol:** name **~4 MECE buckets first**, then go 3–5 ideas deep on the most promising. Don't free-associate.

**The close (do this even if not asked — rewarded in ~70% of cases):** **Recommendation** (1 line + the number) → **Risks** (2–3) → **Next steps** (2–3, sequenced).

---

## 2. Clarifying-question defaults (% = how often the answer key rewards it)

Lead with these, roughly in this order of payoff:

| Ask about… | % of cases | Why it pays |
|---|---|---|
| **Competitors / market share** | **33%** | Most-rewarded clarifier. "Who else is in this market and what's their share/moat?" |
| **Cost & price structure** | **28%** | Fixed vs. variable, unit economics — unlocks profitability & pricing math |
| **Objective / target / definition of success** | **25%** | The number you'll anchor the whole case to |
| **Geography / scope** | **23%** | National vs. local; what transfers across regions |
| **Time horizon** | **14%** | Sets whether you use payback, NPV, or perpetuity |
| **Capabilities / resources** | **10%** | Right-to-win; build vs. buy |
| **Market size / growth, customer segments** | **~6% each** | When sizing or targeting matters |

---

## 3. ⚡ Universal trigger → action cheat sheet (the headline)

Empirically the strongest "if you see X, do Y" rules (lift = how much more likely than baseline):

| If the prompt says / you see… | …then the answer key usually… | Evidence |
|---|---|---|
| **Revenue is declining/falling** | **Decompose revenue into price × volume (and by segment/product)** — and ask for the actual figures by segment before averaging | **lift 1.72×** |
| **Profit / margin is declining** | First **decompose revenue (1.71×)**, then **split cost into fixed vs. variable (1.51×)**; isolate which side moved | **lift 1.7×** |
| **Profit down but revenue flat** | Jump straight to the **cost side**; check each cost line as % of revenue YoY — the line that broke trend is the culprit | Profitability keys |
| **Multiple products / segments / regions** | **Never average — ask for the breakdown.** The root cause hides in one sub-bucket | ~25/30 profit cases |
| **A competitor is mentioned** | **Isolate internal-vs-external (1.35×)** and **examine the broader market/industry/macro (1.15×)**; quantify the rival's share/moat & likely response | **lift 1.35×** |
| **"Should we acquire / merge" (M&A)** | **Assess strategic fit & synergies (1.56×)**; frame as *standalone value + synergy NPV ≥ price* | **lift 1.56×** |
| **"Should we invest / build a facility"** | **Get to the financial case — NPV / payback / breakeven (1.34×)**; compare to the do-nothing/alternative | **lift 1.34×** |
| **Pricing decision** | Run **all three lenses** (cost floor, competitor anchor, value ceiling) — and **decompose cost (1.27×)** | **lift 1.27×** |
| **Costs are rising / high** | Check **capabilities & structure (1.32×)**: is the cost fixed-structural (needs portfolio action) or variable-operational (negotiate/substitute)? | **lift 1.32×** |
| **A numeric target / ambition is given** | **Back-calculate the required CAGR / share / volume** and sanity-check feasibility *before* brainstorming levers | Growth keys |
| **"Should we enter a market"** | Size the market **and** assess **right-to-win / capabilities (1.24×)** — never conclude "big market → enter" | **lift 1.24×** |
| **A target/asset underperforms peers** | **Diagnose the root cause and re-model the post-fix economics** — don't take the weak margin as fixed | M&A / profit keys |
| **Sunk cost mentioned** | **Exclude it** from the decision and say so out loud (common trap) | Investment/M&A keys |
| **An exhibit appears** | Normalize → find the outlier → "so what". For cost charts: *if costs match a rival but profit differs → the lever is price* | 56% of cases |

Risk side, when you close: the risks that recur most are **competitive response (43%)**, **execution/operational (39%)**, **regulation (22%)**, **brand (20%)**, **cost overrun/capital (16%)**. Name 2–3 of these.

---

## 4. Per-type playbooks

### Profitability  *(626 cases — the most common)*
- **Framework:** Profit = Revenue − Cost. (1) confirm which side is the driver, (2) decompose it. Revenue = price × volume, split by product/segment/region/channel/cohort. Cost = **fixed vs. variable first**, then line items (rent, labour, COGS, distribution, SG&A). Add a **per-unit margin** layer for mix/breakeven.
- **Triggers:** profit↓ revenue flat → cost side; revenue↓ cost flat → is it price, volume, or mix?; decline coincides with an event (acquisition, mgmt change, new pricing) → that event is the cause; multiple SKUs → get the breakdown; capacity-constrained → rank products by **profit per unit of the constraint** (per machine-hour / per seat / per sq ft), not per unit.
- **Math:** weighted-avg margin; per-unit profit = price − VC; **breakeven = fixed ÷ (price − VC)**; % -change cost bridges; perpetuity = profit ÷ r; payback = capex ÷ annual profit.
- **Great vs. good:** segment before averaging; use math to *kill* hypotheses; tie root cause to a mechanism; quantify each lever; ignore sunk/fixed costs in decisions.

### Market Entry  *(386)*
- **Framework (5 buckets):** market attractiveness (size/growth/profitability/competition) → **company fit / right-to-win** → entry mode (build/buy/partner) → financial viability (share→revenue, breakeven/NPV) → risks & go/no-go.
- **Triggers:** "should we enter" → size **and** right-to-win; capability gap → buy/partner not build; multiple segments → segment-and-select before sizing; new geography → check regulation, distribution, local cost; entrenched competitor → quantify their moat/share; entry cost given → do payback/breakeven; razor-and-blade/subscription → model recurring revenue separately; market near saturation → pivot to new segment/geography.
- **Great vs. good:** quantify right-to-win (not just attractiveness); surface the unprompted 3rd option (license/JV/sell); test against the stated hurdle; sequence the entry (test → validate → scale); stress-test the most dangerous assumption.

### Investment / PE  *(354)*
- **Framework:** market attractiveness → asset/target quality → **financial case (NPV/IRR/payback)** → risks & exit → strategic fit/synergies.
- **Triggers:** any "should we invest/build" → it's ultimately a numbers decision, get to NPV/payback; ROI target given → invert to a **max price** (`total profit ÷ (1+hurdle)`); discount rate given → DCF/growing-perpetuity `FCF ÷ (r − g)`, not a simple sum; build-a-plant → map the value chain for the **binding bottleneck** before using nameplate capacity; thin margin (≤5%) → stress-test loudly; two near-equal NPVs → look for a missing revenue/cost stream or decide on qualitative/execution risk; growth rate looks too good → find the structural cause (one-time wave?); sunk cost → exclude.
- **Math:** payback (most common), NPV (fixed-horizon and perpetuity), growing/declining perpetuity `FCF/(r−g)`, ROI inversion to max price, contribution/breakeven. State simplifications ("undiscounted payback…").
- **Great vs. good:** find the bottleneck before the revenue calc; ask for r and g; spot disguised trends; don't double-count synergies/intra-company transfers; quantify intangibles to an order of magnitude; reverse-engineer the required exit and test feasibility.

### Growth  *(238)*
- **Framework:** organic vs. inorganic → **Ansoff 2×2** (penetration / new products / new segments-geos / diversification) → revenue bridge (volume × price × mix).
- **Triggers:** "how to grow" → anchor on Ansoff before brainstorming; growth stalled but volume stable → suspect saturation/share shift, compare client vs. market growth; numeric target → back-calc CAGR & feasibility; organic vs. inorganic → compare **net contribution / CLV per customer** for each; new entrant took share → decompose (did we lose customers, or did they grow the category?); single-customer concentration → diversification; new line → compute cannibalization vs. total revenue; EBITDA target (PE) → decompose the gap and size each initiative's contribution.
- **Great vs. good:** decompose before diagnosing; declare the required CAGR out loud; quantify each initiative's share of the gap; compare organic/inorganic on economics; ask for the control group on test-market data; check the binding constraint on vertical-integration ideas before strategizing; flag when the addressable market is too small to hit the target.

### M&A  *(149)*
- **Framework (7):** strategic rationale → market attractiveness → target standalone value → **synergies (cost vs. revenue, quantified separately)** → valuation & price → integration & risks → alternatives.
- **Triggers:** any acquisition → probe **rationale first** (why this target, why now); "should we acquire" → *standalone NPV + synergy NPV ≥ price*; quantify **cost synergies (certain) separately from revenue synergies (caveated)**; comps given → apply EV/EBITDA to **post-synergy** EBITDA; perpetuity `CF/(r−g)`; PE buyer → reframe on MOIC/IRR with a year-by-year table + exit multiple; weak target margin → diagnose root cause and re-model; contracting market → it's a consolidation play; multi-target → eliminate on strategic fit before running numbers; cross-sell revenue → net out cannibalization; sunk cost → exclude.
- **Great vs. good:** **don't ignore the price** — always close "max price = X vs. ask = Y → creates/destroys Z"; post-synergy EBITDA in multiples; diagnose underperformance; consider alternatives; net cannibalization from synergies; separate "should we do it" from "how to structure it".

### Pricing  *(71)*
- **Framework — 3 lenses every time:** **cost-based** (floor), **competitor-based** (anchor), **value-based / WTP** (ceiling); set price between floor and ceiling. Add **segmentation / price discrimination** when buyer types/SKUs/channels differ. (Each lens appears in ~half of cases; ~11/18 require running all three in sequence.)
- **Triggers:** any pricing Q → run all 3 lenses before committing; new/innovative product with measurable benefit → **value-based, not cost-plus** (capture a share of the customer's quantified savings); commodity cheaper than rivals with identical product → raise toward competitor; competitive bid → switch to **total cost of ownership**, not sticker price; cut one SKU / raise another → run elasticity by segment then **sum to check total contribution**; sold through an intermediary → treat **commission as a pricing variable**; regulated price → pricing isn't the lever, volume/cost is; exclusivity → scarcity raises WTP; patent expiry → time the strategy to the lifecycle.
- **Math:** price-gap × volume; contribution = (price − VC) × volume; breakeven on a price change; value ceiling = competitor price + quantified incremental value; build a price→profit table and pick the max (not highest price or volume).

### Market Sizing  *(94)*
- **Approach:** mostly **bottom-up** (population → cohort → penetration → frequency → unit size/price); durable goods = **installed base ÷ lifespan + new demand**; top-down when you have a known anchor (a player's share/volume).
- **Triggers:** consumable → population × cohort × penetration × usage × price; durable → replacement (base ÷ lifespan) + new; B2B/fleet → size to **peak** demand; **always convert a stock to a flow** by asking the purchase cycle/lifespan; sub-national → scale from national by population ratio; known player data → back into the total; sizing exists to **answer the real question** (feasibility/breakeven), so end with a verdict; ratio asked → build numerator & denominator independently; apply a **market-share step** before reporting company (not market) revenue.
- **Great vs. good:** state the equation before computing; round aggressively & say why; state assumptions with a directional rationale; **use the number to answer the question**; run a sensitivity on the most uncertain assumption; segment before aggregating.

### Operations / Cost-reduction  *(~214)*
- **Framework:** clarify objective → **walk the value chain stage by stage** (inputs → process → outputs) → cost-to-serve decomposition (fixed/variable, direct/overhead, **per-unit**) → capacity/throughput/**bottleneck** → quality/SLA as a binding constraint → one-time investment vs. ongoing savings (**payback**).
- **Triggers:** high per-unit cost → decompose into utilization-driven fixed cost + variable drivers, normalize to % of revenue; low utilization (≤50%) → consolidate / JV / outsource; make-vs-buy → side-by-side cost table + payback + qualitative override; SKU proliferation + inventory build → Pareto the SKUs; automation → labour saved − new overhead, then payback (note automation often **shifts** work, not eliminates it; include severance); cost-cut with a "don't hurt X" constraint → rank levers by efficiency per unit of the constraint (e.g. NPS per $M); outsourcing costs more → compare on headcount × cost, not cost per head.

---

## 5. The math playbook (87.5% of cases)

Ranked by how often each appears (% of math cases):

1. **Per-unit / ratio economics (53%)** — cost per unit, revenue per customer/store/hour. Always normalize to per-unit before comparing.
2. **Margin / profit (50%)** — profit = revenue − cost; contribution = (price − VC) × volume; weighted-avg margin across segments.
3. **Breakeven / payback (19%)** — breakeven units = fixed ÷ (price − VC); payback = capex ÷ annual profit. State if undiscounted.
4. **NPV / discounting (19%)** — fixed-horizon DCF; **growing perpetuity = FCF ÷ (r − g)**; round factors ((1.1)⁴≈1.5, (1.1)⁷≈2.0).
5. **Market sizing (18%)** — population → cohort → penetration → frequency → price; or installed base ÷ lifespan.
6. **% change / growth rate (15%)** — CAGR = (end/start)^(1/n) − 1; YoY cost bridges.
7. **Market-share math (9%)**, **ROI/IRR (3%)**.

**Recurring tricks:** ignore sunk costs; rank by profit-per-constrained-unit when capacity binds; use post-synergy EBITDA in M&A multiples; convert a target into a required CAGR/share/volume; always apply a market-share step before reporting *company* revenue.

---

## 6. Brainstorming structures (plan for ~4 MECE buckets)

Most common bucket framings seen across the corpus: **cost reduction · competitive dynamics · pricing · distribution · operational · financial · strategic fit · geographic expansion**. Reliable 2×2/menu skeletons:

- **Profit levers:** Revenue (price / volume / mix) × Cost (fixed / variable).
- **Growth:** Ansoff — existing-vs-new products × existing-vs-new customers, plus inorganic.
- **Customer-focused vs. Product-focused** (classic for "how to raise price/revenue").
- **Internal vs. External**, **Short-term vs. Long-term** when the question is open.

---

## 7. Recommendation & risk templates

**Recommendation (1–2 sentences):** lead with the verdict + the number that supports it → name the 1–2 swing variables → flag the single biggest risk + contingency.

**Risks to scan (with corpus frequency):** competitive response **43%** · execution/operational **39%** · regulation/legal **22%** · brand/reputation **20%** · cost overrun/capital **16%** · customer churn/acceptance **8%** · cannibalization **8%**. Name 2–3, ideally one quantified ("the 7-yr payback is ~2× the 4-yr hurdle").

**Next steps:** 2–3 sequenced, actionable validations ("first confirm X, then model Y, then decide Z").

---

*Generated by `scripts/07_mine_patterns.py` (quantitative, all 2,141 cases) + per-type analysis of sampled answer keys. Numbers are descriptive of THIS library, not universal truths. Case interviews reward sound reasoning over answer-matching.*
