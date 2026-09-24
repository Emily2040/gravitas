#!/usr/bin/env python3
"""Deterministic bookkeeping for a Gravitas fan-out.

Counting, deduplication and vote tallies are kept in a JSON file so that the
loop decisions do not depend on a model's memory of forty findings across three
rounds. Standard library only, Python 3.8 or later.

Commands:
  init        LEDGER --scale quick|standard|full|exhaustive [--max-rounds N] [--dry-stop N] [--votes N]
  add         LEDGER RECORDS.json --round N --by AGENT
  verdict     LEDGER KEY --by AGENT --refuted yes|no|blocked [--tier T] [--source S] [--reason R]
  merge       LEDGER KEEP_KEY DUP_KEY [DUP_KEY ...]
  child       LEDGER --id ID --agent NAME --status running|done|failed|denied|empty|killed [--note N]
  close-round LEDGER --round N
  report      LEDGER [--format md|json]

RECORDS.json holds one finding record or a list of them, shaped like
schemas/finding.schema.json. Exit status is 0 on success and 2 on bad input.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile

TIERS = ("observed", "executed", "read", "inferred")
SEVERITIES = ("critical", "high", "medium", "low", "info")
CHILD_STATES = ("running", "done", "failed", "denied", "empty", "killed")
SCALES = {
    "quick": {"max_rounds": 1, "dry_stop": 1, "votes": 0},
    "standard": {"max_rounds": 3, "dry_stop": 1, "votes": 1},
    "full": {"max_rounds": 5, "dry_stop": 2, "votes": 3},
    "exhaustive": {"max_rounds": 8, "dry_stop": 2, "votes": 3},
}
# Word-overlap (Jaccard) thresholds for two claims at the same location. Calibrated on
# one 22-finding audit run: true duplicates scored 0.13 to 0.69, distinct defects on the
# same line 0.02 to 0.15. Automatic merges start at 0.25; 0.10 to 0.25 is only flagged,
# and the parent decides with `merge`.
SIMILARITY = 0.25
POSSIBLE = 0.10
STOP = set("the a an of to in and or for by is are that this with without into from on at as be it its".split())
QUOTE = re.compile(r"[\"“”‘’'].{3,}[\"“”‘’']")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def load(path):
    if not os.path.exists(path):
        fail("no ledger at %s; run init first" % path)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=folder, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def words(text):
    return re.findall(r"[a-z0-9_./:-]+", (text or "").lower())


def norm(text):
    return " ".join(words(text))


def make_key(rec):
    basis = norm(rec.get("location")) + "|" + norm(rec.get("claim"))
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]


def overlap(a, b):
    sa, sb = set(words(a)) - STOP, set(words(b)) - STOP
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def unwrap(source):
    """Finders sometimes write the whole label into source: read ("path", "quote")."""
    m = re.match(r"^\s*(observed|executed|read|inferred)\s*\((.*)\)\s*$", source or "", re.S)
    return m.group(2).strip() if m else (source or "")


def check_provenance(rec):
    """Return a reason string if the record's label cannot stand, else None."""
    tier, source = rec["tier"], (rec.get("source") or "").strip()
    if tier == "inferred":
        return None
    if not source:
        return "%s label with no source" % tier
    if tier == "read" and not QUOTE.search(source):
        return "read label whose source quotes nothing"
    return None


def cmd_init(a):
    if os.path.exists(a.ledger) and not a.force:
        fail("%s exists; pass --force to replace it" % a.ledger)
    d = dict(SCALES[a.scale])
    for k in ("max_rounds", "dry_stop", "votes"):
        if getattr(a, k) is not None:
            d[k] = getattr(a, k)
    save(a.ledger, {"version": 1, "scale": a.scale, **d, "dry": 0,
                    "rounds": {}, "findings": {}, "children": {}})
    print("ledger %s: scale=%s max_rounds=%d dry_stop=%d votes=%d"
          % (a.ledger, a.scale, d["max_rounds"], d["dry_stop"], d["votes"]))


