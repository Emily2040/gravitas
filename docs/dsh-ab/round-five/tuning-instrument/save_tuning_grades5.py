#!/usr/bin/env python3
"""Save a round-five tuning grading workflow's output against its id map, after validating every grade.

    python save_tuning_grades5.py BATCH OUTPUT.json [OUTPUT2.json ...]    -> grades-BATCH.json, only if nothing is wrong
    python save_tuning_grades5.py BATCH OUTPUT.json --replace             move an existing grades-BATCH.json aside first
                                                                          (tuning_check5.py then returns STOP_ASK_EMILY
                                                                          for a pass batch; see README)
    options: --base4 DIR, --base5 DIR, --inst DIR (folders; the defaults are the real ones)

OUTPUT is what the Workflow tool returned for one script of the batch (part or rerun): the list [{id, grade}], or an
object whose "result" is that list. Save every part output as soon as it returns, and before building any rerun.

Every row received is appended to ledger5.jsonl (time, batch, idmap_sha256, file, id, valid, problems, grade). For
each id the grade used is the earliest valid row on the whole ledger for this batch and id map, whatever order the
files are given in and whatever later outputs hold (a later valid grade for the same id is reported and not used).
That is how the rule's "one shuffled batch" per pass is kept: a regrade never replaces a grade already on the ledger.
A grade is valid when:
  - it matches the frozen schema (tuning-grade-schema5.json) specialised to its case: every key point id with one of
    correct/vague/missing/wrong, every LKP id with one of KEPT/FLAT/WRONG/ABSENT and a quote string, every premise id
    (the gated one and the reported ones) with yes/no, the lists AW, AU, S, SP, SR of {quote, reason} with both
    non-empty, PC yes/no, PC_quote a string, and no other key;
  - its "id" is the row's id;
  - PC is "yes" exactly when the gated premise point (premise-points.json "premise") is "yes" in PC_points;
  - an LKP is ABSENT exactly when its key point is "missing".
grades-BATCH.json is written only when every id of the map has a valid grade, no row names an id outside the map,
the id map's scripts are unchanged, and every mapped answer on disk still has the sha256 the map recorded.
Otherwise nothing is written (except the ledger), every problem is listed, and the exit code is 1.
Reported, not refused: quotes not found word for word in the answer, empty quotes for a non-ABSENT LKP or a "yes" PC.
Standard library only.
"""
import argparse
import datetime
import json
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tuning_common5 as T  # noqa: E402


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def now_us():
    """Ledger row times to the microsecond, so tuning_check5.py can order a row against a rerun's build time."""
    return datetime.datetime.now().astimezone().isoformat(timespec="microseconds")


def append_ledger(inst, entries):
    lock = os.path.join(inst, T.LEDGER_FILE + ".lock")
    for _ in range(200):
        try:
            os.mkdir(lock)
            break
        except FileExistsError:
            time.sleep(0.05)
    else:
        raise SystemExit("ledger lock %s held for 10 s; remove it if no save is running" % lock)
    try:
        with open(os.path.join(inst, T.LEDGER_FILE), "a", encoding="utf-8", newline="\n") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    finally:
        os.rmdir(lock)


