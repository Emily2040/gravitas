#!/usr/bin/env python3
"""Build one grading batch of the round-five tuning instrument: an id map and the Workflow script(s) that grade it.

    python make_tuning_grade_script.py calibration          the 48 round-four baselines (ids t001-t048)
    python make_tuning_grade_script.py pass1                the 12 c5 answers of pass 1 + the 48 baselines (t101-t160)
    python make_tuning_grade_script.py pass2                the same for pass 2 (t201-t260)
    python make_tuning_grade_script.py calibration2         a recalibration after a rubric fix (t301-t348; calibration3: t401-)
    python make_tuning_grade_script.py BATCH --only t103,t117   a rerun script for those ids from the existing id map;
                                                refused for an id that has a valid grade on ledger5.jsonl, or that has
                                                no ledger row yet (save the part outputs first)
    options: --replace (move an existing map and its scripts aside first; tuning_check5.py then returns
             STOP_ASK_EMILY for a pass batch and does not count a calibration batch), --max-bytes N (default 500000),
             --base4 DIR, --base5 DIR, --inst DIR (folders; the defaults are the real ones)

What it writes (nothing else, and nothing outside --inst):
    maps/<batch>-idmap.json            id -> case, arm, run, answer path and sha256; the grader never sees this file
    workflows/<batch>/grade-<batch>.part<k>.js   one Workflow script per part, each under --max-bytes
    workflows/<batch>/grade-<batch>.rerun<k>.js  (--only) and maps/<batch>-reruns.json, which records each rerun

Each script embeds its batch as a constant (as round four's dev/make_label_script.py did), because the Workflow tool
takes its arguments inline. It runs one agent per answer with model 'opus' and the per-case schema (the frozen
tuning-grade-schema5.json with that case's ids required), labels agents by opaque id only, and returns
[{id, grade}] for every id of the part (grade null when an agent returned nothing). The agent prompt is the frozen
tuning-grader-prompt5.md, then the case's packet (request, round-four key, key points, LKP ids, the PC premise id
and the other premise corrections), then the answer and the delivery lines. No arm, run or file name is in any script.

Order: the items are shuffled with the batch's written seed (tuning_common5.BATCHES) and numbered in that order, so
neither the order nor the id says which arm or run an answer came from. Standard library only.
"""
import argparse
import datetime
import json
import os
import random
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tuning_common5 as T  # noqa: E402

MAX_BYTES = 500000
ARM_STRINGS = ("gv-plain", "gv-grav", "gv-grav-base", "gv-grav-c5", "raw\\", "tuning\\", ".r1.", ".r2.")


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def batch_items(batch, b4, b5):
    """[(case, arm, run)] for the batch, in a fixed order before shuffling."""
    items = [(c, a, r) for c in T.CASES for a, r in T.BASELINE_GROUPS]
    n = T.batch_pass(batch)
    if n is not None:
        items += [(c, T.C5, "r%d" % n) for c in T.CASES]
    return items


def case_head(case, info, b4):
    """The packet text shared by every answer of one case."""
    def rd(p):
        with open(p, encoding="utf-8-sig") as f:
            return f.read().strip()
    req = rd(os.path.join(b4, "prompts", case + ".txt"))
    key = rd(os.path.join(b4, "keys", case + ".md"))
    pts = "\n".join("%s. %s" % (x["id"], x["point"].strip()) for x in info[case]["points"])
    return ("## Packet\n\n### Request\n\n%s\n\n### Answer key\n\n%s\n\n### Key points\n\n%s\n\n"
            "### Limited key points (LKP ids)\n\n%s\n\n### Premise point for PC (id)\n\n%s\n\n"
            "### Other premise corrections (ids; marked in PC_points, not part of PC)\n\n%s"
            % (req, key, pts, ", ".join(info[case]["lkp"]), ", ".join(info[case]["premise"]),
               ", ".join(info[case]["reported"]) or "none"))


def answer_block(item_id, answer):
    return ("### Answer (id %s)\n\n===== ANSWER START =====\n%s\n===== ANSWER END =====\n\n"
            "Output: do not write any file. Return the JSON object described above through the StructuredOutput tool, "
            "with \"id\" set to \"%s\". Do not open any file, do not search the web, and do not look for other "
            "answers, runs, maps or grades." % (item_id, answer, item_id))


