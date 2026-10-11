#!/usr/bin/env python3
"""Deterministic bookkeeping for a Gravitas fan-out.

Counting, deduplication and vote tallies are kept in a JSON file so that the
loop decisions do not depend on a model's memory of forty findings across three
rounds. Standard library only, Python 3.8 or later.

Commands:
  init        LEDGER --scale quick|standard|full|exhaustive [--max-rounds N] [--dry-stop N] [--votes N]
  add         LEDGER RECORDS.json --round N --by AGENT
  verdict     LEDGER KEY --by AGENT --refuted yes|no|blocked [--tier T] [--source S] [--reason R] [--error E]
  verdicts    LEDGER VERDICTS.json --by AGENT
  merge       LEDGER KEEP_KEY DUP_KEY [DUP_KEY ...]
  child       LEDGER --id ID --agent NAME --status running|done|failed|denied|empty|killed [--note N]
  close-round LEDGER --round N
  report      LEDGER [--format md|json]

RECORDS.json holds one finding record or a list of them, shaped like
schemas/finding.schema.json. VERDICTS.json holds one verdict or a list of them,
shaped like schemas/verdict.schema.json. Records are checked against those
schemas; a malformed record is rejected with the reason, and a record whose only
problem is a missing source is demoted to inferred instead. Exit status is 0 on
success and 2 on bad input.
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
# Two findings in the same file are compared when their lines are at most this far apart.
# Nearby findings merge automatically only when their wording is near-identical, because
# two distinct defects a few lines apart are often described in similar words.
NEARBY_LINES = 5
NEAR_SIMILARITY = 0.8
STOP = set("the a an of to in and or for by is are that this with without into from on at as be it its".split())
# A quotation is text in straight double quotes, typographic double quotes, or a typographic
# single pair whose closing mark is not an apostrophe inside a word. Straight single quotes
# are not accepted: they cannot be told apart from apostrophes.
QUOTES = (
    re.compile(r'"([^"\n]+)"'),
    re.compile("“([^”\n]+)”"),
    re.compile("‘(.+?)’(?!\\w)"),
)
QUOTE_WORDS = 3
# Code is quoted in few words ("revokeAccess(token)"), so a span this long also counts.
QUOTE_CHARS = 12
LOCATION = re.compile(r"^(?P<file>.+?)(?::L?|#L)(?P<a>\d+)(?:\s*[-–]\s*L?(?P<b>\d+))?(?::\d+)?\s*(?:\([^)]*\))?\s*$")
SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "schemas")

# Used only when the schemas folder is not beside the scripts folder.
FALLBACK_SCHEMAS = {
    "finding": {
        "type": "object",
        "required": ["claim", "location", "tier"],
        "properties": {
            "claim": {"type": "string"}, "location": {"type": "string"},
            "tier": {"enum": list(TIERS)}, "source": {"type": "string"},
            "severity": {"enum": list(SEVERITIES)}, "dimension": {"type": "string"},
            "hypothesis": {"type": "boolean"}, "falsifier": {"type": "string"}, "key": {"type": "string"},
        },
        "allOf": [{"if": {"properties": {"tier": {"enum": ["observed", "executed", "read"]}}},
                   "then": {"required": ["source"], "properties": {"source": {"minLength": 1}}}}],
        "additionalProperties": False,
    },
    "verdict": {
        "type": "object",
        "required": ["key", "refuted", "tier", "reason"],
        "properties": {
            "status": {"enum": ["done", "blocked"]},
            "key": {"type": "string"}, "refuted": {"enum": ["yes", "no", "blocked"]},
            "lens": {"type": "string"}, "tier": {"enum": list(TIERS)}, "source": {"type": "string"},
            "reason": {"type": "string"}, "error": {"type": "string"},
        },
        "additionalProperties": False,
    },
}
_SCHEMAS = {}


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def load(path):
    if not os.path.exists(path):
        fail("no ledger at %s; run init first" % path)
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        fail("cannot read ledger %s: %s" % (path, e))


def load_json(path, what):
    # utf-8-sig: Windows PowerShell 5.1 writes a byte order mark by default
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return json.load(fh)
    except OSError as e:
        fail("cannot read %s %s: %s" % (what, path, e.strerror or e))
    except ValueError as e:
        fail("%s %s is not valid JSON: %s" % (what, path, e))


def save(path, data):
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=folder, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------- schema checks

def schema(name):
    """The named schema from schemas/NAME.schema.json, or the built-in copy if it is absent."""
    if name not in _SCHEMAS:
        path = os.path.join(SCHEMA_DIR, name + ".schema.json")
        try:
            with open(path, encoding="utf-8") as fh:
                _SCHEMAS[name] = json.load(fh)
        except (OSError, ValueError):
            _SCHEMAS[name] = FALLBACK_SCHEMAS[name]
    return _SCHEMAS[name]


def type_ok(value, kind):
    if kind == "string":
        return isinstance(value, str)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def validate(value, sch, field="", conditional=False):
    """Check VALUE against the subset of JSON Schema the Gravitas schemas use.

    Returns (errors, unknown): errors is a list of (field, message, conditional), where
    conditional is True for an error raised by an if/then rule; unknown lists the
    properties that additionalProperties: false does not allow.
    """
    errors, unknown = [], []
    kind = sch.get("type")
    if kind and not type_ok(value, kind):
        errors.append((field, "must be a %s, not %s" % (kind, type(value).__name__), conditional))
        return errors, unknown
    if "enum" in sch and value not in sch["enum"]:
        errors.append((field, "%r is not one of %s" % (value, ", ".join(map(str, sch["enum"]))), conditional))
    if "minLength" in sch and isinstance(value, str) and len(value) < sch["minLength"]:
        errors.append((field, "must not be empty", conditional))
    if isinstance(value, dict):
        props = sch.get("properties", {})
        for name in sch.get("required", []):
            if name not in value:
                errors.append((name, "is required", conditional))
        for name, item in value.items():
            if name in props:
                errors += validate(item, props[name], name, conditional)[0]
            elif sch.get("additionalProperties") is False:
                unknown.append(name)
        for rule in sch.get("allOf", []):
            if "if" in rule and not validate(value, rule["if"])[0]:
                errors += validate(value, rule.get("then", {}), field, True)[0]
    return errors, unknown


def check_record(rec, name, nonempty):
    """Validate one record against schema NAME.

    Returns (clean, problems, unknown): clean is the record without null optional fields
    and without unknown fields, problems lists the reasons to reject it (empty when it
    may be kept), and unknown names the fields that were dropped. A conditional error
    (an observed, executed or read record with no source) is not a problem here; the
    provenance check demotes it.
    """
    if not isinstance(rec, dict):
        return None, ["is a %s, not an object" % type(rec).__name__], []
    clean = {k: v for k, v in rec.items() if v is not None}
    errors, unknown = validate(clean, schema(name))
    problems = ["%s %s" % (f, m) if f else m for f, m, cond in errors if not cond]
    for f in nonempty:
        if isinstance(clean.get(f), str) and not clean[f].strip():
            problems.append("%s must not be empty" % f)
    for f in unknown:
        clean.pop(f, None)
    return clean, problems, unknown


def describe(rec):
    text = (rec.get("claim") or rec.get("key") or "") if isinstance(rec, dict) else rec
    return repr(str(text)[:60])


# ---------------------------------------------------------------- deduplication

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


def line_span(location):
    """(file, first, last) for file:line, file:line-line, file:line:col or file#Lline; else None."""
    m = LOCATION.match((location or "").strip())
    if not m:
        return None
    path = m.group("file").strip().replace("\\", "/").lower()
    while path.startswith("./"):
        path = path[2:]
    first = int(m.group("a"))
    last = int(m.group("b")) if m.group("b") else first
    return path, min(first, last), max(first, last)