def save(batch, outputs, inst=T.INST, b4=T.B4, b5=T.B5, replace=False, quiet=False):
    """Returns (ok, problems, notes)."""
    say = (lambda *a: None) if quiet else print
    map_path = os.path.join(inst, "maps", "%s-idmap.json" % batch)
    problems, notes = [], []
    try:
        idmap = T.read_json(map_path)
    except (OSError, ValueError) as e:
        return False, ["id map %s unreadable (%s)" % (map_path, e.__class__.__name__)], []
    if idmap.get("batch") != batch:
        return False, ["id map %s is for batch %r" % (map_path, idmap.get("batch"))], []
    info, probs = T.load_case_lists(inst, b4)
    if probs:
        return False, probs, []
    base_schema = T.read_json(os.path.join(inst, T.SCHEMA_FILE))
    if T.sha256_file(os.path.join(inst, T.SCHEMA_FILE)) != idmap.get("schema_sha256"):
        problems.append("tuning-grade-schema5.json changed since the batch was built")
    for f in (T.LKP_FILE, T.PREMISE_FILE):
        if T.sha256_file(os.path.join(inst, f)) != idmap.get(f.split("-")[0].split(".")[0] + "_sha256"):
            problems.append("%s changed since the batch was built" % f)
    for part in idmap.get("parts", []):
        if T.sha256_file(os.path.join(inst, part["file"])) != part["sha256"]:
            problems.append("%s is not the script the id map recorded" % part["file"])
    with open(os.path.join(inst, T.PROMPT_FILE), encoding="utf-8") as f:
        if T.sha256_text(f.read().rstrip()) != idmap.get("prompt_sha256"):
            notes.append("tuning-grader-prompt5.md changed since the batch was built (the grades carry the batch's "
                         "prompt sha256; tuning_check5.py compares it with the calibration's)")
    by_id = {it["id"]: it for it in idmap["items"]}
    answers = {}
    for iid, m in by_id.items():
        t, err = T.packaged_text(T.answer_path(m["case"], m["arm"], m["run"], b4, b5))
        if err:
            problems.append("%s: answer file %s" % (iid, err))
        elif T.sha256_text(t) != m["answer_sha256"]:
            problems.append("%s: the answer on disk is not the answer this batch graded" % iid)
        else:
            answers[iid] = t
    schemas = {c: T.schema_for_case(base_schema, info[c]["kp"], info[c]["lkp"], info[c]["pc_points"]) for c in T.CASES}
    idmap_sha = T.sha256_file(map_path)
    given, ledger = [], []
    for path in outputs:
        try:
            rows = T.read_outputs(path)
        except (OSError, ValueError) as e:
            problems.append("output %s unreadable (%s)" % (path, e))
            continue
        for n, row in enumerate(rows):
            rid = row.get("id") if isinstance(row, dict) else None
            grade = row.get("grade") if isinstance(row, dict) else None
            entry = {"time": now_us(), "batch": batch, "idmap_sha256": idmap_sha, "file": os.path.abspath(path), "row": n,
                     "id": rid, "valid": False, "problems": [], "grade": grade}
            if rid not in by_id:
                entry["problems"] = ["id %r is not in the %s id map" % (rid, batch)]
                problems.append("output %s row %d: id %r is not in the %s id map" % (path, n, rid, batch))
            elif grade is None:
                entry["problems"] = ["no grade (the agent returned nothing)"]
            else:
                m = by_id[rid]
                p, _ = T.validate_grade(grade, schemas[m["case"]], rid, answers.get(rid), info[m["case"]]["premise"])
                entry["problems"], entry["valid"] = p, not p
                if not p:
                    given.append((rid, path, n, grade))
            ledger.append(entry)
    if ledger:
        append_ledger(inst, ledger)
    # The grade used for each id is the earliest valid row on the whole ledger for this batch and id map, so the order
    # in which output files are given, or a later regrade, never changes which grade counts (one batch per pass).
    lrows, lprobs = T.read_ledger(inst)
    problems += lprobs
    brows = T.batch_rows(lrows, batch, idmap_sha)
    first = T.first_valid_rows(brows)
    chosen, warn, used_files = {}, {}, []
    for iid in sorted(by_id):
        r = first.get(iid)
        if r is None:
            bad = [e for e in brows if e.get("id") == iid]
            why = "; ".join(sorted({x for e in bad for x in e.get("problems", [])})) or "no row for it on the ledger"
            problems.append("%s has no valid grade: %s" % (iid, why))
            continue
        case = by_id[iid]["case"]
        p, w = T.validate_grade(r.get("grade"), schemas[case], iid, answers.get(iid), info[case]["premise"])
        if p:
            problems.append("%s: its earliest valid grade on the ledger (line %d) no longer validates: %s"
                            % (iid, r["_line"], "; ".join(p[:2])))
            continue
        chosen[iid], warn[iid] = r["grade"], w
        if r.get("file") not in used_files:
            used_files.append(r.get("file"))
    for rid, path, n, grade in given:
        if rid in chosen and grade != chosen[rid]:
            notes.append("%s: the valid grade in output %s row %d is not used; the earliest valid grade on the ledger "
                         "is (line %d, %s)" % (rid, path, n, first[rid]["_line"], first[rid].get("file")))
    n_warn = sum(len(w) for w in warn.values())
    for iid in sorted(warn):
        for w in warn[iid]:
            say("note: %s %s" % (iid, w))
    for n in notes:
        say("note: " + n)
    if problems:
        say("REFUSED: grades-%s.json not written. Problems (%d):" % (batch, len(problems)))
        for p in problems:
            say("  - " + p)
        return False, problems, notes
    out_path = os.path.join(inst, "grades-%s.json" % batch)
    if os.path.exists(out_path):
        if not replace:
            say("REFUSED: %s exists (use --replace to move it aside)" % out_path)
            return False, ["%s exists" % out_path], notes
        say("moved the old file to %s" % T.move_aside(out_path))
        say("WARNING: a superseded grades-%s.json now exists; tuning_check5.py returns STOP_ASK_EMILY for a pass batch "
            "and does not count a calibration batch with one" % batch)
    items = []
    for it in idmap["items"]:
        items.append({"id": it["id"], "case": it["case"], "arm": it["arm"], "run": it["run"],
                      "answer_sha256": it["answer_sha256"], "warnings": warn.get(it["id"], []),
                      "grade": chosen[it["id"]]})
    T.write_json(out_path, {"batch": batch, "pass": idmap.get("pass"), "seed": idmap.get("seed"), "saved": now(),
                            "idmap_sha256": idmap_sha, "prompt_sha256": idmap["prompt_sha256"],
                            "schema_sha256": idmap["schema_sha256"], "lkp_sha256": idmap["lkp_sha256"],
                            "premise_sha256": idmap["premise_sha256"], "outputs": used_files,
                            "outputs_given": [os.path.abspath(p) for p in outputs],
                            "quote_warnings": n_warn, "items": items})
    say("wrote %s: %d grades (%d quote or evidence warnings, listed above)" % (out_path, len(items), n_warn))
    return True, [], notes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch")
    ap.add_argument("outputs", nargs="+")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--base4", default=T.B4)
    ap.add_argument("--base5", default=T.B5)
    ap.add_argument("--inst", default=T.INST)
    a = ap.parse_args()
    ok, _, _ = save(a.batch, a.outputs, a.inst, a.base4, a.base5, a.replace)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
