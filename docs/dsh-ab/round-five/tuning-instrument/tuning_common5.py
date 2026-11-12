"""Shared pieces of the round-five tuning instrument (standard library only).

Used by make_tuning_grade_script.py, save_tuning_grades5.py and tuning_check5.py. Nothing here decides anything:
it holds the paths, the frozen constants (cases, arms, batches and their shuffle seeds), the readers, the grade
validator and the importer for round four's verdict scripts.
"""
import sys

sys.dont_write_bytecode = True   # importing round four's scripts must leave no __pycache__ in their folder

import hashlib
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
B4 = r"W:\AgentData\logs\gravitas-dsh-ab4"          # round four: prompts, keys, key points, baseline answers
B5 = r"W:\AgentData\logs\gravitas-dsh-ab5"          # round five: the c5 tuning answers land in tuning\
INST = HERE                                          # this folder: W:\AgentData\logs\gravitas-dsh-ab5\tuning-instrument

RULE_FILE = os.path.join(B5, "design", "tuning-decision-rule.md")
RULE_SHA256 = "6da489caa8e452928dfb99139a1646e570eb9b0d4e914f8c4d148e0965436922"   # as read on 2026-10-26
VERDICT_AMENDED = "verdict4-amended.py"
VERDICT_AMENDED_SHA256 = "5cf3316b8fbb55b50688ca94f2fc2840f339b4b66f50981aa6078959fc715c14"
VERDICT_FROZEN_SHA256 = "11cdd365b88df9e20a38ad2514ba50a1e3baac6feea796c1f3220429826792ca"   # verdict4.py

PROMPT_FILE = "tuning-grader-prompt5.md"
SCHEMA_FILE = "tuning-grade-schema5.json"
LKP_FILE = "lkp.json"
PREMISE_FILE = "premise-points.json"
LEDGER_FILE = "ledger5.jsonl"

LANGS = ("zh", "en", "ja", "ko")
# The rule's short names and round four's case names (prompts\, keys\, keypoints\, raw\).
SHORT = {
    "en-529": "en-529-roth", "en-fsa": "en-fsa-rollover", "en-medicare": "en-medicare-part-b",
    "ja-medical": "ja-medical-deduction", "ja-part": "ja-part-time-leave", "ja-wallpaper": "ja-wallpaper-restoration",
    "ko-jeonse": "ko-jeonse-protection", "ko-severance": "ko-severance-pay", "ko-unemployment": "ko-unemployment-quit",
    "zh-flex": "zh-flex-hours", "zh-insurance": "zh-insurance-gap", "zh-sick": "zh-sick-pay",
}
CASES = sorted(SHORT.values())
PLAIN, BASE, C5 = "gv-plain", "gv-grav-base", "gv-grav-c5"
RUNS = ("r1", "r2")
BASELINE_GROUPS = ((BASE, "r1"), (BASE, "r2"), (PLAIN, "r1"), (PLAIN, "r2"))
KP_MARKS = ("correct", "vague", "missing", "wrong")
LKP_MARKS = ("KEPT", "FLAT", "WRONG", "ABSENT")
LIST_FIELDS = ("AW", "AU", "S", "SP", "SR")
PLACEHOLDER = "(no answer: the run produced no final text)"

# Batches: (first id number - 1, shuffle seed). Written down before any batch is built; ids are t001-t048 for the
# calibration, t101-t160 for pass 1, t201-t260 for pass 2, t301-/t401- for a recalibration after a rubric fix.
BATCHES = {
    "calibration": (0, 505001),
    "pass1": (100, 505011),
    "pass2": (200, 505021),
    "calibration2": (300, 505002),
    "calibration3": (400, 505003),
}


def lang_of(case):
    p = case.split("-", 1)[0] if isinstance(case, str) else None
    return p if p in LANGS else None


def batch_pass(batch):
    """1 or 2 for pass batches, None for calibration batches."""
    return {"pass1": 1, "pass2": 2}.get(batch)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(t):
    return sha256_bytes(t.encode("utf-8"))


def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return sha256_bytes(f.read())
    except OSError:
        return None


def read_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def move_aside(path, tag="superseded"):
    """Never delete: move an existing file to <name>.<tag>-<k><ext>. Returns the new path or None."""
    if not os.path.exists(path):
        return None
    root, ext = os.path.splitext(path)
    k = 1
    while os.path.exists("%s.%s-%d%s" % (root, tag, k, ext)):
        k += 1
    new = "%s.%s-%d%s" % (root, tag, k, ext)
    os.replace(path, new)
    return new


