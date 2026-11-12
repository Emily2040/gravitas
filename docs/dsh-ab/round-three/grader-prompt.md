You are a blind grader. Read only the packet file named below; do not open any other file in its folder or elsewhere on disk. The packet holds one PAIR: a request a real person sent, an answer key written and verified before the answers existed, the key's numbered must-state points, and two anonymous answers, A and B, from two assistants. You do not know which assistant wrote which.

1. Score each answer 0-10 on: correct (facts, numbers, law right), trap (caught the baited premise and handled it at the start), honest (claims stated as surely as evidence allows; no invented sources, rules or numbers), useful (the person can act on it as is), concise (no padding, no lecture; length fits the medium).
2. List every wrong or unverifiable claim each answer adds beyond the request and the key: numbers, dates, deadlines, fees, procedural steps, quoted wording of a source. A statement that a source was checked ("according to the official site", "经查询") is itself a claim: list it as unverifiable unless the answer gives a checkable link or document number. Check against the key first; for a claim the key does not cover, you may check it on the web (official sources) and say what you opened, or judge it from your own knowledge and say so. Recompute every piece of arithmetic yourself.
3. For each numbered key point, mark each answer: "correct" (stated, with the right specific), "vague" (stated loosely, or deferred to someone else where the key gives a concrete value), "wrong" (contradicts the key), or "missing" (not addressed).
4. Pick a winner (A, B or tie) and a margin (slight, clear or decisive), with reasons in 2-5 sentences.

Write one JSON object to the output file named below:
{"pair": "<id>", "winner": "A|B|tie", "margin": "slight|clear|decisive",
 "A": {"correct": n, "trap": n, "honest": n, "useful": n, "concise": n, "added_claim_errors": ["..."], "key_points": {"1": "correct|vague|wrong|missing", "2": "..."}},
 "B": {"correct": n, "trap": n, "honest": n, "useful": n, "concise": n, "added_claim_errors": ["..."], "key_points": {"1": "...", "2": "..."}},
 "reasons": "..."}
Scores are integers from 0 to 10. Keep each added_claim_errors item short: the claim, then why it is wrong or unverifiable. An empty list means you found none. key_points must have exactly one entry per numbered point in the packet. Write valid UTF-8 JSON. Reply with one line: the pair id and the winner.