def same_place(loc_a, loc_b):
    """'same' for identical locations or overlapping line spans in one file, 'near' for
    spans in one file at most NEARBY_LINES apart, None otherwise. Only 'same' can be
    merged automatically; 'near' is flagged for the parent to decide with `merge`."""
    if norm(loc_a) == norm(loc_b):
        return "same"
    a, b = line_span(loc_a), line_span(loc_b)
    if not a or not b or a[0] != b[0]:
        return None
    gap = max(a[1], b[1]) - min(a[2], b[2])
    if gap <= 0:
        return "same"
    return "near" if gap <= NEARBY_LINES else None


# ---------------------------------------------------------------- provenance

def unwrap(source):
    """Finders sometimes write the whole label into source: read ("path", "quote")."""
    m = re.match(r"^\s*(observed|executed|read|inferred)\s*\((.*)\)\s*$", source or "", re.S)
    return m.group(2).strip() if m else (source or "")


def pathlike(text):
    """A quoted path or location ("src/auth.py", "auth.py:9") quotes no content."""
    t = text.strip()
    if not t or re.search(r"\s", t):
        return bool(t) and bool(LOCATION.match(t))
    return ("/" in t or "\\" in t or bool(re.fullmatch(r"[\w.-]+\.\w{1,5}(?::L?\d+)?", t))
            or bool(LOCATION.match(t)))