def answer_path(case, arm, run, b4=B4, b5=B5):
    if arm == C5:
        return os.path.join(b5, "tuning", "%s.%s.%s.txt" % (case, arm, run))
    return os.path.join(b4, "raw", "%s.%s.%s.txt" % (case, arm, run))


def stream_path(case, arm, run, b4=B4, b5=B5):
    return answer_path(case, arm, run, b4, b5)[:-4] + ".ndjson"


def packaged_text(path):
    """The answer as the grader gets it: the final read as UTF-8 and stripped. Returns (text, None) or (None, reason);
    a blank final is refused (a blank run is invalid and is rerun before grading)."""
    if not os.path.isfile(path):
        return None, "missing"
    try:
        with open(path, encoding="utf-8-sig") as f:
            t = f.read().strip()
    except (OSError, UnicodeDecodeError) as e:
        return None, "unreadable (%s)" % e.__class__.__name__
    if not t:
        return None, "blank"
    return t, None


def load_keypoints(case, b4=B4):
    """Round four's keypoints\\<case>.json: [{"id": "1", "point": "..."}]. Returns (list, None) or (None, reason)."""
    p = os.path.join(b4, "keypoints", case + ".json")
    try:
        kp = read_json(p)
    except (OSError, ValueError) as e:
        return None, "%s unreadable (%s)" % (p, e.__class__.__name__)
    if not isinstance(kp, list) or not kp:
        return None, "%s is not a non-empty list" % p
    ids = []
    for x in kp:
        if not (isinstance(x, dict) and isinstance(x.get("id"), str) and isinstance(x.get("point"), str)):
            return None, "%s has a malformed entry" % p
        ids.append(x["id"])
    if len(set(ids)) != len(ids):
        return None, "%s repeats an id" % p
    return kp, None


def load_case_lists(inst=INST, b4=B4):
    """(info, problems): info[case] = {"kp": [ids], "lkp": [ids], "premise": [ids], "reported": [ids],
    "pc_points": [ids]} from keypoints, lkp.json and premise-points.json, each checked against the others.
    "premise" is the gated PC point (key point 1); "reported" are the other premise corrections, marked by the grader
    and reported, never gated; "pc_points" is both, the ids the grader's PC_points must hold."""
    problems, info = [], {}
    try:
        lkp = read_json(os.path.join(inst, LKP_FILE))["lkp"]
        pfile = read_json(os.path.join(inst, PREMISE_FILE))
        prem = pfile["premise"]
        rep = pfile.get("reported", {})
        if not isinstance(rep, dict):
            raise TypeError("reported is not an object")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return None, ["lkp.json or premise-points.json unreadable (%s)" % e.__class__.__name__]
    total = 0
    for c in CASES:
        kp, err = load_keypoints(c, b4)
        if err:
            problems.append(err)
            continue
        ids = [x["id"] for x in kp]
        l, p = lkp.get(c), prem.get(c)
        if not (isinstance(l, list) and l and all(i in ids for i in l) and len(set(l)) == len(l)):
            problems.append("lkp.json entry for %s missing or names an id that is not a key point" % c)
            continue
        if not (isinstance(p, list) and p and all(i in ids for i in p) and len(set(p)) == len(p)):
            problems.append("premise-points.json entry for %s missing or names an id that is not a key point" % c)
            continue
        r = rep.get(c, [])
        if not (isinstance(r, list) and all(i in ids for i in r) and len(set(r)) == len(r) and not set(r) & set(p)):
            problems.append("premise-points.json 'reported' entry for %s names an id that is not a key point, repeats "
                            "one, or repeats a gated premise id" % c)
            continue
        total += len(l)
        info[c] = {"kp": ids, "lkp": list(l), "premise": list(p), "reported": list(r), "pc_points": list(p) + list(r),
                   "points": kp}
    if not problems and total != 42:
        problems.append("lkp.json lists %d limited key points, not the rule's 42" % total)
    extra = sorted(set(lkp) - set(CASES))
    if extra:
        problems.append("lkp.json names unknown cases: %s" % ", ".join(extra))
    extra = sorted((set(prem) | set(rep)) - set(CASES))
    if extra:
        problems.append("premise-points.json names unknown cases: %s" % ", ".join(extra))
    return (None, problems) if problems else (info, [])


# ------------------------------------------------------------------------------------------- the grading ledger

