"""Build round-five blind packets, one pair per file, from the pair list (never by splitting text).

    python make_pairs5.py             -> blind/packets/<pid>.md, blind-map.json
    python make_pairs5.py --base DIR  build in DIR instead
    python make_pairs5.py --selftest  check this script on made-up data in a temporary folder

Sets: main (gv-grav-c5 vs gv-plain), base (gv-grav-base vs gv-plain), attr (gv-grav-c5 vs gv-grav-base),
per case and round; aa-plain (gv-plain r1 vs r2) and aa-c5 (gv-grav-c5 r1 vs r2), per case.
A/B is balanced by design (alternating by case and round); pair ids are opaque and shuffled with a seed;
every answer is checked to appear in its packet exactly once and in full.

Amendment 2026-10-25 (integrity):
- each blind-map entry stores the sha256 of each packaged answer (A_sha256, B_sha256: the final read as UTF-8 and
  stripped, as packaged); verdict5-amended.py rechecks them against raw/;
- an answer that names an arm or the harness (gv-plain, gv-grav..., gravitas-dsh, AgentData, r5-...) is refused, so no
  packet can tell a judge which arm wrote it;
- a final that is still blank after its one rerun (its run is in reruns.json) is packaged as the placeholder
  "(no answer: the run produced no final text)", so it loses its pairs instead of stopping the build; a blank final
  that has not been rerun still stops it.
"""
import argparse
import glob
import hashlib
import json
import os
import random
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDER = "(no answer: the run produced no final text)"
LEAK = re.compile(r"gv-(plain|grav)|gravitas-dsh|AgentData|\br5-")