def full_prompt(grader_prompt, head, block):
    """Exactly the string the Workflow script builds: graderPrompt + blank line + head + blank line + block."""
    return grader_prompt + "\n\n" + head + "\n\n" + block


JS_TEMPLATE = """export const meta = {
  name: '%(name)s',
  description: '%(description)s',
  phases: [{ title: 'Grade', detail: 'one opus session per answer, blind to arm and run' }],
}
const EMBEDDED = %(embedded)s;
// Built by make_tuning_grade_script.py. Each agent gets the frozen grader prompt, its case's packet and one answer,
// and returns the grade object through the per-case schema. Agents are labelled by opaque id only.
phase('Grade')
const prompt = (it) => EMBEDDED.graderPrompt + '\\n\\n' + EMBEDDED.cases[it.c].head + '\\n\\n' + it.block
const jobs = EMBEDDED.items.map((it) => () =>
  agent(prompt(it), { label: `grade:${it.id}`, phase: 'Grade', model: 'opus', schema: EMBEDDED.cases[it.c].schema })
    .then((grade) => ({ id: it.id, grade: grade || null })))
const results = await parallel(jobs)
const rows = EMBEDDED.items.map((it, i) => results[i] || { id: it.id, grade: null })
const done = rows.filter((r) => r.grade).length
log(`${EMBEDDED.batch} ${EMBEDDED.part}: ${done} of ${rows.length} grades returned`)
if (done < rows.length) log(`no grade for: ${rows.filter((r) => !r.grade).map((r) => r.id).join(', ')} (save_tuning_grades5.py lists them; build a rerun with --only)`)
return rows
"""


def js_json(obj):
    """JSON as a JavaScript literal: U+2028 and U+2029 escaped (older engines reject them inside string literals)."""
    return json.dumps(obj, ensure_ascii=False).replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def render(batch, part_label, n_parts_label, items, heads, schemas, grader_prompt):
    cases = sorted({it["c"] for it in items})
    emb = {"batch": batch, "part": part_label, "graderPrompt": grader_prompt,
           "cases": {c: {"head": heads[c], "schema": schemas[c]} for c in cases},
           "items": [{"id": it["id"], "c": it["c"], "block": it["block"]} for it in items]}
    name = re.sub(r"[^a-z0-9-]", "-", ("round-five-tuning-grades-%s-%s" % (batch, part_label)).lower())
    desc = ("Round-five tuning grader (opus): one answer per session, blind to arm and run; %s %s%s, %d answers"
            % (batch, part_label, n_parts_label, len(items)))
    return JS_TEMPLATE % {"name": name, "description": desc, "embedded": js_json(emb)}


def blind_problems(script, items):
    """Arm, run or folder strings anywhere in a script outside the answers themselves."""
    probe = script
    for it in items:
        probe = probe.replace(js_json(it["block"])[1:-1], "")
    return [s for s in ARM_STRINGS if s in probe]


def split_parts(batch, items, heads, schemas, grader_prompt, max_bytes):
    """Greedy split in id order so that every script is under max_bytes."""
    parts, cur = [], []
    for it in items:
        trial = cur + [it]
        if len(render(batch, "partX", " of N", trial, heads, schemas, grader_prompt).encode("utf-8")) > max_bytes - 64:
            if not cur:
                raise SystemExit("one answer alone (%s) makes a script over %d bytes" % (it["id"], max_bytes))
            parts.append(cur)
            cur = [it]
        else:
            cur = trial
    if cur:
        parts.append(cur)
    return parts


def load_inputs(inst, b4):
    info, probs = T.load_case_lists(inst, b4)
    if probs:
        raise SystemExit("cannot build: " + "; ".join(probs))
    with open(os.path.join(inst, T.PROMPT_FILE), encoding="utf-8") as f:
        grader_prompt = f.read().rstrip()
    base_schema = T.read_json(os.path.join(inst, T.SCHEMA_FILE))
    heads = {c: case_head(c, info, b4) for c in T.CASES}
    schemas = {c: T.schema_for_case(base_schema, info[c]["kp"], info[c]["lkp"], info[c]["pc_points"]) for c in T.CASES}
    return info, grader_prompt, heads, schemas


