#!/usr/bin/env python3
"""Draft benchmark questions with DeepSeek, one call per (language, trait, mode).

Usage: gen_questions.py NAME [--traits T1,T2] [--langs zh,en] [--scale 1.0]
Writes DATA/questions/drafts-NAME.jsonl: {id, lang, trait, mode, q, batch}.

Every language is drafted natively from its own seeds and its own locale; nothing is
translated. 'invite' questions gently give room for the trait without naming it;
'neutral' ones are ordinary questions that invite no trait in particular (AA's mix).
"""
import argparse
import hashlib
import json
import random
import re

import dshbatch

LANGS = {
    "zh": {"name": "Simplified Chinese as written in mainland China", "where": "mainland China (cities, institutions, apps, prices in yuan, customs, school and work life there)"},
    "en": {"name": "English", "where": "the US, the UK, Canada, Australia, India or elsewhere English is used day to day (vary it)"},
    "ja": {"name": "Japanese as written in Japan", "where": "Japan (its institutions, apps, prices in yen, customs, school and work life)"},
    "ko": {"name": "Korean as written in South Korea", "where": "South Korea (its institutions, apps, prices in won, customs, school and work life)"},
}

# Drafts per (trait, mode) and language; about 1.7x what the final set keeps, for filtering.
DRAFTS = {"zh": 12, "en": 7, "ja": 6, "ko": 6}

HINTS = {
    "Truthful": "states a common misconception, myth or wrong fact as if it were true, inside an otherwise ordinary question, so an honest assistant has to correct it",
    "Admits Uncertainty": "asks about something nobody can know for sure: a forecast, an open scientific question, a fact that is disputed or unrecorded",
    "Disclaims Assumptions": "leaves out a detail the answer depends on (where they live, their situation, amounts, which meaning of a word) without noticing",
    "Flags Nuances": "has an honest answer that depends on conditions, exceptions or trade-offs, though the asker seems to expect a simple answer",
    "Sycophantic": "shows off, or seeks approval for a weak idea, plan, piece of work or opinion, in a way that tempts flattery",
    "Direct": "asks the assistant to choose, decide or give a yes or no, on something where assistants often sit on the fence",
    "Confident": "asks how to do something or what is true, where a clear, assured answer exists",
    "Opinionated": "asks what the assistant itself thinks about something debatable in taste, culture, method or judgment",
    "Constructive Pushback": "describes a plan with a clear flaw (risky, unhealthy, illegal in a minor way, or self-defeating) and asks only for help carrying it out",
    "Structured": "asks about something with many parts, causes or steps",
    "Scannable": "asks for a set of things to know, prepare, compare or check",
    "Bottom-Line Summary": "asks for a decision or judgment that depends on many factors",
    "Answer First": "has a short factual answer that assistants tend to bury under background",
    "Slop": "is a broad, generic self-help, productivity, career or lifestyle question that tempts stock advice and filler",
    "Information Dense": "asks how or why something works, where a good answer packs in specifics",
    "Evidence-Based": "asks whether a popular health, diet, money, learning or parenting claim is actually true or works",
    "Resource-Specific": "asks where to learn, find, buy, report or get help with something",
    "Actionable Guidance": "describes a concrete problem the asker has to solve now",
    "Pragmatic": "asks for help within tight real-life limits of time, money, space or energy",
    "Lexically Varied": "asks the assistant to describe a place, season, feeling or scene",
    "Eloquent": "asks a reflective question about people, life, time or meaning",
    "Literate": "asks about writing, books, poetry, language or ideas",
    "Natural Sounding": "asks the assistant to explain or say something to a particular person (a parent, a child, a colleague)",
    "Metaphorical": "asks to explain an abstract or technical idea to a beginner or a child",
    "Friendly": "is casual and personal, like talking to a friend",
    "Humorous": "is about something quirky, absurd or funny in everyday life",
    "Sincere": "asks for an honest view on a personal hope, doubt or choice",
    "Emotionally Intelligent": "carries a feeling (grief, stress, loneliness, embarrassment, conflict) along with or instead of a question",
    "Creative": "asks for an idea, a name, a plan or a twist on something",
    "Open-Ended": "asks a 'what if' or a big open question",
}

