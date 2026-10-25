#!/usr/bin/env python3
"""Turn DeepSeek drafts into the benchmark question set: check, rate, dedupe, select, split.

Usage: filter_questions.py SETNAME DRAFTS.jsonl [DRAFTS.jsonl ...] [--no-rate]

1. Script checks (measured, not declared): the script of the text matches the declared
   language (metrics.detect_lang); length inside bounds; no URL; one message.
2. One DeepSeek rating call per surviving draft (natural, self-contained, answerable in text,
   safe, needs no live data, fits its mode, does not name the trait).
3. Exact and near duplicates: character 2-4-gram TF-IDF cosine within a language; a draft
   at or above NEAR (0.5) to an already selected question is skipped.
4. Selection per (language, trait, mode) up to QUOTA, best rated first, taking short, medium
   and long questions in turn so each cell keeps a length mix.
5. Split per (language, trait): invite questions alternate tuning/held-out starting with
   tuning, neutral ones starting with held-out, in a hash order, so tuning and held-out get
   the same count in each cell. AA's public questions and my seeds go to tuning only.

Writes DATA/questions/SETNAME/{all,tuning,heldout,rejects}.jsonl and report.json.
"""
import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

import dshbatch
import metrics

QUOTA = {"zh": 7, "en": 4, "ja": 3, "ko": 3}
NEAR = 0.5        # character 2-4-gram cosine of the question texts
TOPIC_NEAR = 0.6  # word cosine of the rater's English topic labels (catches same topic, new wording)
SALT = "gravitas-personality-v1"
TRAITS = json.load(open(dshbatch.HERE / "traits.json", encoding="utf-8"))["traits"]

RATE_TEMPLATE = """You are checking one draft question for a test set of real user questions to AI chat assistants.

Language: {lang_name}
Draft: <<<{q}>>>
Intended use: {intent}

Answer each check about the draft:
- natural: 1-5, how much it reads like a real native speaker of {lang_name} typed it to a chat assistant (5 = fully natural, 3 = understandable but stiff or translated-sounding, 1 = unnatural).
- self_contained: true if it can be answered without seeing a file, link, image, account or earlier conversation.
- answerable_in_text: true if a text answer can address it.
- safe: true if it is not asking for anything dangerous, sexual or hateful.
- needs_live_data: true if a good answer needs today's news, live prices or very recent events.
- fits: true if it serves the intended use stated above.
- names_trait: true if the draft explicitly asks for the style itself (for example 'be honest', 'be brief', 'make it funny', 'summarise').
- topic: 3 to 6 English words naming the specific situation or subject asked about (for example 'probation period social insurance', 'child first eye test dilation').

Reply with only a JSON object with exactly these keys."""

LANG_NAME = {"zh": "Simplified Chinese (mainland China)", "en": "English", "ja": "Japanese (Japan)", "ko": "Korean (South Korea)"}


def intent(r):
    if r["mode"] == "invite":
        return (f"it should gently give an assistant room to show the trait '{r['trait']}' "
                f"({TRAITS[r['trait']]['definition']}) without naming or asking for it.")
    return "an ordinary question that does not particularly invite any style such as humour, flattery, pushback or hedging."


def size(r):
    """Length in the units a reader feels: characters for zh/ja/ko, words for en."""
    return len(r["q"].split()) if r["lang"] == "en" else len(re.sub(r"\s", "", r["q"]))


def bucket(r):
    s = size(r)
    short, long_ = {"en": (12, 30), "zh": (25, 60), "ja": (30, 75), "ko": (25, 60)}[r["lang"]]
    return "short" if s <= short else ("long" if s > long_ else "medium")


def script_check(r):
    q = r["q"]
    if metrics.detect_lang(q) != r["lang"]:
        return "language script mismatch"
    lo, hi = {"en": (3, 90), "zh": (5, 220), "ja": (5, 250), "ko": (5, 250)}[r["lang"]]
    if not lo <= size(r) <= hi:
        return "length out of bounds"
    if re.search(r"https?://|www\.", q):
        return "url"
    if q.count("\n") > 2:
        return "multi-line"
    return None


