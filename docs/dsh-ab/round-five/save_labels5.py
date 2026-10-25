"""Save the relabelling workflow's results through the ledger, and check that every note is labelled by both relabellers.

    python save_labels5.py <workflow-output-file> [...]   -> ledger.jsonl (every label received), then labels-sonnet.json
                                                             and labels-opus.json, only if there is no problem
    python save_labels5.py --retire ID RELABELLER REASON  log a replace record: the next valid label received is used
    python save_labels5.py --selftest                     check this script on made-up data in a temporary folder
    --base DIR                                            the round folder (default: the folder this script is in)

Every label received (workflows/label5.js results: {"file", "case", "model", "labels": [{"id", "label", "cite"}] or
null}) is appended to ledger.jsonl with its time, id, relabeller and batch, valid or not. A label is valid when its id
is a note of claim-notes.json, its label is wrong, unverified or not an error, and a 'wrong' carries a cite. The label
used for an (id, relabeller) is the first valid one in the ledger after the last replace record (amendment 2026-10-25),
and labels-*.json are written from those, so passing a rerun batch before the original changes nothing.

labels-*.json are written only when there is no problem. Problems: an output that cannot be read; a label for an id
that is not a note; two different valid labels for the same id and relabeller in the outputs given; any note without
a valid label from either relabeller after all outputs. Not problems (reported as notes): an empty batch that a later
file fills; an invalid label that a valid one replaces; a valid label that differs from the one already in force from
an earlier run (logged, not used). Exit 1 on any problem. Standard library only.
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_FILE = "ledger.jsonl"
MODELS = ("sonnet", "opus")
LABELS = ("wrong", "unverified", "not an error")


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def results(path):
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    data = data.get("result") if isinstance(data, dict) else data
    if not isinstance(data, list):
        raise ValueError("no result list")
    return data


def append_ledger(base, entries):
    lock = os.path.join(base, LEDGER_FILE + ".lock")
    for _ in range(200):
        try:
            os.mkdir(lock)
            break
        except FileExistsError:
            time.sleep(0.05)
    else:
        raise SystemExit("ledger lock %s held for 10 s; remove it if no save is running" % lock)
    try:
        with open(os.path.join(base, LEDGER_FILE), "a", encoding="utf-8", newline="\n") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    finally:
        os.rmdir(lock)


def label_refs(base):
    """{(id, relabeller): first valid label entry after the last replace record}."""
    refs, p = {}, os.path.join(base, LEDGER_FILE)
    if not os.path.isfile(p):
        return refs
    with open(p, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            e = json.loads(line)
            if e.get("kind") == "replace-label":
                refs[(e.get("id"), e.get("relabeller"))] = None
            elif e.get("kind") == "label" and e.get("valid") is True:
                k = (e.get("id"), e.get("relabeller"))
                if refs.get(k) is None:
                    refs[k] = e
    return refs


def norm_id(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and v.strip().isdigit():
        return int(v.strip())
    return None


def run(base, paths):
    """Returns (problems, notes, written)."""
    with open(os.path.join(base, "claim-notes.json"), encoding="utf-8-sig") as f:
        notes_ids = {norm_id(n["id"]) for n in json.load(f)}
    problems, notes, entries = [], [], []
    empty = []          # (file, model) batches that returned nothing, in order
    filled = set()
    seen = {}           # (id, model) -> first valid (label, cite) in these outputs
    for path in paths:
        try:
            rows = results(path)
        except (OSError, ValueError) as e:
            problems.append("cannot read %s: %s" % (path, e))
            continue
        for r in rows:
            if not isinstance(r, dict) or r.get("model") not in MODELS:
                problems.append("%s: a result entry has no known model" % path)
                continue
            key = (r.get("file"), r["model"])
            if r.get("labels") is None:
                empty.append(key)
                continue
            filled.add(key)
            for l in r["labels"]:
                rid = norm_id(l.get("id")) if isinstance(l, dict) else None
                lab = l.get("label") if isinstance(l, dict) else None
                cite = (l.get("cite") or "") if isinstance(l, dict) else ""
                why = []
                if rid not in notes_ids:
                    problems.append("%s: label for id %r, which is not a note" % (r.get("file"), l.get("id") if isinstance(l, dict) else l))
                    why.append("unknown id")
                if lab not in LABELS:
                    why.append("label %r" % (lab,))
                elif lab == "wrong" and not str(cite).strip():
                    why.append("wrong without a cite")
                entries.append({"kind": "label", "time": now(), "id": rid, "relabeller": r["model"], "valid": not why,
                                "problems": why, "label": lab, "cite": cite, "source": os.path.basename(path),
                                "batch": r.get("file")})
                if why:
                    if rid in notes_ids:
                        notes.append("id %s from %s: invalid label (%s), logged and not used" % (rid, r["model"], "; ".join(why)))
                    continue
                k = (rid, r["model"])
                if k in seen and seen[k] != (lab, cite):
                    problems.append("two different labels for id %s from %s in the outputs given" % k)
                seen.setdefault(k, (lab, cite))
    for key in empty:
        if key in filled:
            notes.append("batch %s from %s returned nothing in one output and was filled by another" % key)
        else:
            problems.append("batch %s from %s returned nothing and no later output fills it" % key)
    if entries:
        append_ledger(base, entries)
    refs = label_refs(base)
    for (rid, model), lab in seen.items():
        ref = refs.get((rid, model))
        if ref is not None and (ref["label"], ref.get("cite") or "") != lab:
            notes.append("id %s from %s: this label differs from the one already in force; logged, not used" % (rid, model))
    out = {m: [] for m in MODELS}
    for m in MODELS:
        miss = sorted(i for i in notes_ids if refs.get((i, m)) is None)
        if miss:
            problems.append("%s: %d notes have no valid label (first ids %s)" % (m, len(miss), miss[:5]))
        out[m] = [{"id": i, "label": refs[(i, m)]["label"], "cite": refs[(i, m)].get("cite") or ""}
                  for i in sorted(notes_ids) if refs.get((i, m)) is not None]
    if problems:
        return problems, notes, False
    for m in MODELS:
        with open(os.path.join(base, "labels-%s.json" % m), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out[m], fh, ensure_ascii=False, indent=1)
    return problems, notes, True


def selftest():
    res = []

    def expect(label, cond, info=""):
        print(("[ok]  " if cond else "[BAD] ") + label + (("  -- " + info) if info else ""))
        res.append(bool(cond))

    root = tempfile.mkdtemp(prefix="save-labels4-selftest-")
    try:
        def fresh():
            for f in os.listdir(root):
                p = os.path.join(root, f)
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
            with open(os.path.join(root, "claim-notes.json"), "w", encoding="utf-8") as f:
                json.dump([{"id": i, "pid": "p001", "side": "A", "grader": "opus", "note": "n%d" % i} for i in (0, 1)], f)

        def out(name, rows):
            p = os.path.join(root, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"result": rows}, f)
            return p

        def batch(model, labels, file="relabel-x-00"):
            return {"file": file, "case": "x", "model": model, "labels": labels}

        ok_labels = [{"id": 0, "label": "wrong", "cite": "key line 1"}, {"id": 1, "label": "unverified", "cite": ""}]
        fresh()
        p, n, w = run(root, [out("a.json", [batch("sonnet", ok_labels), batch("opus", ok_labels)])])
        expect("complete labels: written, nothing to report", w and not p, str(p))
        lines = open(os.path.join(root, LEDGER_FILE), encoding="utf-8").read().splitlines()
        expect("route (b): every label received is in the ledger (4)", len(lines) == 4)
        flipped = [{"id": 0, "label": "unverified", "cite": ""}, ok_labels[1]]
        p, n, w = run(root, [out("b.json", [batch("sonnet", flipped)])])
        lab = json.load(open(os.path.join(root, "labels-sonnet.json"), encoding="utf-8"))
        expect("route (b): a later rerun with a different label is logged, not used; the first stays in force",
               w and lab[0]["label"] == "wrong" and any("differs from the one already in force" in x for x in n), str(n))
        fresh()
        p, n, w = run(root, [out("c.json", [batch("sonnet", flipped), batch("sonnet", ok_labels), batch("opus", ok_labels)])])
        expect("route (c): two different labels for one id in the outputs given: a problem, nothing written",
               not w and any("two different labels" in x for x in p) and not os.path.exists(os.path.join(root, "labels-sonnet.json")))
        fresh()
        p, n, w = run(root, [out("d1.json", [batch("sonnet", None), batch("opus", ok_labels)]),
                             out("d2.json", [batch("sonnet", ok_labels)])])
        expect("route (c): an empty batch that a later file fills is not a problem; labels written",
               w and not p and any("filled by another" in x for x in n), str(p))
        fresh()
        p, n, w = run(root, [out("e.json", [batch("sonnet", None), batch("opus", ok_labels)])])
        expect("route (c): an empty batch never filled: a problem, nothing written",
               not w and any("no later output fills it" in x for x in p) and not os.path.exists(os.path.join(root, "labels-opus.json")))
        fresh()
        p, n, w = run(root, [out("f.json", [batch("sonnet", [{"id": 0, "label": "wrong", "cite": ""}, ok_labels[1]]),
                                            batch("opus", ok_labels)])])
        expect("route (c): a 'wrong' without a cite leaves a note unlabelled: a problem, nothing written",
               not w and any("sonnet: 1 notes have no valid label" in x for x in p))
        led = [json.loads(l) for l in open(os.path.join(root, LEDGER_FILE), encoding="utf-8")]
        expect("route (b): the invalid label is in the ledger too, marked invalid",
               sum(1 for e in led if e["valid"] is False and e["id"] == 0 and e["relabeller"] == "sonnet") == 1)
        p, n, w = run(root, [out("g.json", [batch("sonnet", ok_labels)])])
        expect("the invalid label is replaced by a valid one in a later run: written",
               w and not p, str(p))
        fresh()
        p, n, w = run(root, [out("h.json", [batch("sonnet", ok_labels + [{"id": 7, "label": "wrong", "cite": "x"}]),
                                            batch("opus", ok_labels)])])
        expect("route (c): a label for an id that is not a note: a problem, nothing written",
               not w and any("not a note" in x for x in p))
        fresh()
        run(root, [out("i.json", [batch("sonnet", ok_labels), batch("opus", ok_labels)])])
        append_ledger(root, [{"kind": "replace-label", "time": now(), "id": 0, "relabeller": "sonnet", "reason": "test"}])
        p, n, w = run(root, [out("j.json", [batch("sonnet", flipped)])])
        lab = json.load(open(os.path.join(root, "labels-sonnet.json"), encoding="utf-8"))
        expect("--retire: after a replace record the next valid label is used", w and lab[0]["label"] == "unverified", str(p))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("selftest: %d assertions, %d failed" % (len(res), res.count(False)))
    return 0 if all(res) else 1


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outputs", nargs="*")
    ap.add_argument("--base", default=HERE)
    ap.add_argument("--retire", nargs=3, metavar=("ID", "RELABELLER", "REASON"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    base = os.path.abspath(a.base)
    if a.retire:
        rid, model, reason = norm_id(a.retire[0]), a.retire[1], a.retire[2]
        if rid is None or model not in MODELS or not reason.strip():
            raise SystemExit("--retire ID RELABELLER REASON: an integer id, sonnet or opus, and a reason")
        append_ledger(base, [{"kind": "replace-label", "time": now(), "id": rid, "relabeller": model, "reason": reason}])
        print("id %d from %s retired: the next valid label received is used (%s)" % (rid, model, reason))
        sys.exit(0)
    problems, notes, written = run(base, a.outputs)
    for x in notes:
        print("note: " + x)
    for x in problems:
        print("problem: " + x)
    print("%s; %d problems" % ("labels-sonnet.json and labels-opus.json written from the ledger" if written else
                               "nothing written", len(problems)))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