def build(B):
    raw = os.path.join(B, "raw")
    cases = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(B, "prompts", "*.txt")))
    if not (len(cases) == 12 and all(sum(c.startswith(l + "-") for c in cases) == 3 for l in ("zh", "en", "ja", "ko"))):
        raise SystemExit("prompts/ does not hold 3 cases per language: %s" % cases)
    rp = os.path.join(B, "reruns.json")
    reruns = set(json.load(open(rp, encoding="utf-8"))) if os.path.exists(rp) else set()

    def text(case, arm, rnd):
        p = os.path.join(raw, "%s.%s.%s.txt" % (case, arm, rnd))
        t = open(p, encoding="utf-8").read().strip()
        if not t:
            if "%s.%s.%s" % (case, arm, rnd) in reruns:
                return PLACEHOLDER
            raise SystemExit("empty answer: %s (not yet rerun; run validity5.py --archive-invalid and the rerun first)" % p)
        m = LEAK.search(t)
        if m:
            raise SystemExit("answer %s names an arm or the harness (%r); it cannot be packaged blind" % (p, m.group()))
        return t

    pairs = []
    for i, case in enumerate(cases):
        for j, rnd in enumerate(("r1", "r2")):
            first = (i + j) % 2 == 0
            for set_name, x, y in (("main", "gv-grav-c5", "gv-plain"), ("base", "gv-grav-base", "gv-plain"), ("attr", "gv-grav-c5", "gv-grav-base")):
                a = (x, rnd, text(case, x, rnd))
                b = (y, rnd, text(case, y, rnd))
                pairs.append((set_name, case, rnd) + ((a, b) if first else (b, a)))
        for set_name, arm in (("aa-plain", "gv-plain"), ("aa-c5", "gv-grav-c5")):
            a1 = (arm, "r1", text(case, arm, "r1"))
            a2 = (arm, "r2", text(case, arm, "r2"))
            pairs.append((set_name, case, "r1r2") + ((a1, a2) if i % 2 == 0 else (a2, a1)))

    ids = ["p%03d" % (n + 1) for n in range(len(pairs))]
    random.Random(20261026 + 5).shuffle(ids)
    out = os.path.join(B, "blind", "packets")
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, "*.md")):
        os.remove(f)
    blind_map = {}
    for pid, (set_name, case, rnd, A, B_) in sorted(zip(ids, pairs)):
        prompt = open(os.path.join(B, "prompts", case + ".txt"), encoding="utf-8").read().strip()
        key = open(os.path.join(B, "keys", case + ".md"), encoding="utf-8").read().strip()
        points = json.load(open(os.path.join(B, "keypoints", case + ".json"), encoding="utf-8"))
        body = "\n\n".join([
            "# PAIR %s" % pid,
            "## Request\n\n````text\n%s\n````" % prompt,
            "## Answer key\n\n%s" % key,
            "## Key points\n\n%s" % "\n".join("%s. %s" % (p["id"], p["point"]) for p in points),
            "## Answer A\n\n````text\n%s\n````" % A[2],
            "## Answer B\n\n````text\n%s\n````" % B_[2],
        ]) + "\n"
        for t in (A[2], B_[2]):
            if body.count(t) != (2 if A[2] == B_[2] else 1):
                raise SystemExit("answer not present exactly once in %s" % pid)
        with open(os.path.join(out, pid + ".md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        entry = {"set": set_name, "case": case, "round": rnd, "A": A[0], "B": B_[0],
                 "A_sha256": hashlib.sha256(A[2].encode("utf-8")).hexdigest(),
                 "B_sha256": hashlib.sha256(B_[2].encode("utf-8")).hexdigest()}
        if set_name.startswith("aa-"):
            entry.update({"A_round": A[1], "B_round": B_[1]})
        blind_map[pid] = entry
    with open(os.path.join(B, "blind-map.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(blind_map, fh, indent=1, sort_keys=True)
    by_set = {}
    for e in blind_map.values():
        by_set[e["set"]] = by_set.get(e["set"], 0) + 1
    placeholders = sum(1 for _, _, _, A, B_ in pairs for t in (A[2], B_[2]) if t == PLACEHOLDER)
    print("%d pairs: %s; every answer present in full; answer sha256 stored; %d placeholder answers" % (
        len(blind_map), by_set, placeholders))
    return blind_map


def selftest():
    res = []

    def expect(label, cond, info=""):
        print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + info) if info else ""))
        res.append(bool(cond))

    root = tempfile.mkdtemp(prefix="make-pairs4-selftest-")
    cases = ["%s-c%d" % (lg, i) for lg in ("zh", "en", "ja", "ko") for i in range(3)]

    def setup():
        for f in os.listdir(root):
            q = os.path.join(root, f)
            shutil.rmtree(q) if os.path.isdir(q) else os.remove(q)
        for d in ("prompts", "keys", "keypoints", "raw"):
            os.makedirs(os.path.join(root, d))
        for c in cases:
            open(os.path.join(root, "prompts", c + ".txt"), "w", encoding="utf-8").write("request %s\n" % c)
            open(os.path.join(root, "keys", c + ".md"), "w", encoding="utf-8").write("key %s\n" % c)
            json.dump([{"id": "1", "point": "p"}], open(os.path.join(root, "keypoints", c + ".json"), "w", encoding="utf-8"))
            for arm in ("gv-plain", "gv-grav-base", "gv-grav-c5"):
                for r in ("r1", "r2"):
                    open(os.path.join(root, "raw", "%s.%s.%s.txt" % (c, arm, r)), "w", encoding="utf-8").write(
                        "  answer of %s %s %s  \n" % (c, arm[-4:], r))

    def built():
        try:
            return build(root), None
        except SystemExit as e:
            return None, str(e)

    try:
        setup()
        m, err = built()
        e = next(v for v in m.values() if v["set"] == "main" and v["case"] == "zh-c0" and v["round"] == "r1") if m else None
        a_arm = e["A"][-4:] if e else ""
        want = hashlib.sha256(("answer of zh-c0 %s r1" % a_arm).encode("utf-8")).hexdigest()
        expect("route (d): every blind-map entry stores the sha256 of each packaged (stripped) answer",
               m is not None and len(m) == 96 and all("A_sha256" in v and "B_sha256" in v for v in m.values())
               and e["A_sha256"] == want, err or "")
        for leak in ("see W:\\AgentData\\logs", "the gv-plain profile", "gv-grav-c5 here", "gravitas-dsh-ab5", "cwd r5-zh-c0"):
            setup()
            open(os.path.join(root, "raw", "en-c1.gv-plain.r2.txt"), "w", encoding="utf-8").write("answer " + leak)
            m, err = built()
            expect("route (d): an answer naming the arm or harness is refused (%r)" % leak,
                   m is None and "names an arm or the harness" in (err or ""), err or "")
        setup()
        open(os.path.join(root, "raw", "ja-c2.gv-grav-c5.r1.txt"), "w", encoding="utf-8").write("  \n")
        m, err = built()
        expect("a blank final not yet rerun stops the build", m is None and "not yet rerun" in (err or ""), err or "")
        json.dump(["ja-c2.gv-grav-c5.r1"], open(os.path.join(root, "reruns.json"), "w", encoding="utf-8"))
        m, err = built()
        e = next((v for v in (m or {}).values() if v["set"] == "main" and v["case"] == "ja-c2" and v["round"] == "r1"), None)
        side = "A" if e and e["A"] == "gv-grav-c5" else "B"
        expect("route (d): a final still blank after its rerun is packaged as the placeholder",
               e is not None and e[side + "_sha256"] == hashlib.sha256(PLACEHOLDER.encode("utf-8")).hexdigest(), err or "")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("selftest: %d assertions, %d failed" % (len(res), res.count(False)))
    return 0 if all(res) else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=HERE)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    build(os.path.abspath(a.base))