def read_ledger(inst=INST):
    """(rows, problems): ledger5.jsonl in file order (each row gets "_line"). No ledger file means no rows. A line
    that is not a JSON object is a problem, never skipped silently."""
    p = os.path.join(inst, LEDGER_FILE)
    if not os.path.exists(p):
        return [], []
    rows, problems = [], []
    try:
        with open(p, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except (OSError, UnicodeDecodeError) as e:
        return [], ["%s unreadable (%s)" % (p, e.__class__.__name__)]
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except ValueError:
            problems.append("%s line %d is not JSON" % (LEDGER_FILE, n))
            continue
        if not isinstance(r, dict):
            problems.append("%s line %d is not an object" % (LEDGER_FILE, n))
            continue
        r["_line"] = n
        rows.append(r)
    return rows, problems


def batch_rows(rows, batch, idmap_sha256):
    """The ledger rows of one batch as built from one id map (its sha256), in ledger order."""
    return [r for r in rows if r.get("batch") == batch and r.get("idmap_sha256") == idmap_sha256]


def first_valid_rows(rows):
    """{id: the earliest row with valid true} over rows already filtered to one batch and id map. This is the grade a
    batch uses for each id: the order output files are given in never matters."""
    out = {}
    for r in rows:
        if r.get("valid") is True and isinstance(r.get("id"), str) and r["id"] not in out:
            out[r["id"]] = r
    return out


def iso_epoch(s):
    """An ISO 8601 time with offset (as now() writes it) as epoch seconds, or None."""
    import datetime
    try:
        t = datetime.datetime.fromisoformat(s)
    except (TypeError, ValueError):
        return None
    if t.tzinfo is None:
        return None
    return t.timestamp()


# ------------------------------------------------------------------------------------------- schema and validation

def schema_for_case(base, kp_ids, lkp_ids, premise_ids):
    """The frozen schema with this case's ids made required (and no others allowed). premise_ids is every id the
    grader marks in PC_points: the gated point and the reported ones (info[case]["pc_points"])."""
    s = json.loads(json.dumps(base))
    s.pop("$schema", None)
    s.pop("title", None)
    s.pop("description", None)
    props = s["properties"]

    def fixed(ids, value_schema):
        return {"type": "object", "properties": {i: json.loads(json.dumps(value_schema)) for i in ids},
                "required": list(ids), "additionalProperties": False}

    props["key_points"] = fixed(kp_ids, props["key_points"]["additionalProperties"])
    props["lkp"] = fixed(lkp_ids, props["lkp"]["additionalProperties"])
    props["lkp_quotes"] = fixed(lkp_ids, props["lkp_quotes"]["additionalProperties"])
    props["PC_points"] = fixed(premise_ids, props["PC_points"]["additionalProperties"])
    return s


def schema_errors(value, schema, path="grade"):
    """A small validator for the JSON Schema subset the instrument uses: type (object, array, string, integer,
    boolean), properties, required, additionalProperties (false or a schema), items, enum, minLength."""
    errs = []
    t = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "boolean": bool}
    if t == "integer":
        if not (isinstance(value, int) and not isinstance(value, bool)):
            return ["%s is not an integer" % path]
    elif t in types:
        if not isinstance(value, types[t]):
            return ["%s is not a %s" % (path, t)]
    if "enum" in schema and value not in schema["enum"]:
        errs.append("%s = %r is not one of %s" % (path, value, "/".join(map(str, schema["enum"]))))
    if t == "string" and isinstance(schema.get("minLength"), int) and len(value) < schema["minLength"]:
        errs.append("%s is shorter than %d characters" % (path, schema["minLength"]))
    if t == "object":
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in value:
                errs.append("%s has no %r" % (path, k))
        ap = schema.get("additionalProperties", True)
        for k, v in value.items():
            if k in props:
                errs += schema_errors(v, props[k], "%s.%s" % (path, k))
            elif ap is False:
                errs.append("%s has an unexpected key %r" % (path, k))
            elif isinstance(ap, dict):
                errs += schema_errors(v, ap, "%s.%s" % (path, k))
    if t == "array" and isinstance(schema.get("items"), dict):
        for i, v in enumerate(value):
            errs += schema_errors(v, schema["items"], "%s[%d]" % (path, i))
    return errs


def norm_quote(s):
    s = re.sub(r"\*\*|__|`|\|", " ", s)
    s = s.replace("\u3000", " ")
    return re.sub(r"\s+", "", s)