def cmd_add(a):
    L = load(a.ledger)
    with open(a.records, encoding="utf-8") as fh:
        recs = json.load(fh)
    if isinstance(recs, dict):
        recs = recs.get("findings", [recs])
    rnd = L["rounds"].setdefault(str(a.round), {"fresh": 0, "duplicates": 0, "demoted": 0,
                                                 "rejected": 0, "closed": False})
    if rnd["closed"]:
        fail("round %d is already closed" % a.round)
    for rec in recs:
        missing = [f for f in ("claim", "location", "tier") if not rec.get(f)]
        if missing or rec.get("tier") not in TIERS:
            rnd["rejected"] += 1
            print("rejected: missing %s or bad tier in %r" % (missing, rec.get("claim", "")[:60]))
            continue
        key = rec.get("key") or make_key(rec)
        same_place = [(overlap(f["claim"], rec["claim"]), k) for k, f in L["findings"].items()
                      if norm(f["location"]) == norm(rec["location"]) and not f.get("merged_into")]
        best = max(same_place) if same_place else (0.0, None)
        if key in L["findings"] or best[0] >= SIMILARITY:
            rnd["duplicates"] += 1
            print("duplicate of %s (overlap %.2f): %s" % (best[1] or key, best[0], rec["claim"][:60]))
            continue
        entry = {k: rec.get(k) for k in ("claim", "location", "tier", "source", "dimension")}
        entry["source"] = unwrap(entry.get("source"))
        entry["severity"] = rec.get("severity") if rec.get("severity") in SEVERITIES else "medium"
        entry.update({"key": key, "round": a.round, "by": a.by, "votes": [], "demoted": None})
        reason = check_provenance(entry)
        if reason:
            entry["demoted"] = "%s (claimed %s)" % (reason, entry["tier"])
            entry["tier"] = "inferred"
            rnd["demoted"] += 1
        L["findings"][key] = entry
        rnd["fresh"] += 1
        print("fresh %s %s %s" % (key, entry["tier"], entry["claim"][:70]))
        if best[0] >= POSSIBLE:
            print("  possible duplicate of %s (overlap %.2f); merge it if it is the same defect" % (best[1], best[0]))
    save(a.ledger, L)
    print("round %d: fresh=%d duplicates=%d demoted=%d rejected=%d"
          % (a.round, rnd["fresh"], rnd["duplicates"], rnd["demoted"], rnd["rejected"]))


def status_of(f, need):
    counted = [v for v in f["votes"] if v["refuted"] != "blocked"]
    if len(counted) < max(need, 1):
        return "pending"
    upheld = sum(1 for v in counted if v["refuted"] == "no")
    refuted = len(counted) - upheld
    if upheld > refuted:
        return "survived"
    if refuted > upheld:
        return "refuted"
    return "contested"


def cmd_verdict(a):
    L = load(a.ledger)
    f = L["findings"].get(a.key)
    if f is None:
        fail("no finding with key %s" % a.key)
    vote = {"by": a.by, "refuted": a.refuted, "tier": a.tier, "source": a.source, "reason": a.reason}
    if a.refuted != "blocked" and a.tier and a.tier != "inferred" and not (a.source or "").strip():
        vote["tier"] = "inferred"
        vote["reason"] = ((a.reason or "") + " [demoted: %s label with no source]" % a.tier).strip()
    f["votes"].append(vote)
    save(a.ledger, L)
    print("%s: %s (%d vote(s), %d needed)"
          % (a.key, status_of(f, L["votes"]), len(f["votes"]), L["votes"]))


def cmd_merge(a):
    L = load(a.ledger)
    keep = L["findings"].get(a.keep)
    if keep is None:
        fail("no finding with key %s" % a.keep)
    for d in a.dups:
        f = L["findings"].get(d)
        if f is None or d == a.keep:
            fail("cannot merge %s" % d)
        keep["votes"].extend(f["votes"])
        f["votes"], f["merged_into"] = [], a.keep
        print("merged %s into %s" % (d, a.keep))
    save(a.ledger, L)


def cmd_child(a):
    L = load(a.ledger)
    L["children"][a.id] = {"agent": a.agent, "status": a.status, "note": a.note}
    save(a.ledger, L)
    print("child %s (%s): %s" % (a.id, a.agent, a.status))


def cmd_close(a):
    L = load(a.ledger)
    rnd = L["rounds"].get(str(a.round))
    if rnd is None:
        rnd = L["rounds"][str(a.round)] = {"fresh": 0, "duplicates": 0, "demoted": 0,
                                            "rejected": 0, "closed": False}
    if rnd["closed"]:
        fail("round %d is already closed" % a.round)
    rnd["closed"] = True
    L["dry"] = L["dry"] + 1 if rnd["fresh"] == 0 else 0
    running = [i for i, c in L["children"].items() if c["status"] == "running"]
    save(a.ledger, L)
    if running:
        print("WARNING: %d child(ren) still marked running: %s" % (len(running), ", ".join(running)))
    pending = [k for k, f in L["findings"].items()
               if L["votes"] and not f.get("merged_into") and status_of(f, L["votes"]) == "pending"]
    if pending:
        print("WARNING: %d finding(s) still short of %d vote(s): %s"
              % (len(pending), L["votes"], ", ".join(pending)))
    if L["dry"] >= L["dry_stop"]:
        print("STOP: %d consecutive dry round(s)" % L["dry"])
    elif a.round >= L["max_rounds"]:
        print("STOP: round ceiling %d reached; report it as a cap" % L["max_rounds"])
    else:
        print("CONTINUE: round %d had %d fresh finding(s); dry=%d of %d"
              % (a.round, rnd["fresh"], L["dry"], L["dry_stop"]))


