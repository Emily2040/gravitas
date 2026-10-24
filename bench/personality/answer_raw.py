#!/usr/bin/env python3
"""Answer questions with the bare model, outside the harness, through dshbatch.

Usage: answer_raw.py QUESTIONS.jsonl ARM
  raw-flash        deepseek-flash, a single user message and no system prompt
                   (AA-PersonalityBench's condition).
  raw-rule:NAME    the same with the Gravitas rule in DATA/rules/NAME/<lang>.md as the
                   system prompt: a quick, cheap proxy used to screen rule candidates on
                   the tuning split before they are run through the harness.
Writes DATA/answers/<ARM with : as _>/<qid>.{txt,json}.
"""
import argparse
import json

import dshbatch

GLANG = {"zh": "zh-CN", "en": "en", "ja": "ja", "ko": "ko"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("questions")
    ap.add_argument("arm")
    ap.add_argument("--concurrency", type=int, default=32)
    a = ap.parse_args()
    qs = [json.loads(l) for l in open(a.questions, encoding="utf-8") if l.strip()]
    outdir = dshbatch.DATA / "answers" / a.arm.replace(":", "_")
    outdir.mkdir(parents=True, exist_ok=True)
    rules = {}
    if a.arm.startswith("raw-rule:"):
        name = a.arm.split(":", 1)[1]
        for lang, g in GLANG.items():
            rules[lang] = (dshbatch.DATA / "rules" / name / f"{g}.md").read_text(encoding="utf-8")
    elif a.arm != "raw-flash":
        raise SystemExit(f"unknown arm {a.arm}")
    todo = [q for q in qs if not (outdir / f"{q['id']}.txt").exists() or not (outdir / f"{q['id']}.txt").read_text(encoding="utf-8").strip()]
    reqs = [{"id": q["id"], "user": q["q"], **({"system": rules[q["lang"]]} if rules else {})} for q in todo]
    res = dshbatch.run(f"answers-{a.arm.replace(':', '_')}-{dshbatch.time.strftime('%Y%m%d-%H%M%S')}", reqs, concurrency=a.concurrency) if reqs else {}
    for q in todo:
        r = res.get(q["id"], {})
        text = (r.get("text") or "").strip()
        (outdir / f"{q['id']}.txt").write_text(text, encoding="utf-8", newline="\n")
        (outdir / f"{q['id']}.json").write_text(json.dumps({"qid": q["id"], "lang": q["lang"], "arm": a.arm, "chars": len(text),
                                                           "usage": r.get("usage"), "error": r.get("error")}, ensure_ascii=False), encoding="utf-8")
    t = dshbatch.usage_totals(res) if res else {}
    print(json.dumps({"arm": a.arm, "answered": len(todo), "usage": t, "usd_offpeak": round(dshbatch.cost_usd(t), 4) if t else 0}))


if __name__ == "__main__":
    main()