def quotes_something(source):
    """True when SOURCE quotes content: at least QUOTE_WORDS words or QUOTE_CHARS
    non-space characters with a letter, and not merely a path or location."""
    for pattern in QUOTES:
        for m in pattern.finditer(source or ""):
            span = m.group(1)
            if pathlike(span):
                continue
            found = [w for w in re.findall(r"\w+", span) if re.search(r"[^\W_]", w)]
            dense = re.sub(r"\s+", "", span)
            if len(found) >= QUOTE_WORDS or (len(dense) >= QUOTE_CHARS and re.search(r"[^\W\d_]", dense)):
                return True
    return False


def check_provenance(rec):
    """Return a reason string if the record's label cannot stand, else None."""
    tier, source = rec["tier"], (rec.get("source") or "").strip()
    if tier == "inferred":
        return None
    if not source:
        return "%s label with no source" % tier
    if tier == "read" and not quotes_something(source):
        return "read label whose source quotes nothing"
    return None


def vote_demotion(vote):
    """Why a vote was demoted to inferred, or None. Ledgers written before votes carried a
    'demoted' field record it only in the reason text."""
    if "demoted" in vote:
        return vote["demoted"]
    m = re.search(r"\[demoted: ([^\]]+)\]", vote.get("reason") or "")
    return m.group(1) if m else None


def counts(vote):
    """A vote counts unless it is blocked or was demoted for a label it could not support."""
    blocked = vote.get("status") == "blocked" or vote.get("refuted") == "blocked"
    return not blocked and not vote_demotion(vote)


# ---------------------------------------------------------------- commands

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
    recs = load_json(a.records, "records file")
    rnd = L["rounds"].setdefault(str(a.round), {"fresh": 0, "duplicates": 0, "demoted": 0,
                                                 "rejected": 0, "closed": False})
    if rnd["closed"]:
        fail("round %d is already closed" % a.round)
    if isinstance(recs, dict) and recs.get("status") == "blocked" and "findings" not in recs:
        # a finder that could not work returns an envelope, not a finding: record why
        rnd.setdefault("blocked", []).append({"by": a.by, "error": str(recs.get("error") or "")})
        save(a.ledger, L)
        print("blocked: %s returned no findings (%s)" % (a.by, recs.get("error") or "no reason given"))
        return
    if isinstance(recs, dict):
        recs = recs.get("findings", [recs])
    if not isinstance(recs, list):
        fail("%s holds neither a finding record nor a list of them" % a.records)
    for n, raw in enumerate(recs, 1):
        rec, problems, unknown = check_record(raw, "finding", ("claim", "location"))
        if problems:
            rnd["rejected"] += 1
            print("rejected: record %d %s does not match finding.schema.json: %s"
                  % (n, describe(raw), "; ".join(problems)))
            continue
        if unknown:
            print("  record %d: ignored field(s) not in finding.schema.json: %s" % (n, ", ".join(unknown)))
        key = rec.get("key") or make_key(rec)
        same, near = [], []
        for k, f in L["findings"].items():
            if f.get("merged_into"):
                continue
            place = same_place(f["location"], rec["location"])
            if place:
                (same if place == "same" else near).append((overlap(f["claim"], rec["claim"]), k))
        best_same = max(same) if same else (0.0, None)
        best = max(same + near) if same or near else (0.0, None)
        best_near = max(near) if near else (0.0, None)
        if key in L["findings"] or best_same[0] >= SIMILARITY or best_near[0] >= NEAR_SIMILARITY:
            dup = best_same if best_same[0] >= SIMILARITY else best_near
            rnd["duplicates"] += 1
            print("duplicate of %s (overlap %.2f): %s" % (dup[1] or key, dup[0], rec["claim"][:60]))
            continue
        entry = {k: rec.get(k) for k in ("claim", "location", "tier", "source", "dimension")}
        entry["source"] = unwrap(entry.get("source"))
        entry["severity"] = rec.get("severity", "medium")
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
    counted = [v for v in f["votes"] if counts(v)]
    if need <= 0 and not counted:
        return "unverified"
    if len(counted) < max(need, 1):
        return "pending"
    upheld = sum(1 for v in counted if v["refuted"] == "no")
    refuted = len(counted) - upheld
    if upheld > refuted:
        return "survived"
    if refuted > upheld:
        return "refuted"
    return "contested"