def build(batch, inst, b4, b5, max_bytes, replace):
    if batch not in T.BATCHES:
        raise SystemExit("unknown batch %r (one of %s)" % (batch, ", ".join(T.BATCHES)))
    offset, seed = T.BATCHES[batch]
    map_path = os.path.join(inst, "maps", "%s-idmap.json" % batch)
    wf_dir = os.path.join(inst, "workflows", batch)
    if os.path.exists(map_path):
        if not replace:
            raise SystemExit("%s exists; a batch is built once (use --replace to move it and its scripts aside)" % map_path)
        print("WARNING: rebuilding %s leaves a superseded id map; the rule grades each pass as one shuffled batch, so "
              "tuning_check5.py will return STOP_ASK_EMILY for a rebuilt pass batch and will not count a rebuilt "
              "calibration batch (use the next calibration batch instead)" % batch)
        moved = T.move_aside(map_path)
        print("moved the old id map to %s" % moved)
        if os.path.isdir(wf_dir):
            k = 1
            while os.path.exists("%s.superseded-%d" % (wf_dir, k)):
                k += 1
            os.replace(wf_dir, "%s.superseded-%d" % (wf_dir, k))
            print("moved the old scripts to %s.superseded-%d" % (wf_dir, k))
        rr_old = T.move_aside(os.path.join(inst, "maps", "%s-reruns.json" % batch))
        if rr_old:
            print("moved the old rerun record to %s" % rr_old)
    info, grader_prompt, heads, schemas = load_inputs(inst, b4)
    raw = batch_items(batch, b4, b5)
    texts, problems = {}, []
    for c, a, r in raw:
        p = T.answer_path(c, a, r, b4, b5)
        t, err = T.packaged_text(p)
        if err:
            problems.append("%s %s" % (p, err))
        else:
            texts[(c, a, r)] = (p, t)
    if problems:
        raise SystemExit("cannot build %s; these answers are missing or blank (a blank run is rerun before grading):\n  %s"
                         % (batch, "\n  ".join(problems)))
    order = list(raw)
    random.Random(seed).shuffle(order)
    items, map_items = [], []
    for i, (c, a, r) in enumerate(order, 1):
        iid = "t%03d" % (offset + i)
        p, t = texts[(c, a, r)]
        block = answer_block(iid, t)
        items.append({"id": iid, "c": c, "block": block})
        map_items.append({"id": iid, "case": c, "arm": a, "run": r,
                          "path": os.path.relpath(p, b5 if a == T.C5 else b4).replace("\\", "/"),
                          "answer_sha256": T.sha256_text(t), "chars": len(t),
                          "prompt_sha256": T.sha256_text(full_prompt(grader_prompt, heads[c], block))})
    parts = split_parts(batch, items, heads, schemas, grader_prompt, max_bytes)
    os.makedirs(wf_dir, exist_ok=True)
    part_rows = []
    for k, part in enumerate(parts, 1):
        script = render(batch, "part%d" % k, " of %d" % len(parts), part, heads, schemas, grader_prompt)
        bad = blind_problems(script, part)
        if bad:
            raise SystemExit("blindness check failed: %s appears in the script outside the answers" % ", ".join(bad))
        leaks = [s for s in ARM_STRINGS[:4] if any(s in it["block"] for it in part)]
        if leaks:
            print("WARNING: an answer itself contains %s (left as written; the grader sees it)" % ", ".join(leaks))
        data = script.encode("utf-8")
        assert len(data) <= max_bytes
        fn = os.path.join(wf_dir, "grade-%s.part%d.js" % (batch, k))
        with open(fn, "wb") as f:
            f.write(data)
        part_rows.append({"file": os.path.relpath(fn, inst).replace("\\", "/"), "sha256": T.sha256_bytes(data),
                          "bytes": len(data), "ids": [it["id"] for it in part]})
        print("wrote %s: %d answers, %d bytes" % (fn, len(part), len(data)))
    idmap = {"batch": batch, "pass": T.batch_pass(batch), "seed": seed, "id_offset": offset, "created": now(),
             "note": "The grader never sees this file. Ids were numbered after shuffling with the seed above.",
             "prompt_file": T.PROMPT_FILE, "prompt_sha256": T.sha256_text(grader_prompt),
             "schema_sha256": T.sha256_file(os.path.join(inst, T.SCHEMA_FILE)),
             "lkp_sha256": T.sha256_file(os.path.join(inst, T.LKP_FILE)),
             "premise_sha256": T.sha256_file(os.path.join(inst, T.PREMISE_FILE)),
             "rule_sha256": T.sha256_file(T.RULE_FILE) if inst == T.INST else None,
             "items": map_items, "parts": part_rows}
    T.write_json(map_path, idmap)
    print("wrote %s: %d ids (%s to %s), seed %d" % (map_path, len(map_items), map_items[0]["id"], map_items[-1]["id"], seed))
    return idmap