def parse_rating(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except ValueError:
        return None
    need = {"natural", "self_contained", "answerable_in_text", "safe", "needs_live_data", "fits", "names_trait", "topic"}
    return d if need <= set(d) else None


def rating_ok(d):
    return (d is not None and isinstance(d.get("natural"), (int, float)) and d["natural"] >= 4 and d["self_contained"] is True
            and d["answerable_in_text"] is True and d["safe"] is True and d["needs_live_data"] is False
            and d["fits"] is True and d["names_trait"] is False)


def hkey(s):
    return hashlib.sha256(f"{SALT}|{s}".encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("setname")
    ap.add_argument("drafts", nargs="+")
    ap.add_argument("--no-rate", action="store_true", help="skip the DeepSeek rating (dry run of the rest)")
    a = ap.parse_args()
    out = dshbatch.DATA / "questions" / a.setname
    out.mkdir(parents=True, exist_ok=True)

    drafts, seen, rejects = [], set(), []
    for path in a.drafts:
        for l in open(path, encoding="utf-8"):
            if not l.strip():
                continue
            r = json.loads(l)
            norm = re.sub(r"\W", "", r["q"].lower())
            if norm in seen:
                rejects.append({**r, "reason": "exact duplicate"})
                continue
            seen.add(norm)
            why = script_check(r)
            if why:
                rejects.append({**r, "reason": why})
                continue
            drafts.append(r)

    if a.no_rate:
        ratings = {r["id"]: {"natural": 5, "self_contained": True, "answerable_in_text": True, "safe": True,
                             "needs_live_data": False, "fits": True, "names_trait": False, "topic": r["q"][:20], "dry_run": True} for r in drafts}
    else:
        reqs = [{"id": r["id"], "user": RATE_TEMPLATE.format(lang_name=LANG_NAME[r["lang"]], q=r["q"], intent=intent(r))} for r in drafts]
        res = dshbatch.run(f"rate-{a.setname}", reqs, concurrency=48)
        ratings = {i: parse_rating(v.get("text")) for i, v in res.items()}
    good = []
    for r in drafts:
        d = ratings.get(r["id"])
        r["rating"] = d
        if rating_ok(d):
            good.append(r)
        else:
            rejects.append({**r, "reason": "rating" if d else "rating unparsed"})

    seeds_doc = json.load(open(dshbatch.HERE / "seeds.json", encoding="utf-8"))
    seeds = [{"id": hashlib.sha256(f"{s['lang']}|{s['q']}".encode()).hexdigest()[:12], "lang": s["lang"], "trait": s["trait"] or "none",
              "mode": s["mode"], "q": s["q"], "source": src} for src in ("aa", "mine") for s in seeds_doc[src]]

    # Near-duplicate control and selection, per language.
    selected = []
    report_near = {}
    for lang in QUOTA:
        pool = [r for r in good if r["lang"] == lang]
        base = [s for s in seeds if s["lang"] == lang]
        texts = [r["q"] for r in base + pool]
        if not texts:
            continue
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=1).fit(texts)
        chosen_vecs = [vec.transform([s["q"]]) for s in base]
        topics = [str(r["rating"].get("topic", "")) for r in pool] or [""]
        tvec = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1, token_pattern=r"(?u)\w+").fit(topics + ["x"])
        chosen_topics = []
        cells = defaultdict(list)
        for r in pool:
            cells[(r["trait"], r["mode"])].append(r)
        skipped_near = 0
        for (trait, mode), rs in sorted(cells.items()):
            rs.sort(key=lambda r: (-r["rating"]["natural"], hkey(r["id"])))
            by_b = defaultdict(list)
            for r in rs:
                by_b[bucket(r)].append(r)
            order, k = [], 0
            while any(by_b.values()):  # short, medium, long in turn
                b = ("short", "medium", "long")[k % 3]
                if by_b[b]:
                    order.append(by_b[b].pop(0))
                k += 1
            taken = 0
            for r in order:
                if taken >= QUOTA[lang]:
                    break
                v = vec.transform([r["q"]])
                if chosen_vecs and max(float((v @ c.T).toarray()[0, 0]) for c in chosen_vecs) >= NEAR:
                    skipped_near += 1
                    rejects.append({**r, "reason": "near duplicate"})
                    continue
                tv = tvec.transform([str(r["rating"].get("topic", ""))])
                if tv.nnz and chosen_topics and max(float((tv @ c.T).toarray()[0, 0]) for c in chosen_topics) >= TOPIC_NEAR:
                    skipped_near += 1
                    rejects.append({**r, "reason": "same topic"})
                    continue
                chosen_vecs.append(v)
                chosen_topics.append(tv)
                selected.append({**r, "source": "deepseek", "bucket": bucket(r)})
                taken += 1
        report_near[lang] = skipped_near

    # Split per (language, trait).
    for lang in QUOTA:
        for trait in TRAITS:
            for mode, first in (("invite", "tuning"), ("neutral", "heldout")):
                rs = sorted([r for r in selected if r["lang"] == lang and r["trait"] == trait and r["mode"] == mode], key=lambda r: hkey(r["id"]))
                other = "heldout" if first == "tuning" else "tuning"
                for i, r in enumerate(rs):
                    r["split"] = first if i % 2 == 0 else other
    for s in seeds:
        s["split"] = "tuning"
        s["bucket"] = bucket(s)
    allq = selected + seeds

    # Measured checks for the report (the verifier reads these; it never trusts the labels).
    vec_all = {}
    max_cos_within, max_cos_across = {}, {}
    for lang in QUOTA:
        rs = [r for r in allq if r["lang"] == lang]
        if len(rs) < 2:
            continue
        X = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)).fit_transform([r["q"] for r in rs])
        S = (X @ X.T).toarray()
        np.fill_diagonal(S, 0)
        max_cos_within[lang] = round(float(S.max()), 3)
        t = np.array([r["split"] == "tuning" for r in rs])
        max_cos_across[lang] = round(float(S[np.ix_(t, ~t)].max()), 3) if t.any() and (~t).any() else None

    def dump(name, rows):
        with open(out / name, "w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    dump("all.jsonl", allq)
    dump("tuning.jsonl", [r for r in allq if r["split"] == "tuning"])
    dump("heldout.jsonl", [r for r in allq if r["split"] == "heldout"])
    dump("rejects.jsonl", rejects)

    gen = [r for r in allq if r["source"] == "deepseek"]
    cell_counts = Counter((r["lang"], r["trait"], r["mode"]) for r in gen)
    short = {f"{l}|{t}|{m}": QUOTA[l] - cell_counts.get((l, t, m), 0) for l in QUOTA for t in TRAITS for m in ("invite", "neutral")
             if cell_counts.get((l, t, m), 0) < QUOTA[l]}
    report = {
        "set": a.setname, "drafts_in": len(drafts) + sum(1 for r in rejects if r["reason"] in ("exact duplicate", "language script mismatch", "length out of bounds", "url", "multi-line")),
        "rated": len(drafts), "rating_dry_run": a.no_rate, "passed_rating": len(good),
        "rejects_by_reason": Counter(r["reason"] for r in rejects),
        "selected_generated": len(gen), "seeds": len(seeds), "total": len(allq),
        "by_lang": Counter(r["lang"] for r in allq), "by_split": Counter(r["split"] for r in allq),
        "by_split_generated": Counter(r["split"] for r in gen),
        "by_mode_generated": Counter(r["mode"] for r in gen),
        "by_trait_generated": Counter(r["trait"] for r in gen),
        "by_bucket_lang": {l: Counter(r["bucket"] for r in allq if r["lang"] == l) for l in QUOTA},
        "script_lang_mismatch": sum(1 for r in allq if metrics.detect_lang(r["q"]) != r["lang"]),
        "near_skipped": report_near, "max_cos_within_lang": max_cos_within, "max_cos_tuning_vs_heldout": max_cos_across,
        "public_or_seed_in_heldout": sum(1 for r in allq if r["source"] != "deepseek" and r["split"] == "heldout"),
        "id_overlap_tuning_heldout": len({r["id"] for r in allq if r["split"] == "tuning"} & {r["id"] for r in allq if r["split"] == "heldout"}),
        "shortfall_cells": short,
        "sha256": {n: hashlib.sha256((out / n).read_bytes()).hexdigest() for n in ("all.jsonl", "tuning.jsonl", "heldout.jsonl")},
    }
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("total", "selected_generated", "seeds", "by_lang", "by_split_generated", "rejects_by_reason", "near_skipped")}, ensure_ascii=False))
    if short:
        print(f"{len(short)} cells short of quota; top up with gen_questions.py --traits/--langs and re-run")


if __name__ == "__main__":
    main()
