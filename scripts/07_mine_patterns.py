"""
Mine recurring, quantified patterns across ALL drilled cases.

Reads every drill.json and aggregates:
  - corpus overview (type/industry/math/round/school distributions)
  - structure stats (framework bullets, clarifying count, brainstorm #categories, math presence)
  - clarifying-question intent buckets (what candidates should clarify, with counts)
  - framework vocabulary per case_type (recurring buckets/levers)
  - brainstorming structure (how many buckets, common bucket labels)
  - math signatures (breakeven / NPV / market sizing / %change / margin / ...)
  - exhibit "shows" chart types + content themes
  - recommendation / risk / next-step recurring themes
  - TRIGGER -> ACTION co-occurrence ("if prompt mentions X, solution usually does Y")

Outputs:
  data/patterns_stats.json  (full machine-readable)
  prints a human summary.

Usage: python 07_mine_patterns.py
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:/Users/guowenjie/casebook-drill/data")
MANIFEST = ROOT / "manifest.json"

STOP = set("""a an the of to and or for in on at by with from into as is are be was were this that these those
your you our we they it its their his her him she he them us i me my mine ours yours client company case
should could would can may might will shall do does did has have had not no yes if then than so such
what which who whom whose how why when where about over under up down out off only just also more most
some any each per via vs etc e g ie eg using use used new other others one two three between within across
into onto upon their there here he she 's n't""".split())


def load_drills():
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = []
    for m in man:
        p = Path(m["dir"]) / "drill.json"
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        out.append(d)
    return out


def norm_type(t):
    """Collapse the free-text case_type long tail into canonical buckets."""
    t = (t or "").lower()
    if not t:
        return "Unknown"
    pairs = [
        ("market siz", "Market Sizing"), ("guesstimat", "Market Sizing"),
        ("market entry", "Market Entry"), ("enter", "Market Entry"), ("go/no", "Market Entry"),
        ("m&a", "M&A"), ("merger", "M&A"), ("acqui", "M&A"), ("due dilig", "M&A"),
        ("pricing", "Pricing"), ("price", "Pricing"),
        ("profitab", "Profitability"), ("cost", "Profitability"), ("margin", "Profitability"),
        ("revenue", "Growth"), ("growth", "Growth"), ("expansion", "Growth"),
        ("invest", "Investment"), ("valuation", "Investment"), ("pe", "Investment"), ("npv", "Investment"),
        ("operation", "Operations"), ("supply", "Operations"), ("process", "Operations"),
        ("new product", "New Product"), ("launch", "New Product"), ("commercial", "New Product"),
        ("opportunit", "Opportunity Assessment"),
        ("brain", "Brain Teaser"),
        ("strategy", "Strategy"), ("competit", "Strategy"),
    ]
    for k, v in pairs:
        if k in t:
            return v
    return "Other"


def words(text):
    return [w for w in re.findall(r"[a-z][a-z\-]+", (text or "").lower()) if w not in STOP and len(w) > 2]


def bigrams(ws):
    return [f"{ws[i]} {ws[i+1]}" for i in range(len(ws) - 1)]


# ---- clarifying-question intent buckets ----
CLARIFY_BUCKETS = {
    "objective / target / goal": r"objective|goal|target|aim|success|how much|by how|looking to|want to (achieve|reach)|defin(e|ition) of success",
    "time horizon": r"time\s?frame|time\s?horizon|how long|by when|years?|short[- ]?term|long[- ]?term|deadline",
    "client core business / how they make money": r"core business|how do(es)? (the|they|we|it).*make money|business model|what does the (client|company) do|revenue (streams|model)|main product",
    "market size / growth": r"market size|how (big|large) is the market|market grow|tam|addressable|industry size",
    "competition / competitors": r"competitor|competition|market share|rivals|players|fragmented|consolidat",
    "geography / scope": r"geograph|region|countr|local|national|global|where (are|is|do)",
    "customers / segments": r"customer segment|target customer|who (are|is) the (customer|client'?s customer)|demographic|b2b|b2c|end user",
    "product / offering details": r"what (is|does) the product|product (line|mix|features|specs)|offering|sku",
    "cost / price structure": r"cost structure|fixed (cost|vs)|variable cost|how much does it cost|price|margin|unit econ",
    "capabilities / resources": r"capabilit|do we have|in[- ]?house|expertise|resources|capacity|assets",
    "why now / context of the ask": r"why (now|did|are)|what (triggered|happened|changed)|context|background|reason",
    "budget / capital available": r"budget|capital|how much can|investment available|funds|afford",
    "competitive response / regulation": r"regulat|legal|government|barrier|patent|response from",
}


# ---- math operation signatures ----
MATH_SIGS = {
    "breakeven / payback period": r"break[- ]?even|payback|recoup|years to (pay|recover)|cover (the|its) (fixed|investment)",
    "NPV / discounting / cash flow": r"npv|discount|present value|wacc|cash flow|over \d+ years",
    "market sizing (population/segment build-up)": r"population|households?|per (capita|person|household)|segment.*\*|% of (the )?(population|market)|bottom[- ]?up|top[- ]?down",
    "percentage change / growth rate": r"\bcagr\b|growth rate|% (increase|decrease|change|growth)|year[- ]?over[- ]?year|yoy",
    "margin / profit calc": r"margin|profit\s*=|revenue\s*-\s*cost|gross profit|operating profit|contribution",
    "price x quantity (revenue)": r"price\s*[\*x]\s*(quantity|volume|units|qty)|units?\s*[\*x]\s*price|volume\s*[\*x]",
    "ROI / return": r"\broi\b|return on (investment|capital)|irr\b",
    "market share math": r"market share\s*[\*x]|share of|\bshare\b.*market size",
    "ratio / per-unit": r"per (unit|lb|ton|item|customer|store|hour|day|year|sku)|cost per|revenue per",
}

# ---- recommendation / risk themes ----
RISK_THEMES = {
    "competitor / competitive response": r"competitor|competit|retaliat|respond|price war|match",
    "cannibalization": r"cannibal",
    "customer churn / acceptance": r"churn|customers? (may|might|could)|acceptance|backlash|willing to pay|lose customers|demand (drop|fall)",
    "execution / operational risk": r"execut|operational|implement|integration|capacity|supply|ramp[- ]?up|timeline",
    "market / demand contraction": r"market (may )?(contract|shrink|decline)|demand (decline|fall|drop)|recession|downturn",
    "regulation / legal": r"regulat|legal|complian|government|patent|antitrust",
    "cost overrun / capital": r"cost overrun|over budget|capex|capital|funding|cash",
    "brand / reputation": r"brand|reputation|image|perception",
    "cannibalize-vs-margin / price": r"margin (erosion|pressure)|price (sensit|elasticity)|discount",
}

# ---- trigger (prompt) -> outcome (solution) co-occurrence ----
TRIGGERS = {
    "revenue is declining/falling": r"revenue.{0,30}(declin|fall|drop|decreas|down|shrink)|(declin|fall|drop|decreas).{0,30}revenue",
    "profit/margin is declining": r"(profit|margin|earnings).{0,30}(declin|fall|drop|decreas|down|shrink|low)",
    "should we enter a market": r"enter|market entry|expand into|go into|launch in",
    "competitor mentioned": r"competitor|competition|rival|new entrant|market share",
    "new product / launch": r"new product|launch|introduc|develop a|roll ?out",
    "acquisition / merger / M&A": r"acqui|merger|merge|buy(ing)? a|target company|takeover",
    "pricing decision": r"\bprice\b|pricing|how much (should|to) charge|set the price",
    "should we invest / build a facility": r"invest|build a (plant|factory|facility)|capex|capacity expansion",
    "market sizing asked": r"how (many|much)|size the|estimate the (number|market)|market size",
    "costs are rising/high": r"cost.{0,30}(ris|increas|high|up|grow)|(ris|increas|high).{0,30}cost",
    "customer/demand issue": r"customer.{0,30}(leav|churn|unhappy|declin|lost)|losing (customers|share)",
    "client wants to grow": r"grow|growth|increase (revenue|sales|profit)|double|scale",
}

OUTCOMES = {
    "decompose revenue = price x volume (or segments)": r"price.{0,20}(volume|quantity|units)|volume.{0,20}price|by segment|product mix|revenue.{0,20}(driver|breakdown|stream)",
    "decompose cost into fixed vs variable": r"fixed (cost|and variable)|variable cost|cogs|overhead",
    "isolate the driver (internal vs external)": r"internal.{0,20}external|company.{0,20}(competitor|market|industry)|3c|micro.{0,20}macro|firm.{0,20}market",
    "examine the broader market / industry / macro": r"market (size|growth|trend)|industry|macro|overall (market|environment)|whole market|external factors|porter",
    "discuss competitive dynamics / response": r"competit|market share|rival|response|retaliat|differentiat",
    "build a market-sizing estimate": r"population|households?|per (capita|person)|segment|bottom[- ]?up|top[- ]?down|% of",
    "evaluate financials (NPV/payback/breakeven)": r"npv|payback|break[- ]?even|roi|cash flow|discount",
    "assess capabilities / fit / synergies": r"capabilit|synerg|strategic fit|core competenc|in[- ]?house|resources",
    "list risks + recommendation + next steps": r"risk|next step|recommend",
    "consider cannibalization / customer willingness": r"cannibal|willing to pay|customer (accept|adopt)|demand",
}


def pct(n, d):
    return round(100 * n / d, 1) if d else 0.0


def as_dict(x):
    return x if isinstance(x, dict) else {}


def bs_categories(sol):
    """brainstorming may be a dict{categories:[...]}, a bare list of categories, or absent."""
    bs = sol.get("brainstorming")
    if isinstance(bs, dict):
        cats = bs.get("categories", [])
    elif isinstance(bs, list):
        cats = bs
    else:
        cats = []
    return [c for c in cats if isinstance(c, dict)]


def main():
    drills = load_drills()
    N = len(drills)
    res = {"n_cases": N}

    # ---- overview ----
    types = Counter(norm_type(d.get("meta", {}).get("case_type")) for d in drills)
    inds = Counter((d.get("meta", {}).get("industry") or "Unknown").strip() for d in drills)
    math_int = Counter(d.get("math_intensity") or "n/a" for d in drills)
    rounds = Counter(str(d.get("meta", {}).get("round") or "n/a") for d in drills)
    res["by_type"] = dict(types.most_common())
    res["by_industry_top25"] = dict(inds.most_common(25))
    res["by_math_intensity"] = dict(math_int.most_common())
    res["by_round"] = dict(rounds.most_common())

    # ---- structure stats ----
    fb, cq, bc, qn, has_math, has_ex = [], [], [], [], 0, 0
    for d in drills:
        sol = d.get("solution", {}) or {}
        pr = d.get("prompt", {}) or {}
        fb.append(len(sol.get("framework", []) or []))
        cq.append(len(pr.get("clarifying_info", []) or []))
        bs = bs_categories(sol)
        if bs:
            bc.append(len(bs))
        qs = [q for q in (sol.get("questions", []) or []) if isinstance(q, dict)]
        qn.append(len(qs))
        if any(q.get("math") for q in qs):
            has_math += 1
        if pr.get("exhibits"):
            has_ex += 1

    def stats(xs):
        xs = [x for x in xs if isinstance(x, int)]
        if not xs:
            return {}
        s = sorted(xs)
        return {"avg": round(sum(xs) / len(xs), 1), "median": s[len(s)//2],
                "min": s[0], "max": s[-1]}
    res["structure"] = {
        "framework_bullets": stats(fb),
        "clarifying_questions": stats(cq),
        "brainstorm_categories": {**stats(bc), "distribution": dict(Counter(bc).most_common())},
        "solution_questions": stats(qn),
        "pct_with_math": pct(has_math, N),
        "pct_with_exhibits": pct(has_ex, N),
    }

    # ---- clarifying intent buckets ----
    all_clar = []
    for d in drills:
        for c in (d.get("prompt", {}) or {}).get("clarifying_info", []) or []:
            all_clar.append((c.get("q") or "").lower())
    clar_hits = {}
    for name, pat in CLARIFY_BUCKETS.items():
        rx = re.compile(pat)
        n_q = sum(1 for q in all_clar if rx.search(q))
        n_cases = sum(1 for d in drills if any(rx.search((c.get("q") or "").lower())
                      for c in (d.get("prompt", {}) or {}).get("clarifying_info", []) or []))
        clar_hits[name] = {"cases": n_cases, "pct_cases": pct(n_cases, N), "questions": n_q}
    res["clarifying_buckets"] = dict(sorted(clar_hits.items(), key=lambda x: -x[1]["cases"]))
    res["clarifying_total_questions"] = len(all_clar)

    # ---- framework vocabulary per type ----
    fw_by_type = defaultdict(list)
    for d in drills:
        t = norm_type(d.get("meta", {}).get("case_type"))
        for b in (d.get("solution", {}) or {}).get("framework", []) or []:
            fw_by_type[t].append(b)
    fw_terms = {}
    for t, bullets in fw_by_type.items():
        if len(bullets) < 15:
            continue
        ws = []
        for b in bullets:
            w = words(b)
            ws += w + bigrams(w)
        fw_terms[t] = {"n_bullets": len(bullets),
                       "top_terms": [w for w, _ in Counter(ws).most_common(30)]}
    res["framework_vocab_by_type"] = fw_terms

    # ---- brainstorming bucket labels ----
    bs_labels = Counter()
    for d in drills:
        for cat in bs_categories(d.get("solution", {}) or {}):
            nm = (cat.get("name") or "").strip().lower()
            if nm:
                bs_labels[nm] += 1
    # cluster label words
    bs_label_words = Counter()
    for nm, c in bs_labels.items():
        for w in words(nm):
            bs_label_words[w] += c
    res["brainstorm_label_top_words"] = dict(bs_label_words.most_common(30))
    res["brainstorm_common_labels"] = dict(bs_labels.most_common(30))

    # ---- math signatures ----
    math_text_by_type = defaultdict(list)
    math_sig_counts = Counter()
    math_sig_cases = Counter()
    for d in drills:
        t = norm_type(d.get("meta", {}).get("case_type"))
        blob = []
        for q in (d.get("solution", {}) or {}).get("questions", []) or []:
            mth = q.get("math") if isinstance(q, dict) else None
            if isinstance(mth, dict):
                blob.append((mth.get("setup") or "") + " " + " ".join(mth.get("steps") or []) + " " + str(mth.get("answer") or ""))
        blob = " ".join(blob).lower()
        if not blob.strip():
            continue
        math_text_by_type[t].append(blob)
        seen = set()
        for name, pat in MATH_SIGS.items():
            if re.search(pat, blob):
                math_sig_counts[name] += 1
                seen.add(name)
        for name in seen:
            math_sig_cases[name] += 1
    res["math_signatures"] = {k: {"cases": v, "pct_of_math_cases": pct(v, has_math)}
                              for k, v in math_sig_cases.most_common()}

    # ---- exhibit themes ----
    ex_shows = []
    chart_types = Counter()
    for d in drills:
        for e in (d.get("prompt", {}) or {}).get("exhibits", []) or []:
            s = ((e.get("shows") or "") + " " + (e.get("title") or "")).lower()
            ex_shows.append(s)
            for ct, pat in {
                "bar / column chart": r"bar chart|column",
                "line / trend chart": r"line (chart|graph)|trend over|time series",
                "pie / share chart": r"pie chart|breakdown of|share of",
                "table of data": r"table|matrix|grid",
                "scatter / bubble": r"scatter|bubble",
            }.items():
                if re.search(pat, s):
                    chart_types[ct] += 1
    ex_theme_words = Counter()
    for s in ex_shows:
        for w in words(s):
            ex_theme_words[w] += 1
    res["exhibits"] = {
        "n_exhibits": len(ex_shows),
        "chart_types": dict(chart_types.most_common()),
        "theme_top_words": dict(ex_theme_words.most_common(30)),
    }

    # ---- risk / next-step themes ----
    risk_hits = Counter()
    risk_blob_all = []
    ns_blob_all = []
    for d in drills:
        rec = as_dict((d.get("solution", {}) or {}).get("recommendation"))
        rblob = " ".join(rec.get("risks", []) or []).lower()
        ns_blob_all += rec.get("next_steps", []) or []
        risk_blob_all.append(rblob)
        for name, pat in RISK_THEMES.items():
            if re.search(pat, rblob):
                risk_hits[name] += 1
    n_with_risk = sum(1 for b in risk_blob_all if b.strip())
    res["risk_themes"] = {k: {"cases": v, "pct_of_risk_cases": pct(v, n_with_risk)}
                          for k, v in risk_hits.most_common()}
    ns_words = Counter()
    for ns in ns_blob_all:
        for w in words(ns):
            ns_words[w] += 1
    res["next_step_top_words"] = dict(ns_words.most_common(30))

    # ---- trigger -> outcome co-occurrence (with lift vs baseline) ----
    def sol_value_text(sol):
        """Concatenate solution VALUES only (not JSON keys), lowercased."""
        parts = list(sol.get("framework", []) or [])
        for q in sol.get("questions", []) or []:
            if isinstance(q, dict):
                parts += [q.get("prompt") or "", q.get("guidance") or ""]
                m = q.get("math")
                if isinstance(m, dict):
                    parts += [m.get("setup") or ""] + (m.get("steps") or [])
        for c in bs_categories(sol):
            parts += [c.get("name") or ""] + (c.get("ideas") or [])
        rec = as_dict(sol.get("recommendation"))
        for key in ("recommendation", "risks", "next_steps"):
            parts += rec.get(key, []) or []
        return " ".join(str(p) for p in parts).lower()

    trig_rx = {k: re.compile(v) for k, v in TRIGGERS.items()}
    out_rx = {k: re.compile(v) for k, v in OUTCOMES.items()}
    cases_txt = []
    for d in drills:
        pr = d.get("prompt", {}) or {}
        ptxt = ((pr.get("context") or "") + " " + (pr.get("question") or "")).lower()
        cases_txt.append((ptxt, sol_value_text(d.get("solution", {}) or {})))
    # baseline outcome rates across whole corpus
    baseline = {o: sum(1 for _, s in cases_txt if orx.search(s)) for o, orx in out_rx.items()}
    res["outcome_baseline_pct"] = {o: pct(c, N) for o, c in baseline.items()}
    cooc = {}
    for tname, trx in trig_rx.items():
        idx = [i for i, (p, s) in enumerate(cases_txt) if trx.search(p)]
        base = len(idx)
        if base == 0:
            continue
        row = {"trigger_cases": base, "pct_of_corpus": pct(base, N), "then_usually": {}}
        for oname, orx in out_rx.items():
            hit = sum(1 for i in idx if orx.search(cases_txt[i][1]))
            trate = pct(hit, base)
            brate = pct(baseline[oname], N)
            lift = round(trate / brate, 2) if brate else None
            row["then_usually"][oname] = {"pct_when_triggered": trate,
                                          "baseline_pct": brate, "lift": lift, "cases": hit}
        # rank by lift (what's DISTINCTIVE about this trigger), then by rate
        row["then_usually"] = dict(sorted(row["then_usually"].items(),
                                   key=lambda x: (-(x[1]["lift"] or 0), -x[1]["pct_when_triggered"])))
        cooc[tname] = row
    res["trigger_to_action"] = cooc

    (ROOT / "patterns_stats.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- human summary ----
    print(f"=== {N} cases ===")
    print("TYPES:", dict(types.most_common(10)))
    print("STRUCTURE:", json.dumps(res["structure"], ensure_ascii=False))
    print("\nTOP CLARIFYING INTENTS (% of cases):")
    for k, v in list(res["clarifying_buckets"].items())[:10]:
        print(f"  {v['pct_cases']:5}%  {k}  ({v['cases']} cases)")
    print("\nBRAINSTORM #categories dist:", res["structure"]["brainstorm_categories"]["distribution"])
    print("BRAINSTORM common labels:", list(res["brainstorm_common_labels"].items())[:12])
    print("\nMATH SIGNATURES (% of math cases):")
    for k, v in list(res["math_signatures"].items()):
        print(f"  {v['pct_of_math_cases']:5}%  {k}  ({v['cases']})")
    print("\nRISK THEMES (% of risk cases):")
    for k, v in list(res["risk_themes"].items()):
        print(f"  {v['pct_of_risk_cases']:5}%  {k}")
    print("\nOUTCOME BASELINE (% of all cases):")
    for o, p in sorted(res["outcome_baseline_pct"].items(), key=lambda x: -x[1]):
        print(f"  {p:5}%  {o}")
    print("\nTRIGGER -> ACTION (ranked by LIFT vs baseline):")
    for t, row in res["trigger_to_action"].items():
        top = [x for x in row["then_usually"].items() if (x[1]["lift"] or 0) >= 1.15][:4]
        print(f"  [{row['pct_of_corpus']}% corpus] {t}:")
        for oname, ov in top:
            print(f"        lift {ov['lift']}x ({ov['pct_when_triggered']}% vs {ov['baseline_pct']}% base) -> {oname}")
    print(f"\nFull stats -> {ROOT/'patterns_stats.json'}")


if __name__ == "__main__":
    main()