def rerun(batch, ids, inst, b4, b5, max_bytes):
    map_path = os.path.join(inst, "maps", "%s-idmap.json" % batch)
    idmap = T.read_json(map_path)
    info, grader_prompt, heads, schemas = load_inputs(inst, b4)
    if T.sha256_text(grader_prompt) != idmap["prompt_sha256"]:
        raise SystemExit("the grader prompt changed since %s was built; a rerun must use the batch's prompt" % batch)
    by_id = {it["id"]: it for it in idmap["items"]}
    unknown = [i for i in ids if i not in by_id]
    if unknown:
        raise SystemExit("not ids of %s: %s" % (batch, ", ".join(unknown)))
    if len(set(ids)) != len(ids):
        raise SystemExit("an id is given twice")
    # One shuffled batch per pass: a rerun is only for an id whose original grade is on the ledger and invalid (or
    # empty). An id with a valid grade is never regraded, and an id with no ledger row yet must first have its part
    # output saved, so that the original grade, good or bad, is on the ledger before any rerun exists.
    rows, lprobs = T.read_ledger(inst)
    if lprobs:
        raise SystemExit("cannot read the ledger: " + "; ".join(lprobs))
    rows = T.batch_rows(rows, batch, T.sha256_file(map_path))
    valid = T.first_valid_rows(rows)
    seen = {r.get("id") for r in rows}
    has_valid = [i for i in ids if i in valid]
    unsaved = [i for i in ids if i not in seen]
    if has_valid:
        raise SystemExit("refused: %s already %s a valid grade on the ledger (a batch is graded once; only ids with no "
                         "valid grade are rerun)" % (", ".join(has_valid), "has" if len(has_valid) == 1 else "have"))
    if unsaved:
        raise SystemExit("refused: %s %s no row on the ledger for this id map; save every part output of %s first "
                         "(save_tuning_grades5.py lists the ids with no valid grade), then rerun those"
                         % (", ".join(unsaved), "has" if len(unsaved) == 1 else "have", batch))
    items = []
    for i in ids:
        m = by_id[i]
        t, err = T.packaged_text(T.answer_path(m["case"], m["arm"], m["run"], b4, b5))
        if err or T.sha256_text(t) != m["answer_sha256"]:
            raise SystemExit("the answer of %s is %s; it is no longer the answer this batch maps" % (i, err or "changed"))
        items.append({"id": i, "c": m["case"], "block": answer_block(i, t)})
    rr_path = os.path.join(inst, "maps", "%s-reruns.json" % batch)
    reruns = T.read_json(rr_path) if os.path.exists(rr_path) else []
    k = len(reruns) + 1
    script = render(batch, "rerun%d" % k, "", items, heads, schemas, grader_prompt)
    if blind_problems(script, items):
        raise SystemExit("blindness check failed")
    data = script.encode("utf-8")
    if len(data) > max_bytes:
        raise SystemExit("rerun script is %d bytes; pass fewer ids" % len(data))
    fn = os.path.join(inst, "workflows", batch, "grade-%s.rerun%d.js" % (batch, k))
    with open(fn, "wb") as f:
        f.write(data)
    reruns.append({"file": os.path.relpath(fn, inst).replace("\\", "/"), "sha256": T.sha256_bytes(data), "ids": ids,
                   "created": datetime.datetime.now().astimezone().isoformat(timespec="microseconds")})
    T.write_json(rr_path, reruns)
    print("wrote %s: %d answers, %d bytes" % (fn, len(items), len(data)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch")
    ap.add_argument("--only", help="comma-separated ids for a rerun script")
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    ap.add_argument("--base4", default=T.B4)
    ap.add_argument("--base5", default=T.B5)
    ap.add_argument("--inst", default=T.INST)
    a = ap.parse_args()
    if a.only:
        rerun(a.batch, [s.strip() for s in a.only.split(",") if s.strip()], a.inst, a.base4, a.base5, a.max_bytes)
    else:
        build(a.batch, a.inst, a.base4, a.base5, a.max_bytes, a.replace)


if __name__ == "__main__":
    main()