def cmd_report(a):
    L = load(a.ledger)
    order = {s: i for i, s in enumerate(SEVERITIES)}
    groups = {"survived": [], "contested": [], "pending": [], "refuted": []}
    live = [f for f in L["findings"].values() if not f.get("merged_into")]
    for f in sorted(live, key=lambda x: (order[x["severity"]], x["round"])):
        groups[status_of(f, L["votes"]) if L["votes"] else "survived"].append(f)
    closed = [int(r) for r, v in L["rounds"].items() if v["closed"]]
    caps = []
    if closed and max(closed) >= L["max_rounds"] and L["dry"] < L["dry_stop"]:
        caps.append("stopped at the round ceiling (%d) before %d dry rounds" % (L["max_rounds"], L["dry_stop"]))
    if L["votes"] and groups["pending"]:
        caps.append("%d finding(s) never reached the %d vote(s) required; they are unverified"
                    % (len(groups["pending"]), L["votes"]))
    gaps = {i: c for i, c in L["children"].items() if c["status"] != "done"}
    if a.format == "json":
        print(json.dumps({"scale": L["scale"], "rounds": L["rounds"], "groups": groups,
                          "children_not_done": gaps, "caps": caps}, indent=2, ensure_ascii=False))
        return
    print("# Ledger report\n")
    print("Scale %s, %d round(s) closed, votes needed %d, dry rounds %d of %d.\n"
          % (L["scale"], len(closed), L["votes"], L["dry"], L["dry_stop"]))
    for name in ("survived", "contested", "pending", "refuted"):
        items = groups[name]
        print("## %s (%d)\n" % (name.capitalize(), len(items)))
        for f in items:
            src = " (%s)" % f["source"] if f.get("source") else ""
            tally = [v["refuted"] for v in f["votes"]]
            votes = " Votes: %d upheld, %d refuted, %d blocked." % (
                tally.count("no"), tally.count("yes"), tally.count("blocked")) if tally else ""
            print("- [%s] %s: %s. %s%s.%s" % (f["severity"], f["location"], f["claim"].rstrip("."),
                                             f["tier"], src, votes))
            if f.get("demoted"):
                print("  - demoted: %s" % f["demoted"])
        print()
    print("## Subagents not done (%d)\n" % len(gaps))
    for i, c in gaps.items():
        print("- %s %s: %s%s" % (c["agent"], i, c["status"], " (%s)" % c["note"] if c.get("note") else ""))
    print("\n## Caps (%d)\n" % len(caps))
    for c in caps:
        print("- " + c)


def main():
    p = argparse.ArgumentParser(description="Gravitas fan-out ledger")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init")
    s.add_argument("ledger")
    s.add_argument("--scale", choices=sorted(SCALES), required=True)
    s.add_argument("--max-rounds", dest="max_rounds", type=int)
    s.add_argument("--dry-stop", dest="dry_stop", type=int)
    s.add_argument("--votes", type=int)
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("add")
    s.add_argument("ledger")
    s.add_argument("records")
    s.add_argument("--round", type=int, required=True)
    s.add_argument("--by", required=True)
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("verdict")
    s.add_argument("ledger")
    s.add_argument("key")
    s.add_argument("--by", required=True)
    s.add_argument("--refuted", choices=("yes", "no", "blocked"), required=True)
    s.add_argument("--tier", choices=TIERS)
    s.add_argument("--source")
    s.add_argument("--reason")
    s.set_defaults(fn=cmd_verdict)

    s = sub.add_parser("merge")
    s.add_argument("ledger")
    s.add_argument("keep")
    s.add_argument("dups", nargs="+")
    s.set_defaults(fn=cmd_merge)

    s = sub.add_parser("child")
    s.add_argument("ledger")
    s.add_argument("--id", required=True)
    s.add_argument("--agent", required=True)
    s.add_argument("--status", choices=CHILD_STATES, required=True)
    s.add_argument("--note")
    s.set_defaults(fn=cmd_child)

    s = sub.add_parser("close-round")
    s.add_argument("ledger")
    s.add_argument("--round", type=int, required=True)
    s.set_defaults(fn=cmd_close)

    s = sub.add_parser("report")
    s.add_argument("ledger")
    s.add_argument("--format", choices=("md", "json"), default="md")
    s.set_defaults(fn=cmd_report)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
