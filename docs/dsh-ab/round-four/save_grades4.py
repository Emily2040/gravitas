#!/usr/bin/env python3
"""Save grades for the three judges, keep the append-only grade ledger, and check every (pair, judge).

    python save_grades4.py <workflow-output> [...]       log every opus/sonnet row to ledger.jsonl and save the valid
                                                         ones that are the first valid grade for their pair and judge;
                                                         then check every (pair, judge); exit 1 if any is missing,
                                                         malformed or not the first valid ledger grade
    python save_grades4.py --replace REASON <output> ... a valid row that differs from the first valid grade is used
                                                         instead, after a replace record with REASON in the ledger
    python save_grades4.py                               check only (--judge J: one judge)
    python save_grades4.py --record JUDGE PID            log blind/grades/JUDGE/PID.json (judge_codex.sh, after each
                                                         session; the session's prompt must be the frozen one)
    python save_grades4.py --check JUDGE PID             exit 0 if that grade is valid and is the first valid ledger grade
    python save_grades4.py --todo JUDGE                  pids of blind/packets/*.md with no valid ledger grade from JUDGE
    python save_grades4.py --retire JUDGE PID REASON     log a replace record: the next valid grade received is used
    python save_grades4.py --restore                     rewrite grade files from their first valid ledger grade
    python save_grades4.py --schema PID OUT              write the strict JSON schema of PID's grade (codex --output-schema)
    python save_grades4.py --selftest                    check this script on made-up data in a temporary folder
    --base DIR                                           the round folder (default: the folder this script is in)

A workflow output (workflows/grade4.js) is a JSON object whose "result" is a list of {"pid", "grader", "grade",
"prompt", "packetPath"}, or such a list itself; grader is "opus" or "sonnet". A row is valid only if its prompt is
exactly grader-prompt4.md (beside this script, trailing whitespace removed) plus grade4.js's frozen delivery lines,
its packetPath is blind/packets/<pid>.md of the round folder, and the grade has the grader prompt's format:
one JSON object; "pair" equals the pid; "winner" exactly A, B or tie; "margin" exactly slight, clear or decisive;
"reasons" a non-empty string; A and B each with the five scores as integers 0-10, "added_claim_errors" a list of
non-empty strings, and "key_points" with exactly the ids of keypoints/<case>.json, each exactly correct, vague, wrong
or missing. Codex grades are the files judge_codex.sh wrote; --record logs each one with its packet's hash and
checks that the session got grader-prompt4.md plus judge_codex.sh's frozen delivery lines and the current packet.

The ledger (ledger.jsonl, append-only; amendment 2026-10-25) gets every grade received, valid or not, with its time,
pid, judge and the packet's sha256. The grade used for a (pair, judge) is the first valid ledger entry after the last
replace record for it, and the file must equal it; verdict4-amended.py checks the same and fails the grade as metric
missing otherwise. Re-grade counts per set and by the arm the first valid grade picked are printed. Standard library
only.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
GRADER_PROMPT = os.path.join(HERE, "grader-prompt4.md")
LEDGER_FILE = "ledger.jsonl"
JUDGES = ("opus", "sonnet", "codex")
CLAUDE_GRADERS = ("opus", "sonnet")
DIMS = ("correct", "trap", "honest", "useful", "concise")
MARKS = ("correct", "vague", "wrong", "missing")
WINNERS = ("A", "B", "tie")
MARGINS = ("slight", "clear", "decisive")
# The delivery lines after the grader prompt, frozen with workflows/grade4.js and judge_codex.sh.
CLAUDE_DELIVERY = ("\n\nPacket file: {path}\nOutput: do not write any file. Return the JSON object described above through "
                   "the StructuredOutput tool, with \"pair\" set to \"{pid}\". Do not open any other file in {dir} or its "
                   "parent folders, and do not look for other packets, runs, maps or grades.")
CODEX_DELIVERY = ("\nPacket: given in full below, between the lines BEGIN PACKET and END PACKET. Do not open any file on "
                  "disk.\nOutput: your whole final reply is the JSON object described above, with \"pair\" set to "
                  "\"{pid}\", and nothing before or after it.\n\nBEGIN PACKET\n{packet}\nEND PACKET\n")


def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def read_exact(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


class Round:
    def __init__(self, base):
        self.base = base
        self.map = load_json(os.path.join(base, "blind-map.json"))
        self._kp = {}

    def kp_ids(self, pid):
        """The case's key-point ids for pid, or raise ValueError with the reason."""
        e = self.map.get(pid)
        if not isinstance(e, dict) or not isinstance(e.get("case"), str):
            raise ValueError("pid %s is not in blind-map.json" % pid)
        case = e["case"]
        if case not in self._kp:
            pts = load_json(os.path.join(self.base, "keypoints", case + ".json"))
            ids = [str(p["id"]) for p in pts]
            if not ids or len(set(ids)) != len(ids):
                raise ValueError("keypoints/%s.json ids missing or repeated" % case)
            self._kp[case] = ids
        return self._kp[case]

    def grade_path(self, judge, pid):
        return os.path.join(self.base, "blind", "grades", judge, pid + ".json")

    def packet_path(self, pid):
        return os.path.join(self.base, "blind", "packets", pid + ".md")

    def packet_sha(self, pid):
        return sha256_file(self.packet_path(pid))

    # ---- ledger
    def ledger_path(self):
        return os.path.join(self.base, LEDGER_FILE)

    def append(self, entries):
        """Append entries to the ledger under a mkdir lock (judge_codex.sh records from three workers at once)."""
        lock = self.ledger_path() + ".lock"
        for _ in range(200):
            try:
                os.mkdir(lock)
                break
            except FileExistsError:
                time.sleep(0.05)
        else:
            raise SystemExit("ledger lock %s held for 10 s; remove it if no save is running" % lock)
        try:
            with open(self.ledger_path(), "a", encoding="utf-8", newline="\n") as f:
                for e in entries:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
        finally:
            os.rmdir(lock)

    def ledger(self):
        """{(pid, judge): {"entries", "valid_entries", "replaces", "ref"}}, the reference being the first valid
        grade entry after the last replace record. Raises ValueError on an unreadable line."""
        slots = {}
        if not os.path.isfile(self.ledger_path()):
            return slots
        with open(self.ledger_path(), encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    e = json.loads(line)
                except ValueError:
                    raise ValueError("%s line %d is not valid JSON" % (LEDGER_FILE, i))
                if not isinstance(e, dict):
                    raise ValueError("%s line %d is not an object" % (LEDGER_FILE, i))
                if e.get("kind") not in ("grade", "replace"):
                    continue
                s = slots.setdefault((e.get("pid"), e.get("judge")), {"entries": 0, "valid_entries": 0, "replaces": 0,
                                                                       "ref": None})
                if e["kind"] == "replace":
                    s["replaces"] += 1
                    s["ref"] = None
                else:
                    s["entries"] += 1
                    if e.get("valid") is True:
                        s["valid_entries"] += 1
                        if s["ref"] is None:
                            s["ref"] = e
        return slots


def problems(g, pid, ids):
    """Everything wrong with grade object g for pair pid; empty when valid."""
    if not isinstance(g, dict):
        return ["not a JSON object"]
    out = []
    if g.get("pair") != pid:
        out.append("pair %r is not %s" % (g.get("pair"), pid))
    if g.get("winner") not in WINNERS:
        out.append("winner %r" % (g.get("winner"),))
    if g.get("margin") not in MARGINS:
        out.append("margin %r" % (g.get("margin"),))
    if not (isinstance(g.get("reasons"), str) and g["reasons"].strip()):
        out.append("reasons missing")
    for side in "AB":
        s = g.get(side)
        if not isinstance(s, dict):
            out.append("%s missing" % side)
            continue
        for d in DIMS:
            v = s.get(d)
            if not (isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 10):
                out.append("%s.%s = %r" % (side, d, v))
        notes = s.get("added_claim_errors")
        if not (isinstance(notes, list) and all(isinstance(x, str) and x.strip() for x in notes)):
            out.append("%s.added_claim_errors is not a list of non-empty strings" % side)
        kp = s.get("key_points")
        if not isinstance(kp, dict):
            out.append("%s.key_points missing" % side)
        else:
            if sorted(kp) != sorted(ids):
                out.append("%s.key_points ids %s are not the case's %s" % (side, sorted(kp), sorted(ids)))
            bad = sorted(k for k, v in kp.items() if v not in MARKS)
            if bad:
                out.append("%s.key_points marks not correct/vague/wrong/missing at %s" % (side, bad))
    return out


def grade_problems(R, pid, g):
    try:
        return problems(g, pid, R.kp_ids(pid))
    except (OSError, ValueError, KeyError, TypeError) as e:
        return ["key points unavailable (%s)" % e]


def claude_prompt_problems(R, pid, prompt, packet_path):
    """A workflow row must carry the exact prompt it was given and the round's own packet path."""
    if not isinstance(packet_path, str) or not isinstance(prompt, str):
        return ["the row has no prompt or packetPath (grade4.js returns both)"]
    want = os.path.normcase(os.path.abspath(R.packet_path(pid)))
    if os.path.normcase(os.path.abspath(packet_path)) != want:
        return ["packetPath %s is not blind/packets/%s.md of this round" % (packet_path, pid)]
    suffix = "\\%s.md" % pid
    if not packet_path.endswith(suffix):
        return ["packetPath %s does not end with %s" % (packet_path, suffix)]
    try:
        gp = read_exact(GRADER_PROMPT).rstrip()
    except OSError:
        return ["grader-prompt4.md missing beside save_grades4.py"]
    expected = gp + CLAUDE_DELIVERY.format(path=packet_path, pid=pid, dir=packet_path[:-len(suffix)])
    if prompt != expected:
        return ["the prompt is not grader-prompt4.md plus the frozen delivery lines"]
    return []


def codex_prompt_problems(R, pid):
    p = os.path.join(R.base, "judge-codex-runs", pid + ".prompt.txt")
    try:
        got = read_exact(p)
    except OSError:
        return ["judge-codex-runs/%s.prompt.txt missing" % pid]
    try:
        expected = read_exact(GRADER_PROMPT) + CODEX_DELIVERY.format(pid=pid, packet=read_exact(R.packet_path(pid)))
    except OSError as e:
        return ["cannot build the expected prompt (%s)" % e]
    return [] if got == expected else ["the session's prompt is not grader-prompt4.md plus the frozen delivery lines "
                                       "and the current packet"]


def check_file(R, judge, pid, slots=None):
    """(True, None) or (False, reason): the file is a valid grade and equals the first valid ledger grade, which was
    given the current packet."""
    p = R.grade_path(judge, pid)
    if not os.path.isfile(p):
        return False, "missing"
    try:
        g = load_json(p)
    except (OSError, UnicodeDecodeError) as e:
        return False, "unreadable (%s)" % e.__class__.__name__
    except ValueError:
        return False, "not valid JSON"
    pr = grade_problems(R, pid, g)
    if pr:
        return False, "; ".join(pr)
    try:
        slots = R.ledger() if slots is None else slots
    except ValueError as e:
        return False, "ledger unreadable (%s)" % e
    ref = (slots.get((pid, judge)) or {}).get("ref")
    if ref is None:
        return False, "no valid ledger entry (grade not received through this script)"
    if ref.get("grade") != g:
        return False, "not the first valid grade received for it (ledger)"
    if ref.get("packet_sha256") != R.packet_sha(pid) or R.packet_sha(pid) is None:
        return False, "blind/packets/%s.md is not the packet the grade was given" % pid
    return True, None


def workflow_results(path):
    data = load_json(path)
    data = data.get("result") if isinstance(data, dict) else data
    if not isinstance(data, list):
        raise ValueError("%s: no result list" % path)
    return data


def write_grade(R, judge, pid, grade):
    p = R.grade_path(judge, pid)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(grade, fh, ensure_ascii=False, indent=1)


def save(R, paths, replace_reason):
    """Log every row and save the grades in force. Returns (problems, notes); problems always fail the run."""
    probs, notes, written = [], [], 0
    try:
        slots = R.ledger()
    except ValueError as e:
        return ["ledger unreadable (%s); nothing saved" % e], notes
    for path in paths:
        try:
            rows = workflow_results(path)
        except (OSError, ValueError) as e:
            probs.append("cannot read workflow output %s: %s" % (path, e))
            continue
        for r in rows:
            if not isinstance(r, dict):
                probs.append("%s: a result entry is not an object" % path)
                continue
            pid, grader, grade = r.get("pid"), r.get("grader"), r.get("grade")
            if grader not in CLAUDE_GRADERS:
                probs.append("%s %s: grader must be opus or sonnet (codex grades come from judge_codex.sh)" % (pid, grader))
                continue
            if pid not in R.map:
                probs.append("%s %s: pid not in blind-map.json" % (pid, grader))
                continue
            ps = R.packet_sha(pid)
            pr = ["the workflow returned no grade"] if grade is None else \
                claude_prompt_problems(R, pid, r.get("prompt"), r.get("packetPath")) + grade_problems(R, pid, grade)
            if ps is None:
                pr.append("blind/packets/%s.md missing" % pid)
            entry = {"kind": "grade", "time": now(), "pid": pid, "judge": grader, "packet_sha256": ps,
                     "valid": not pr, "problems": pr, "grade": grade, "source": os.path.basename(path)}
            slot = slots.setdefault((pid, grader), {"entries": 0, "valid_entries": 0, "replaces": 0, "ref": None})
            ref = slot["ref"]
            if entry["valid"] and ref is not None and ref.get("grade") != grade:
                if replace_reason:
                    R.append([{"kind": "replace", "time": now(), "pid": pid, "judge": grader, "reason": replace_reason}])
                    slot["replaces"] += 1
                    slot["ref"] = ref = None
                else:
                    notes.append("%s %s: a different valid grade is already the first; this one is logged and not used "
                                 "(--replace REASON to use it)" % (pid, grader))
            R.append([entry])
            slot["entries"] += 1
            if not entry["valid"]:
                notes.append("%s %s: not valid, logged and not saved: %s" % (pid, grader, "; ".join(pr)))
                continue
            slot["valid_entries"] += 1
            if ref is None:
                slot["ref"] = entry
                write_grade(R, grader, pid, grade)
                written += 1
    print("logged every row to %s; saved %d grades in force" % (LEDGER_FILE, written))
    return probs, notes


def record(R, judge, pid):
    """Log the grade file judge_codex.sh just wrote; returns the entry."""
    p = R.grade_path(judge, pid)
    grade, pr = None, []
    try:
        grade = load_json(p)
    except (OSError, ValueError, UnicodeDecodeError) as e:
        pr.append("blind/grades/%s/%s.json unreadable or not plain JSON (%s)" % (judge, pid, e.__class__.__name__))
    if grade is not None:
        pr += grade_problems(R, pid, grade)
    if judge == "codex":
        pr += codex_prompt_problems(R, pid)
    ps = R.packet_sha(pid)
    if ps is None:
        pr.append("blind/packets/%s.md missing" % pid)
    entry = {"kind": "grade", "time": now(), "pid": pid, "judge": judge, "packet_sha256": ps, "valid": not pr,
             "problems": pr, "grade": grade, "source": "judge_codex.sh" if judge == "codex" else "file"}
    R.append([entry])
    return entry


def check_all(R, judges):
    bad = []
    try:
        slots = R.ledger()
    except ValueError as e:
        return [(pid, j, "ledger unreadable (%s)" % e) for pid in sorted(R.map) for j in judges], [], {}
    for pid in sorted(R.map):
        for j in judges:
            ok, why = check_file(R, j, pid, slots)
            if not ok:
                bad.append((pid, j, why))
    stray = []
    for j in judges:
        d = os.path.join(R.base, "blind", "grades", j)
        if os.path.isdir(d):
            stray += ["%s/%s" % (j, f) for f in sorted(os.listdir(d)) if f.endswith(".json") and f[:-5] not in R.map]
    return bad, stray, regrade_counts(R, slots, judges)


def regrade_counts(R, slots, judges):
    """Per set: (pair, judge) slots with more than one entry or a replace, entries beyond the first, replaces, and the
    arm the first valid grade picked."""
    out = {}
    for pid, e in R.map.items():
        for j in judges:
            s = slots.get((pid, j))
            if not s or (s["entries"] <= 1 and not s["replaces"]):
                continue
            ref = s["ref"]
            win = ref["grade"].get("winner") if ref and isinstance(ref.get("grade"), dict) else None
            arm = "tie" if win == "tie" else e.get(win) if win in ("A", "B") else "none"
            d = out.setdefault(e.get("set"), {"pair_judges": 0, "extra_entries": 0, "replaces": 0,
                                              "by_first_valid_winner": Counter()})
            d["pair_judges"] += 1
            d["extra_entries"] += max(s["entries"] - 1, 0)
            d["replaces"] += s["replaces"]
            d["by_first_valid_winner"][arm] += 1
    return out


def todo(R, judge):
    d = os.path.join(R.base, "blind", "packets")
    pids = sorted(f[:-3] for f in os.listdir(d) if f.endswith(".md")) if os.path.isdir(d) else []
    slots = R.ledger()
    out = []
    for pid in pids:
        if pid not in R.map:
            print("warning: packet %s is not in blind-map.json; skipped" % pid, file=sys.stderr)
            continue
        ref = (slots.get((pid, judge)) or {}).get("ref")
        if ref is None:
            out.append(pid)
        elif ref.get("packet_sha256") != R.packet_sha(pid):
            print("warning: %s %s was graded on another version of its packet; retire it (--retire) to grade it "
                  "again" % (judge, pid), file=sys.stderr)
    return out


def restore(R):
    n = 0
    for (pid, judge), s in R.ledger().items():
        ref = s["ref"]
        if ref is None or pid not in R.map:
            continue
        cur = None
        try:
            cur = load_json(R.grade_path(judge, pid))
        except (OSError, ValueError, UnicodeDecodeError):
            pass
        if cur != ref["grade"]:
            write_grade(R, judge, pid, ref["grade"])
            n += 1
    print("restored %d grade files from their first valid ledger grade" % n)


def schema(R, pid):
    ids = R.kp_ids(pid)
    side = {"type": "object", "additionalProperties": False,
            "required": list(DIMS) + ["added_claim_errors", "key_points"],
            "properties": dict({d: {"type": "integer", "enum": list(range(11))} for d in DIMS},
                               added_claim_errors={"type": "array", "items": {"type": "string"}},
                               key_points={"type": "object", "additionalProperties": False, "required": ids,
                                           "properties": {i: {"type": "string", "enum": list(MARKS)} for i in ids}})}
    return {"type": "object", "additionalProperties": False,
            "required": ["pair", "winner", "margin", "A", "B", "reasons"],
            "properties": {"pair": {"type": "string", "enum": [pid]},
                           "winner": {"type": "string", "enum": list(WINNERS)},
                           "margin": {"type": "string", "enum": list(MARGINS)},
                           "A": side, "B": side, "reasons": {"type": "string"}}}


def selftest():
    res = []

    def expect(label, cond, info=""):
        print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + info) if info else ""))
        res.append(bool(cond))

    root = tempfile.mkdtemp(prefix="save-grades4-selftest-")
    try:
        def wj(rel, obj):
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False)

        def write_packet(pid, extra=""):
            p = os.path.join(root, "blind", "packets", pid + ".md")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write("# PAIR %s\n\npacket text\n%s" % (pid, extra))

        wj("blind-map.json", {"p001": {"set": "main", "case": "ja-x", "A": "gv-grav-c4", "B": "gv-plain"},
                              "p002": {"set": "main", "case": "ko-y", "A": "gv-plain", "B": "gv-grav-c4"}})
        wj("keypoints/ja-x.json", [{"id": "1", "point": "a"}, {"id": "2", "point": "b"}])
        wj("keypoints/ko-y.json", [{"id": "1", "point": "a"}])
        for pid in ("p001", "p002", "p999"):
            write_packet(pid)
        gp = read_exact(GRADER_PROMPT).rstrip()

        def ppath(pid):
            return os.path.join(root, "blind", "packets") + "\\" + pid + ".md"

        def prompt(pid, path=None):
            path = path or ppath(pid)
            return gp + CLAUDE_DELIVERY.format(path=path, pid=pid, dir=path[:-len("\\%s.md" % pid)])

        def grade(pid, ids, **over):
            side = {"correct": 7, "trap": 8, "honest": 7, "useful": 7, "concise": 6, "added_claim_errors": ["x: not in the key"],
                    "key_points": {i: "correct" for i in ids}}
            g = {"pair": pid, "winner": "A", "margin": "clear", "A": dict(side), "B": dict(side), "reasons": "because"}
            g.update(over)
            return g

        def row(pid, grader, g, **over):
            r = {"pid": pid, "grader": grader, "grade": g, "prompt": prompt(pid), "packetPath": ppath(pid)}
            r.update(over)
            return r

        def output(name, rows):
            p = os.path.join(root, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"summary": "x", "result": rows}, f, ensure_ascii=False)
            return p

        R = Round(root)
        good1, good2 = grade("p001", ["1", "2"]), grade("p002", ["1"])
        expect("a well-formed grade has no problems", problems(good1, "p001", ["1", "2"]) == [])
        for label, g in (("winner 'a' (lower case)", grade("p001", ["1", "2"], winner="a")),
                         ("margin missing", {k: v for k, v in good1.items() if k != "margin"}),
                         ("pair of another pid", grade("p002", ["1", "2"])),
                         ("score 11", dict(good1, A=dict(good1["A"], trap=11))),
                         ("score True", dict(good1, A=dict(good1["A"], trap=True))),
                         ("score 7.0", dict(good1, A=dict(good1["A"], trap=7.0))),
                         ("an empty added-claim note", dict(good1, B=dict(good1["B"], added_claim_errors=[" "]))),
                         ("a key-point id too many", dict(good1, A=dict(good1["A"], key_points={"1": "correct", "2": "vague", "3": "wrong"}))),
                         ("a key-point mark 'Correct'", dict(good1, A=dict(good1["A"], key_points={"1": "Correct", "2": "vague"}))),
                         ("empty reasons", dict(good1, reasons=" ")),
                         ("an array instead of an object", [good1])):
            expect("malformed: %s" % label, problems(g, "p001", ["1", "2"]) != [])
        # route (a): the prompt and the packet path of a workflow row
        probs, notes = save(R, [output("wf1.json", [
            row("p001", "opus", good1, prompt=prompt("p001").replace("concise", "brief")),
            row("p001", "sonnet", good1, packetPath=os.path.join(root, "elsewhere") + "\\p001.md",
                prompt=prompt("p001", os.path.join(root, "elsewhere") + "\\p001.md")),
            row("p002", "opus", good2, prompt=None)])], None)
        expect("route (a): a row whose prompt was edited is logged as invalid and not saved",
               any("p001 opus: not valid" in n and "frozen delivery lines" in n for n in notes)
               and not os.path.exists(R.grade_path("opus", "p001")), str(notes)[:200])
        expect("route (a): a row whose packet is not blind/packets/<pid>.md is not saved",
               any("p001 sonnet: not valid" in n and "packetPath" in n for n in notes)
               and not os.path.exists(R.grade_path("sonnet", "p001")))
        expect("route (a): a row without its prompt is not saved", any("p002 opus: not valid" in n for n in notes))
        # route (b): the ledger
        probs, notes = save(R, [output("wf2.json", [row("p001", "opus", good1), row("p002", "sonnet", dict(good2, winner="maybe")),
                                                     row("p002", "opus", None), row("p001", "codex", good1)])], None)
        expect("a valid row is saved and is in force", check_file(R, "opus", "p001")[0])
        expect("a malformed grade is logged and not saved",
               any("p002 sonnet: not valid" in n for n in notes) and not os.path.exists(R.grade_path("sonnet", "p002")))
        expect("a null grade is logged", any("p002 opus" in n and "no grade" in n for n in notes))
        expect("a codex row in a workflow output is refused", any("p001 codex" in p for p in probs))
        n_lines = len(open(R.ledger_path(), encoding="utf-8").read().splitlines())
        expect("route (b): every row received is in the ledger, valid or not (6 rows so far)", n_lines == 6, str(n_lines))
        probs, notes = save(R, [output("wf3.json", [row("p001", "opus", dict(good1, winner="B"))])], None)
        expect("route (b): a later different valid grade is logged and not used without --replace",
               any("already the first" in n for n in notes) and load_json(R.grade_path("opus", "p001"))["winner"] == "A")
        with open(R.grade_path("opus", "p001"), "w", encoding="utf-8") as f:
            json.dump(dict(good1, winner="B"), f)
        expect("route (b): a grade file overwritten with the later grade fails the check",
               check_file(R, "opus", "p001") == (False, "not the first valid grade received for it (ledger)"))
        restore(R)
        expect("--restore puts the first valid grade back", check_file(R, "opus", "p001")[0]
               and load_json(R.grade_path("opus", "p001"))["winner"] == "A")
        save(R, [output("wf4.json", [row("p001", "opus", dict(good1, winner="B"))])], "the first session lost its tool")
        lines = [json.loads(l) for l in open(R.ledger_path(), encoding="utf-8")]
        expect("route (b): --replace REASON logs a replace record with the reason, then the new grade is in force",
               any(l["kind"] == "replace" and l["reason"] == "the first session lost its tool" for l in lines)
               and load_json(R.grade_path("opus", "p001"))["winner"] == "B" and check_file(R, "opus", "p001")[0])
        bad, stray, rc = check_all(R, JUDGES)
        expect("route (b): re-grade counts per set and by the first valid grade's arm",
               rc.get("main", {}).get("extra_entries") == 4 and rc["main"]["replaces"] == 1
               and rc["main"]["by_first_valid_winner"] == Counter({"gv-plain": 1, "none": 1}), str(rc))
        write_packet("p001", "edited\n")
        expect("a packet edited after grading fails the check",
               check_file(R, "opus", "p001") == (False, "blind/packets/p001.md is not the packet the grade was given"))
        write_packet("p001")
        # codex: the file in place, its session prompt, the ledger
        wj("blind/grades/codex/p001.json", good1)
        e = record(R, "codex", "p001")
        expect("--record: a codex grade whose session prompt is missing is logged as invalid",
               e["valid"] is False and any("prompt.txt missing" in x for x in e["problems"]))
        os.makedirs(os.path.join(root, "judge-codex-runs"), exist_ok=True)
        pf = os.path.join(root, "judge-codex-runs", "p001.prompt.txt")
        with open(pf, "w", encoding="utf-8", newline="") as f:
            f.write(read_exact(GRADER_PROMPT).replace("concise", "brief") +
                    CODEX_DELIVERY.format(pid="p001", packet=read_exact(R.packet_path("p001"))))
        e = record(R, "codex", "p001")
        expect("--record: a codex session given an edited grader prompt is logged as invalid",
               e["valid"] is False and any("frozen delivery lines" in x for x in e["problems"]))
        with open(pf, "w", encoding="utf-8", newline="") as f:
            f.write(read_exact(GRADER_PROMPT) + CODEX_DELIVERY.format(pid="p001", packet=read_exact(R.packet_path("p001"))))
        e = record(R, "codex", "p001")
        expect("--record: a codex grade with the frozen prompt and the current packet is valid and in force",
               e["valid"] is True and check_file(R, "codex", "p001")[0], str(e["problems"]))
        expect("todo codex lists p002 only (p001 has a valid ledger grade; p999 has no map entry)", todo(R, "codex") == ["p002"])
        with open(R.grade_path("codex", "p002"), "w", encoding="utf-8") as f:
            f.write("```json\n" + json.dumps(good2) + "\n```")
        expect("a fenced codex file is not valid", check_file(R, "codex", "p002") == (False, "not valid JSON"))
        wj("blind/grades/codex/p002.json", good2)
        expect("a valid codex file that was never recorded fails the check (not in the ledger)",
               check_file(R, "codex", "p002")[1].startswith("no valid ledger entry"))
        R.append([{"kind": "replace", "time": now(), "pid": "p001", "judge": "codex", "reason": "test"}])
        expect("--retire: after a replace record the pair is to be graded again", "p001" in todo(R, "codex"))
        bad, stray, rc = check_all(R, JUDGES)
        expect("check lists every missing, malformed or unledgered (pair, judge)",
               sorted((p, j) for p, j, _ in bad) == [("p001", "codex"), ("p001", "sonnet"), ("p002", "codex"),
                                                      ("p002", "opus"), ("p002", "sonnet")], str(bad))
        sc = schema(R, "p001")
        expect("schema: strict objects, the case's key-point ids, the pid fixed",
               sc["additionalProperties"] is False and sc["properties"]["pair"]["enum"] == ["p001"]
               and sc["properties"]["A"]["properties"]["key_points"]["required"] == ["1", "2"]
               and sc["properties"]["A"]["additionalProperties"] is False)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("selftest: %d assertions, %d failed" % (len(res), res.count(False)))
    return 0 if all(res) else 1


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outputs", nargs="*", help="workflow output files of the Claude graders")
    ap.add_argument("--base", default=HERE)
    ap.add_argument("--replace", metavar="REASON", help="use a valid row that differs from the first valid grade")
    ap.add_argument("--judge", choices=JUDGES, help="check only this judge")
    ap.add_argument("--check", nargs=2, metavar=("JUDGE", "PID"))
    ap.add_argument("--record", nargs=2, metavar=("JUDGE", "PID"))
    ap.add_argument("--todo", metavar="JUDGE", choices=JUDGES)
    ap.add_argument("--retire", nargs=3, metavar=("JUDGE", "PID", "REASON"))
    ap.add_argument("--restore", action="store_true")
    ap.add_argument("--schema", nargs=2, metavar=("PID", "OUT"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if a.replace is not None and not a.replace.strip():
        raise SystemExit("--replace needs a reason")
    R = Round(os.path.abspath(a.base))
    if a.record:
        e = record(R, *a.record)
        print("%s %s: logged, %s" % (a.record[1], a.record[0], "valid" if e["valid"] else "INVALID: " + "; ".join(e["problems"])))
        sys.exit(0 if e["valid"] else 1)
    if a.check:
        ok, why = check_file(R, a.check[0], a.check[1])
        if not ok:
            print("%s %s: %s" % (a.check[1], a.check[0], why))
        sys.exit(0 if ok else 1)
    if a.todo:
        print("\n".join(todo(R, a.todo)))
        sys.exit(0)
    if a.retire:
        j, pid, reason = a.retire
        if j not in JUDGES or pid not in R.map or not reason.strip():
            raise SystemExit("--retire JUDGE PID REASON: a judge of the panel, a mapped pid and a reason")
        R.append([{"kind": "replace", "time": now(), "pid": pid, "judge": j, "reason": reason}])
        print("%s %s retired: the next valid grade received is used (%s)" % (pid, j, reason))
        sys.exit(0)
    if a.restore:
        restore(R)
    if a.schema:
        with open(a.schema[1], "w", encoding="utf-8", newline="\n") as f:
            json.dump(schema(R, a.schema[0]), f, ensure_ascii=False, indent=1)
        sys.exit(0)
    probs, notes = save(R, a.outputs, a.replace) if a.outputs else ([], [])
    judges = (a.judge,) if a.judge else JUDGES
    bad, stray, rc = check_all(R, judges)
    for p in notes:
        print("note: " + p)
    for p in probs:
        print("problem: " + p)
    for pid, j, why in bad:
        print("%s %s: %s" % (pid, j, why))
    for s in stray:
        print("warning: grade file with no blind-map entry: %s" % s)
    for s, d in sorted(rc.items()):
        print("re-grades in %s: %d (pair, judge) slots, %d entries beyond the first, %d replaces; first valid grade "
              "picked %s" % (s, d["pair_judges"], d["extra_entries"], d["replaces"], dict(d["by_first_valid_winner"])))
    print("%d pairs x %d judges (%s): %d missing, malformed or not the first valid ledger grade; %d problems in the "
          "workflow outputs" % (len(R.map), len(judges), ", ".join(judges), len(bad), len(probs)))
    sys.exit(1 if bad or probs else 0)


if __name__ == "__main__":
    main()