def record_vote(L, rec, by):
    """Append one schema-valid verdict to its finding and print the result."""
    key, seen = rec["key"], set()
    while L["findings"][key].get("merged_into") and key not in seen:
        seen.add(key)
        key = L["findings"][key]["merged_into"]
    if key != rec["key"]:
        print("  %s was merged into %s; the vote is recorded there" % (rec["key"], key))
    f = L["findings"][key]
    vote = {"by": by, "refuted": rec["refuted"], "tier": rec.get("tier"),
            "source": unwrap(rec.get("source")), "reason": rec.get("reason"), "demoted": None}
    for extra in ("lens", "error", "status"):
        if rec.get(extra):
            vote[extra] = rec[extra]
    blocked = vote.get("status") == "blocked" or vote["refuted"] == "blocked"
    if not blocked and vote["tier"]:
        # a vote is held to the same provenance rule as a finding
        reason = check_provenance({"tier": vote["tier"], "source": vote["source"]})
        if reason:
            vote["demoted"] = reason
            vote["tier"] = "inferred"
            vote["reason"] = ((vote["reason"] or "") + " [demoted: %s]" % reason).strip()
    f["votes"].append(vote)
    print("%s: %s (%d vote(s), %d needed)"
          % (key, status_of(f, L["votes"]), len(f["votes"]), L["votes"]))
    if blocked:
        print("  vote by %s is blocked (%s); it is recorded but does not count"
              % (by, vote.get("error") or "no reason given"))
    if vote.get("demoted"):
        print("  vote by %s demoted to inferred (%s); it is recorded but does not count"
              % (by, vote["demoted"]))


def cmd_verdict(a):
    L = load(a.ledger)
    if a.key not in L["findings"]:
        fail("no finding with key %s" % a.key)
    rec = {"key": a.key, "refuted": a.refuted, "tier": a.tier, "source": a.source,
           "reason": a.reason if a.reason is not None else "", "error": a.error}
    # an unlabelled verdict is the voter's own judgement, which is what inferred means
    rec["tier"] = rec["tier"] or "inferred"
    rec, problems, _ = check_record(rec, "verdict", ("key",))
    if problems:
        fail("verdict does not match verdict.schema.json: %s" % "; ".join(problems))
    record_vote(L, rec, a.by)
    save(a.ledger, L)


def cmd_verdicts(a):
    L = load(a.ledger)
    recs = load_json(a.records, "verdicts file")
    if isinstance(recs, dict):
        recs = recs.get("verdicts", [recs])
    if not isinstance(recs, list):
        fail("%s holds neither a verdict nor a list of them" % a.records)
    taken = rejected = 0
    for n, raw in enumerate(recs, 1):
        rec, problems, unknown = check_record(raw, "verdict", ("key",))
        if not problems and rec["key"] not in L["findings"]:
            problems = ["no finding with key %s" % rec["key"]]
        if problems:
            rejected += 1
            print("rejected: verdict %d %s does not match verdict.schema.json: %s"
                  % (n, describe(raw), "; ".join(problems)))
            continue
        if unknown:
            print("  verdict %d: ignored field(s) not in verdict.schema.json: %s" % (n, ", ".join(unknown)))
        record_vote(L, rec, a.by)
        taken += 1
    save(a.ledger, L)
    print("verdicts: recorded=%d rejected=%d" % (taken, rejected))


