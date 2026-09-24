#!/usr/bin/env python3
"""Behaviour checks for plugin/skills/gravitas/scripts/ledger.py.

Run with plain `python tests/scripts/test_ledger.py`. Every case builds its own ledger
in a temporary directory. Prints one PASS or FAIL line per case and exits 1 if any fail.
Set LEDGER_SCRIPT to point the cases at another copy of the script.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.environ.get("LEDGER_SCRIPT") or os.path.normpath(
    os.path.join(HERE, "..", "..", "plugin", "skills", "gravitas", "scripts", "ledger.py"))


class Ledger:
    def __init__(self, root, scale, *extra):
        self.root = root
        self.path = os.path.join(root, "run.ledger.json")
        self.n = 0
        self.run("init", self.path, "--scale", scale, *extra)

    def run(self, *args):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        p = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True,
                           text=True, encoding="utf-8", env=env)
        self.last = p
        return p

    def write(self, data):
        self.n += 1
        path = os.path.join(self.root, "records%d.json" % self.n)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False)
        return path

    def add(self, records, rnd=1, by="finder"):
        return self.run("add", self.path, self.write(records), "--round", str(rnd), "--by", by)

    def verdict(self, key, *args):
        return self.run("verdict", self.path, key, "--by", "refuter", *args)

    def report(self, fmt="md"):
        p = self.run("report", self.path, "--format", fmt)
        return json.loads(p.stdout) if fmt == "json" and p.returncode == 0 else p.stdout

    def data(self):
        with open(self.path, encoding="utf-8") as fh:
            return json.load(fh)

    def keys(self):
        return list(self.data()["findings"])

    def finding(self, idx=0):
        return list(self.data()["findings"].values())[idx]


def rec(claim="logout does not revoke the refresh token", location="app/auth.py:9",
        tier="inferred", **kw):
    r = {"claim": claim, "location": location, "tier": tier}
    r.update(kw)
    return r


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def expect(cond, detail):
    if not cond:
        raise AssertionError(detail)


# ---------------------------------------------------------------- defect 1: quick scale

@case
def d1_quick_scale_reports_unverified_not_survived(t):
    L = Ledger(t, "quick")
    L.add([rec(), rec("price rounding drops cents", "app/pricing.py:40", "executed",
                      source="python -c ... -> 9.99 became 9.9")])
    L.run("close-round", L.path, "--round", "1")
    md = L.report()
    j = L.report("json")
    expect(len(j["groups"]["survived"]) == 0, "survived should be empty, got %d" % len(j["groups"]["survived"]))
    expect(len(j["groups"].get("unverified", [])) == 2, "expected 2 unverified")
    expect("## Survived (0)" in md, "md survived count not 0")
    expect("## Unverified, quick scale takes no votes (2)" in md, "no unverified heading:\n" + md)
    expect("No votes were taken" in md, "report does not declare that no votes were taken")
    expect(any("no votes were taken" in c for c in j["caps"]), "no cap for votes: %r" % j["caps"])


@case
def d1_quick_scale_voted_finding_still_gets_status(t):
    L = Ledger(t, "quick")
    L.add([rec(), rec("price rounding drops cents", "app/pricing.py:40")])
    L.verdict(L.keys()[0], "--refuted", "no", "--tier", "executed", "--source", "pytest -> 1 failed")
    j = L.report("json")
    expect(len(j["groups"]["survived"]) == 1, "voted finding should survive")
    expect(len(j["groups"].get("unverified", [])) == 1, "unvoted finding should be unverified")
    expect(any("never voted on" in c for c in j["caps"]), "cap missing: %r" % j["caps"])


# ---------------------------------------------------------------- defect 2: demoted votes

@case
def d2_demoted_upheld_vote_does_not_make_survivor(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    k = L.keys()[0]
    out = L.verdict(k, "--refuted", "no", "--tier", "executed").stdout
    expect("pending" in out, "status after demoted vote should be pending: %s" % out)
    j = L.report("json")
    expect(not j["groups"]["survived"], "demoted vote made the finding survive")
    expect(len(j["groups"]["pending"]) == 1, "finding should be pending")
    expect(len(j.get("votes_not_counted", [])) == 1, "votes_not_counted missing")
    v = L.finding()["votes"][0]
    expect(v["tier"] == "inferred", "vote should be recorded as inferred")


@case
def d2_report_says_how_many_votes_did_not_count(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    L.verdict(L.keys()[0], "--refuted", "no", "--tier", "observed")
    md = L.report()
    expect("1 not counted" in md, "per-finding tally missing:\n" + md)
    expect("vote not counted: refuter" in md, "demoted vote not shown:\n" + md)
    expect("1 vote(s) did not count" in md and "no source" in md, "cap with reason missing:\n" + md)


@case
def d2_demoted_refuting_vote_does_not_refute(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    L.verdict(L.keys()[0], "--refuted", "yes", "--tier", "read")
    j = L.report("json")
    expect(not j["groups"]["refuted"], "demoted vote refuted the finding")
    expect(len(j["groups"]["pending"]) == 1, "finding should stay pending")


@case
def d2_legacy_ledger_demoted_vote_not_counted(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    data = L.data()
    f = list(data["findings"].values())[0]
    f["votes"].append({"by": "old", "refuted": "no", "tier": "inferred", "source": None,
                       "reason": "[demoted: executed label with no source]"})
    with open(L.path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    j = L.report("json")
    expect(not j["groups"]["survived"], "legacy demoted vote still counted")


@case
def old_inferred_vote_still_counts(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    L.verdict(L.keys()[0], "--refuted", "no", "--tier", "inferred", "--reason", "logic holds")
    j = L.report("json")
    expect(len(j["groups"]["survived"]) == 1, "honest inferred vote should count")
    expect(not j.get("votes_not_counted"), "inferred vote reported as not counted")


@case
def old_untiered_vote_still_counts(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    L.verdict(L.keys()[0], "--refuted", "no")
    j = L.report("json")
    expect(len(j["groups"]["survived"]) == 1, "vote with no tier should still count")


@case
def old_sourced_vote_survives_and_blocked_ignored(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    k = L.keys()[0]
    L.verdict(k, "--refuted", "blocked", "--reason", "read_file denied")
    j = L.report("json")
    expect(len(j["groups"]["pending"]) == 1, "blocked vote alone should leave it pending")
    L.verdict(k, "--refuted", "no", "--tier", "executed", "--source", "pytest -> 1 failed")
    j = L.report("json")
    expect(len(j["groups"]["survived"]) == 1, "sourced vote should make it survive")
    md = L.report()
    expect("Votes: 1 upheld, 0 refuted, 1 blocked." in md, "tally format changed:\n" + md)
    expect("Unverified" not in md, "unverified section shown at standard scale")


@case
def old_full_scale_needs_three_votes(t):
    L = Ledger(t, "full")
    L.add([rec()])
    k = L.keys()[0]
    for _ in range(2):
        L.verdict(k, "--refuted", "no", "--tier", "executed", "--source", "run -> ok")
    expect(L.report("json")["groups"]["pending"], "two votes should not be enough at full")
    L.verdict(k, "--refuted", "yes", "--tier", "read", "--source", 'a.py:1 "the call is guarded here"')
    j = L.report("json")
    expect(len(j["groups"]["survived"]) == 1, "2 of 3 upheld should survive")


# ---------------------------------------------------------------- defect 3: quotes

def read_tier_after(t, source):
    L = Ledger(t, "standard")
    L.add([rec(tier="read", source=source)])
    f = L.finding()
    return f["tier"], f.get("demoted")


@case
def d3_single_quoted_fragment_is_not_a_quote(t):
    tier, why = read_tier_after(t, "app/auth.py:9 'abc'")
    expect(tier == "inferred" and "quotes nothing" in (why or ""), "kept tier %s" % tier)


@case
def d3_apostrophes_are_not_a_quote(t):
    tier, _ = read_tier_after(t, "app/auth.py:9, the user's token isn't revoked")
    expect(tier == "inferred", "apostrophes accepted as a quote")


@case
def d3_short_double_quote_is_not_enough(t):
    tier, _ = read_tier_after(t, 'app/auth.py:9, "abcd"')
    expect(tier == "inferred", "one-word quote accepted")


@case
def old_double_quoted_line_is_a_quote(t):
    tier, why = read_tier_after(t, 'app/auth.py:9, "if token is None: return"')
    expect(tier == "read" and not why, "real quote demoted: %s" % why)


@case
def old_typographic_quote_is_a_quote(t):
    tier, why = read_tier_after(t, "app/auth.py:9, “revoke the access token only”")
    expect(tier == "read" and not why, "typographic quote demoted: %s" % why)


@case
def old_wrapped_label_source_is_unwrapped(t):
    tier, _ = read_tier_after(t, 'read ("app/auth.py:9", "session.revoke(access_token) only")')
    expect(tier == "read", "wrapped read source demoted")


# ---------------------------------------------------------------- defect 4: nearby lines

@case
def d4_adjacent_lines_are_deduplicated(t):
    L = Ledger(t, "standard")
    L.add([rec(location="app/auth.py:9")])
    out = L.add([rec(location="app/auth.py:10")], rnd=1, by="finder2").stdout
    expect("duplicate of" in out and len(L.keys()) == 1, "adjacent duplicate kept:\n" + out)


@case
def d4_line_range_within_five_is_compared(t):
    L = Ledger(t, "standard")
    L.add([rec(location="app/auth.py:9-12")])
    out = L.add([rec(location="app\\auth.py:17")]).stdout
    expect("duplicate of" in out, "range within 5 lines not compared:\n" + out)


@case
def d4_nearby_possible_duplicate_is_flagged(t):
    L = Ledger(t, "standard")
    L.add([rec("logout does not revoke the refresh token", "app/auth.py:9")])
    out = L.add([rec("refresh token lives forever after password change", "app/auth.py:12")]).stdout
    expect("possible duplicate of" in out and len(L.keys()) == 2, "no flag for nearby record:\n" + out)


@case
def old_far_lines_are_not_merged(t):
    L = Ledger(t, "standard")
    L.add([rec(location="app/auth.py:9")])
    out = L.add([rec(location="app/auth.py:15")]).stdout
    expect("duplicates=0" in out and "possible duplicate" not in out and len(L.keys()) == 2, "6 lines apart merged:\n" + out)


@case
def old_other_file_is_not_merged(t):
    L = Ledger(t, "standard")
    L.add([rec(location="app/auth.py:9")])
    out = L.add([rec(location="app/files.py:9")]).stdout
    expect("duplicates=0" in out and "possible duplicate" not in out and len(L.keys()) == 2, "other file merged:\n" + out)


@case
def old_same_location_merge_and_distinct_kept(t):
    L = Ledger(t, "standard")
    L.add([rec("logout does not revoke the refresh token", "https://example.com/docs#session")])
    out = L.add([rec("the refresh token is not revoked by logout", "https://example.com/docs#session"),
                 rec("password hashing uses md5", "https://example.com/docs#session")]).stdout
    expect(out.count("duplicate of") == 1 and len(L.keys()) == 2, "identical-location dedup changed:\n" + out)


@case
def old_exact_key_duplicate_and_rejected_stay_seen(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    L.verdict(L.keys()[0], "--refuted", "yes", "--tier", "executed", "--source", "pytest -> passed")
    L.run("close-round", L.path, "--round", "1")
    out = L.add([rec()], rnd=2).stdout
    expect("duplicate of" in out and "fresh=0" in out, "refuted finding came back:\n" + out)


# ---------------------------------------------------------------- defect 5: schema validation

@case
def d5_bad_severity_is_rejected(t):
    L = Ledger(t, "standard")
    out = L.add([rec(severity="urgent")]).stdout
    expect("rejected" in out and "severity" in out and "rejected=1" in out, "bad severity accepted:\n" + out)
    expect(not L.keys(), "record stored")


@case
def d5_wrong_type_is_rejected_cleanly(t):
    L = Ledger(t, "standard")
    p = L.add([rec(claim=42), rec(hypothesis="yes"), "not a record"])
    expect(p.returncode == 0 and "Traceback" not in p.stderr, "crashed: %s" % p.stderr[-300:])
    expect("rejected=3" in p.stdout, "expected 3 rejections:\n" + p.stdout)
    expect("claim must be a string" in p.stdout, "message unclear:\n" + p.stdout)


@case
def d5_verdicts_file_is_validated(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    k = L.keys()[0]
    path = L.write([
        {"key": k, "refuted": "maybe", "tier": "read", "reason": "x"},
        {"key": k, "refuted": "no", "tier": "executed", "source": "pytest -> 1 failed"},
        {"key": "nosuchkey", "refuted": "no", "tier": "inferred", "reason": "x"},
        {"status": "done", "key": k, "refuted": "no", "lens": "security", "tier": "executed",
         "source": "pytest -> 1 failed", "reason": "reproduced", "error": ""},
    ])
    p = L.run("verdicts", L.path, path, "--by", "refuter")
    expect(p.returncode == 0, "verdicts failed: %s" % p.stderr)
    expect("recorded=1 rejected=3" in p.stdout, "wrong tally:\n" + p.stdout)
    expect("'maybe' is not one of" in p.stdout and "reason is required" in p.stdout, "messages:\n" + p.stdout)
    expect(len(L.report("json")["groups"]["survived"]) == 1, "valid verdict not counted")


@case
def old_missing_required_field_is_rejected(t):
    L = Ledger(t, "standard")
    out = L.add([{"claim": "x is wrong", "location": "a.py:1"}, rec(location=""),
                 rec(tier="guessed")]).stdout
    expect("rejected=3" in out, "expected 3 rejections:\n" + out)


@case
def old_missing_source_is_demoted_not_rejected(t):
    L = Ledger(t, "standard")
    out = L.add([rec(tier="executed"), rec("price is wrong", "app/pricing.py:3", "observed", source=None)]).stdout
    expect("demoted=2" in out and "rejected=0" in out, "missing source not demoted:\n" + out)
    expect(all(f["tier"] == "inferred" for f in L.data()["findings"].values()), "tier kept")


@case
def old_finder_envelope_and_extra_fields_accepted(t):
    L = Ledger(t, "standard")
    out = L.add({"status": "done", "findings": [rec(severity="high", dimension="session",
                 falsifier="a revoke call", hypothesis=True, extra="x")], "covered": []}).stdout
    expect("fresh=1" in out and "rejected=0" in out, "envelope not accepted:\n" + out)
    expect(L.finding()["severity"] == "high", "severity lost")


# ---------------------------------------------------------------- rest of the old behaviour

@case
def old_rounds_dry_stop_and_ceiling(t):
    L = Ledger(t, "full")
    L.add([rec()])
    out = L.run("close-round", L.path, "--round", "1").stdout
    expect("CONTINUE" in out, out)
    out = L.run("close-round", L.path, "--round", "2").stdout
    expect("CONTINUE" in out and "dry=1 of 2" in out, out)
    out = L.run("close-round", L.path, "--round", "3").stdout
    expect("STOP: 2 consecutive dry round(s)" in out, out)
    p = L.run("close-round", L.path, "--round", "3")
    expect(p.returncode == 2 and "already closed" in p.stderr, "closing twice allowed")
    second = os.path.join(t, "quick")
    os.makedirs(second)
    L2 = Ledger(second, "quick")
    L2.add([rec()])
    out = L2.run("close-round", L2.path, "--round", "1").stdout
    expect("STOP: round ceiling 1 reached" in out, out)
    expect(any("round ceiling" in c for c in L2.report("json")["caps"]), "ceiling cap missing")


@case
def old_merge_children_and_init_output(t):
    L = Ledger(t, "standard", "--votes", "2")
    expect("scale=standard max_rounds=3 dry_stop=1 votes=2" in L.last.stdout, L.last.stdout)
    L.add([rec(), rec("pricing overflows", "app/pricing.py:80")])
    a, b = L.keys()
    L.verdict(b, "--refuted", "no", "--tier", "executed", "--source", "run -> ok")
    out = L.run("merge", L.path, a, b).stdout
    expect("merged %s into %s" % (b, a) in out, out)
    expect(len(L.data()["findings"][a]["votes"]) == 1, "votes not moved")
    L.run("child", L.path, "--id", "c1", "--agent", "gravitas-finder", "--status", "denied", "--note", "no read")
    md = L.report()
    expect("- gravitas-finder c1: denied (no read)" in md, md)
    expect("never reached the 2 vote(s)" in md, md)
    p = L.run("init", L.path, "--scale", "quick")
    expect(p.returncode == 2 and "--force" in p.stderr, "init overwrote without --force")


# ---------------------------------------------------------------- follow-ups from the verifier

@case
def f1_blocked_status_vote_does_not_count(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    key = L.keys()[0]
    path = L.write([{"key": key, "status": "blocked", "refuted": "no", "tier": "inferred",
                     "reason": "could not open the file", "error": "relative path"}])
    L.run("verdicts", L.path, path, "--by", "refuter")
    expect(L.report("json")["groups"]["survived"] == [], "a blocked vote made the finding survive: %s" % L.last.stdout)


@case
def f2_code_quote_is_a_quote(t):
    L = Ledger(t, "quick")
    L.add([rec(tier="read", source='app/auth.py:9, "revokeAccess(token)"')])
    expect(L.finding()["tier"] == "read", "a 19-character code quote was demoted: %s" % L.last.stdout)


@case
def f3_quoted_path_is_not_a_quote(t):
    L = Ledger(t, "quick")
    L.add([rec(tier="read", source='"src/auth/session.ts"')])
    expect(L.finding()["tier"] == "inferred", "a quoted path passed as a quotation")
    second = os.path.join(t, "b")
    os.makedirs(second)
    L2 = Ledger(second, "quick")
    L2.add([rec(tier="read", source='"auth.py:9"')])
    expect(L2.finding()["tier"] == "inferred", "a quoted location passed as a quotation")


@case
def f4_nearby_distinct_defects_are_flagged_not_dropped(t):
    L = Ledger(t, "quick")
    L.add([rec(claim="query builds SQL from user input without escaping", location="db.py:10")])
    L.add([rec(claim="query builds SQL from request params without escaping", location="db.py:14")])
    expect(len(L.keys()) == 2, "a distinct nearby defect was dropped: %s" % L.last.stdout)
    expect("possible duplicate" in L.last.stdout, "the nearby finding was not flagged: %s" % L.last.stdout)


@case
def f5_read_vote_without_quote_is_demoted(t):
    L = Ledger(t, "standard")
    L.add([rec()])
    L.verdict(L.keys()[0], "--refuted", "no", "--tier", "read", "--source", "app/auth.py:9", "--reason", "fine")
    expect(L.report("json")["groups"]["survived"] == [], "a read vote quoting nothing counted")


@case
def f6_vote_on_merged_key_is_redirected(t):
    L = Ledger(t, "standard")
    L.add([rec(claim="logout keeps the refresh token alive", location="a.py:1")])
    L.add([rec(claim="refresh tokens are never deleted on sign out", location="b.py:1")])
    keep, dup = L.keys()
    L.run("merge", L.path, keep, dup)
    L.verdict(dup, "--refuted", "no", "--tier", "inferred", "--reason", "confirmed")
    expect("merged into" in L.last.stdout, "no redirect message: %s" % L.last.stdout)
    expect(len(L.data()["findings"][keep]["votes"]) == 1, "the vote did not reach the kept finding")


@case
def f7_blocked_finder_envelope_is_recorded(t):
    L = Ledger(t, "quick")
    p = L.add({"status": "blocked", "error": "read_file denied"})
    expect(p.returncode == 0 and "blocked" in p.stdout and "read_file denied" in p.stdout, p.stdout + p.stderr)
    expect(L.data()["rounds"]["1"].get("blocked"), "the blocked envelope was not recorded")


@case
def f8_bom_input_is_read(t):
    L = Ledger(t, "quick")
    path = os.path.join(t, "bom.json")
    with open(path, "w", encoding="utf-8-sig") as fh:
        json.dump([rec()], fh)
    p = L.run("add", L.path, path, "--round", "1", "--by", "finder")
    expect(p.returncode == 0 and len(L.keys()) == 1, p.stdout + p.stderr)


def main():
    failed = 0
    for fn in CASES:
        root = tempfile.mkdtemp(prefix="ledger-test-")
        try:
            fn(root)
            print("PASS %s" % fn.__name__)
        except Exception as e:  # noqa: BLE001 - every failure is reported, not raised
            failed += 1
            detail = str(e).strip().splitlines()
            print("FAIL %s: %s" % (fn.__name__, " | ".join(detail[:6])))
        finally:
            shutil.rmtree(root, ignore_errors=True)
    print("%d of %d passed" % (len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