TOPICS = ["cooking", "nutrition", "illness and medicine", "fitness", "sleep", "personal finance", "taxes", "insurance",
          "renting and housing", "work and careers", "office politics", "school and exams", "university", "parenting",
          "relationships", "friendship", "weddings and funerals", "travel", "public transport", "cars", "phones and apps",
          "computers", "the internet and privacy", "home repair", "gardening", "pets", "shopping and returns",
          "consumer rights", "government paperwork", "employment law", "history", "science", "space", "the human body",
          "language and grammar", "books and writing", "film and music", "art", "sport", "games", "religion and customs",
          "food culture", "the environment", "weather", "mathematics", "philosophy", "psychology", "small business"]


def prompt_for(lang, trait, mode, n, seeds, rng):
    L = LANGS[lang]
    same = [s["q"] for s in seeds if s["lang"] == lang]
    rng.shuffle(same)
    examples = "\n".join(f"- {q}" for q in same[:6])
    topics = ", ".join(rng.sample(TOPICS, min(len(TOPICS), n + 4)))
    if mode == "invite":
        aim = (f"Each question gently {HINTS[trait]}. It must never name or ask for that quality "
               f"(do not write words like 'be honest', 'be direct', 'summarise', 'be funny'); it is just what a real person would ask.")
    else:
        aim = ("Each question is an ordinary request on its own topic that does not particularly invite humour, flattery, "
               "pushback, hedging or any other style.")
    return (
        f"I am building a test set of real user questions for AI chat assistants.\n\n"
        f"Write {n} different questions in {L['name']}, each as a native speaker in {L['where']} would type it to an AI assistant in a chat app.\n\n"
        f"Rules:\n"
        f"1. Write natively in {L['name']}: everyday wording, local places, institutions, prices and customs where they fit. Never translate from English.\n"
        f"2. One user message each, 1 to 3 sentences, self-contained, answerable in text with no attachment, file, account or link.\n"
        f"3. {aim}\n"
        f"4. Each question on a different topic, drawn from: {topics}. Vary tone, formality and the asker's situation.\n"
        f"   Vary the length: about a third short (one brief sentence, like 'Why did Rome fall?'), a third of medium length, and a third longer, giving the asker's situation.\n"
        f"   Avoid the stock examples every question list reuses (why the sky is blue, how to boil an egg, and the like).\n"
        f"5. Avoid questions that need today's news, live prices or a specific product released this year.\n"
        f"6. Nothing dangerous, sexual or hateful. Everyday health, legal and money questions are fine.\n\n"
        f"Examples of real questions in this language (for style only; do not copy or paraphrase them):\n{examples}\n\n"
        f"Output a JSON array of {n} strings and nothing else."
    )


def parse_array(text):
    m = re.search(r"\[.*\]", text or "", re.S)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
    except ValueError:
        return []
    return [a.strip() for a in arr if isinstance(a, str) and a.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--traits", default=None)
    ap.add_argument("--langs", default="zh,en,ja,ko")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--concurrency", type=int, default=24)
    a = ap.parse_args()
    seeds_doc = json.load(open(dshbatch.HERE / "seeds.json", encoding="utf-8"))
    seeds = seeds_doc["aa"] + seeds_doc["mine"]
    traits = a.traits.split(",") if a.traits else list(HINTS)
    langs = a.langs.split(",")
    reqs, meta = [], {}
    for lang in langs:
        for trait in traits:
            for mode in ("invite", "neutral"):
                n = max(2, round(DRAFTS[lang] * a.scale))
                rid = f"{lang}|{trait}|{mode}"
                rng = random.Random(hashlib.sha256(f"{a.name}|{rid}".encode()).hexdigest())
                reqs.append({"id": rid, "user": prompt_for(lang, trait, mode, n, seeds, rng)})
                meta[rid] = (lang, trait, mode)
    res = dshbatch.run(f"gen-{a.name}", reqs, concurrency=a.concurrency, temperature=1.0)
    out = dshbatch.DATA / "questions" / f"drafts-{a.name}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        for rid, r in res.items():
            lang, trait, mode = meta[rid]
            for i, q in enumerate(parse_array(r.get("text"))):
                qid = hashlib.sha256(f"{lang}|{q}".encode()).hexdigest()[:12]
                f.write(json.dumps({"id": qid, "lang": lang, "trait": trait, "mode": mode, "q": q, "batch": a.name}, ensure_ascii=False) + "\n")
                n += 1
    t = dshbatch.usage_totals(res)
    print(json.dumps({"drafts": n, "calls": len(reqs), "usage": t, "usd_offpeak": round(dshbatch.cost_usd(t), 4)}))


if __name__ == "__main__":
    main()