def cmd_merge(a):
    L = load(a.ledger)
    keep = L["findings"].get(a.keep)
    if keep is None:
        fail("no finding with key %s" % a.keep)
    # A merged finding is left out of the report, so only a live finding can take another in,
    # and a finding is merged once: merging A into B and then B into A would drop both.
    if keep.get("merged_into"):
        fail("%s is already merged into %s; merge into that one" % (a.keep, keep["merged_into"]))
    for d in a.dups:
        f = L["findings"].get(d)
        if f is None or d == a.keep:
            fail("cannot merge %s" % d)
        if f.get("merged_into"):
            fail("%s is already merged into %s" % (d, f["merged_into"]))
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
    groups = {"survived": [], "contested": [], "pending": [], "refuted": [], "unverified": []}
    live = [f for f in L["findings"].values() if not f.get("merged_into")]
    for f in sorted(live, key=lambda x: (order.get(x["severity"], order["medium"]), x["round"])):
        groups[status_of(f, L["votes"])].append(f)
    closed = [int(r) for r, v in L["rounds"].items() if v["closed"]]
    not_counted = [{"key": f["key"], "by": v.get("by"), "refuted": v.get("refuted"),
                    "reason": vote_demotion(v)}
                   for f in live for v in f["votes"] if v.get("refuted") != "blocked" and vote_demotion(v)]
    counted_total = sum(1 for f in live for v in f["votes"] if counts(v))
    unvoted_label = "%s scale takes no votes" % L["scale"] if L["scale"] == "quick" else "this run takes no votes"
    caps = []
    if closed and max(closed) >= L["max_rounds"] and L["dry"] < L["dry_stop"]:
        caps.append("stopped at the round ceiling (%d) before %d dry rounds" % (L["max_rounds"], L["dry_stop"]))
    if L["votes"] and groups["pending"]:
        caps.append("%d finding(s) never reached the %d vote(s) required; they are unverified"
                    % (len(groups["pending"]), L["votes"]))
    if not L["votes"]:
        if counted_total:
            caps.append("%s; %d finding(s) were never voted on and are unverified"
                        % (unvoted_label, len(groups["unverified"])))
        else:
            caps.append("no votes were taken (%s); all %d finding(s) are unverified"
                        % (unvoted_label, len(groups["unverified"])))
    if not_counted:
        caps.append("%d vote(s) did not count toward survival or refutation: each claimed observed, "
                    "executed or read with no source and was demoted to inferred" % len(not_counted))
    gaps = {i: c for i, c in L["children"].items() if c["status"] != "done"}
    if a.format == "json":
        print(json.dumps({"scale": L["scale"], "votes_needed": L["votes"], "votes_taken": counted_total,
                          "rounds": L["rounds"], "groups": groups, "votes_not_counted": not_counted,
                          "children_not_done": gaps, "caps": caps}, indent=2, ensure_ascii=False))
        return
    print("# Ledger report\n")
    print("Scale %s, %d round(s) closed, votes needed %d, dry rounds %d of %d.\n"
          % (L["scale"], len(closed), L["votes"], L["dry"], L["dry_stop"]))
    if not L["votes"]:
        if counted_total:
            print("The %s scale takes no votes; %d vote(s) were cast anyway, and every finding without "
                  "one is listed as unverified.\n" % (L["scale"], counted_total))
        else:
            print("No votes were taken: the %s scale takes none, so no finding below has been "
                  "verified.\n" % L["scale"])
    names = ["survived", "contested", "pending", "refuted"]
    if not L["votes"]:
        names.insert(1, "unverified")
    for name in names:
        items = groups[name]
        title = "Unverified, %s" % unvoted_label if name == "unverified" else name.capitalize()
        print("## %s (%d)\n" % (title, len(items)))
        for f in items:
            src = " (%s)" % f["source"] if f.get("source") else ""
            tally = [v["refuted"] for v in f["votes"] if counts(v) or v["refuted"] == "blocked"]
            dropped = [v for v in f["votes"] if v["refuted"] != "blocked" and vote_demotion(v)]
            votes = ""
            if f["votes"]:
                votes = " Votes: %d upheld, %d refuted, %d blocked" % (
                    tally.count("no"), tally.count("yes"), tally.count("blocked"))
                votes += ", %d not counted." % len(dropped) if dropped else "."
            print("- [%s] %s: %s. %s%s.%s" % (f["severity"], f["location"], f["claim"].rstrip("."),
                                             f["tier"], src, votes))
            if f.get("demoted"):
                print("  - demoted: %s" % f["demoted"])
            for v in dropped:
                print("  - vote not counted: %s (%s) was demoted to inferred: %s"
                      % (v.get("by"), "upheld" if v["refuted"] == "no" else "refuted", vote_demotion(v)))
        print()
    print("## Subagents not done (%d)\n" % len(gaps))
    for i, c in gaps.items():
        print("- %s %s: %s%s" % (c["agent"], i, c["status"], " (%s)" % c["note"] if c.get("note") else ""))
    print("\n## Caps (%d)\n" % len(caps))
    for c in caps:
        print("- " + c)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
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
    s.add_argument("--error")
    s.set_defaults(fn=cmd_verdict)

    s = sub.add_parser("verdicts", help="record verdict records from a JSON file")
    s.add_argument("ledger")
    s.add_argument("records")
    s.add_argument("--by", required=True)
    s.set_defaults(fn=cmd_verdicts)

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