def validate_grade(grade, case_schema, expected_id, answer=None, pc_ids=None):
    """(problems, warnings) for one grade object. Problems make the grade invalid; warnings are reported.
    pc_ids: the gated premise ids (info[case]["premise"]); PC must be yes exactly when each of them is yes in
    PC_points. Without it every PC_points entry is treated as gated (the stricter check)."""
    if not isinstance(grade, dict):
        return ["the grade is not a JSON object (%s)" % type(grade).__name__], []
    problems = schema_errors(grade, case_schema)
    warnings = []
    if problems:
        return problems, warnings
    if grade["id"] != expected_id:
        problems.append("grade.id is %r, not %r" % (grade["id"], expected_id))
    pts = grade["PC_points"]
    gated = list(pts) if pc_ids is None else list(pc_ids)
    absent = [i for i in gated if i not in pts]
    if absent or not gated:
        problems.append("PC_points has no mark for the gated premise id(s) %s" % (", ".join(absent) or "(none given)"))
    all_yes = bool(gated) and all(pts.get(i) == "yes" for i in gated)
    if (grade["PC"] == "yes") != all_yes:
        problems.append("PC is %r but the gated premise point(s) %s are %s (PC must be yes exactly when the gated "
                        "premise point is yes)" % (grade["PC"], ", ".join(gated),
                                                   ", ".join(str(pts.get(i)) for i in gated)))
    for i, mark in grade["lkp"].items():
        kpm = grade["key_points"].get(i)
        if (mark == "ABSENT") != (kpm == "missing"):
            problems.append("LKP %s is %s but key point %s is %s (ABSENT exactly when the key point is missing)"
                            % (i, mark, i, kpm))
        if mark != "ABSENT" and not grade["lkp_quotes"][i].strip():
            warnings.append("LKP %s is %s with an empty quote" % (i, mark))
    if grade["PC"] == "yes" and not grade["PC_quote"].strip():
        warnings.append("PC is yes with an empty PC_quote")
    if answer is not None:
        na = norm_quote(answer)
        quotes = [("lkp_quotes." + i, q) for i, q in grade["lkp_quotes"].items() if q.strip()]
        quotes += [("PC_quote", grade["PC_quote"])] if grade["PC_quote"].strip() else []
        for f in LIST_FIELDS:
            quotes += [("%s[%d]" % (f, n), it["quote"]) for n, it in enumerate(grade[f])]
        for where, q in quotes:
            nq = norm_quote(q)
            if nq and nq not in na:
                # quotes may join pieces with an ellipsis; accept when every piece is in the answer
                pieces = [norm_quote(x) for x in re.split(r"\.\.\.|…|⋯", q)]
                if not all(p in na for p in pieces if p):
                    warnings.append("%s is not found verbatim in the answer: %s" % (where, q[:80]))
    return problems, warnings


def read_outputs(path):
    """A Workflow output file: the returned list itself, or an object whose "result" (or "output") is that list."""
    data = read_json(path)
    if isinstance(data, dict):
        for k in ("result", "output", "rows"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
    if not isinstance(data, list):
        raise ValueError("no list of rows in %s" % path)
    return data


# ------------------------------------------------------------------------------------------- round four's scripts

_VERDICT = {}


def load_verdict(b4=B4):
    """Return (module, None) for verdict4-amended.py (which loads verdict4.py itself, after checking its sha256), or
    (None, reason). The file is imported unchanged and only after its sha256 matches the one recorded here."""
    if b4 in _VERDICT:
        return _VERDICT[b4]
    p = os.path.join(b4, VERDICT_AMENDED)
    sha = sha256_file(p)
    if sha is None:
        out = (None, "%s missing" % p)
    elif sha != VERDICT_AMENDED_SHA256:
        out = (None, "%s has sha256 %s, not the %s this instrument was built against" % (p, sha, VERDICT_AMENDED_SHA256))
    else:
        try:
            spec = importlib.util.spec_from_file_location("verdict4_amended_for_tuning5", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if mod.V4 is None:
                out = (None, "verdict4-amended.py could not load verdict4.py: %s" % mod.V4_ERR)
            elif mod.V4_SHA != VERDICT_FROZEN_SHA256:
                out = (None, "verdict4.py sha256 %s is not the frozen one" % mod.V4_SHA)
            else:
                out = (mod, None)
        except Exception as e:   # an import failure gives no metric, never a pass
            out = (None, "verdict4-amended.py failed to load (%s: %s)" % (type(e).__name__, e))
    _VERDICT[b4] = out
    return out
