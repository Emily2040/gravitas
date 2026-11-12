"""Save the labelling workflow's results and check that every note and listed item is labelled.

    python save_labels.py <workflow-output-file>   -> labels-sonnet.json, labels-opus.json, listed-labels.json
"""
import json
import os
import sys

B = os.path.dirname(os.path.abspath(__file__))
out = json.load(open(sys.argv[1], encoding="utf-8"))["result"]  # {"labels": [...], "regrade": {...}}
res = out["labels"]
for r in res:  # job files are named relabel-<case>-<nn> and listed-<case>
    r.setdefault("case", r["file"].split("-", 1)[1].rsplit("-", 1)[0] if r["kind"] == "relabel" else r["file"].split("-", 1)[1])
rg = out.get("regrade") or {}
if rg.get("grade"):
    d = os.path.join(B, "blind", "grades", rg["grader"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, rg["pid"] + ".json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rg["grade"], fh, ensure_ascii=False, indent=1)
notes = json.load(open(os.path.join(B, "claim-notes.json"), encoding="utf-8"))
listed = {b["case"]: b["items"] for b in json.load(open(os.path.join(B, "listed-batches.json"), encoding="utf-8"))}
by_model = {"sonnet": {}, "opus": {}}
listed_out, problems = [], []
for r in res:
    if r.get("labels") is None:
        problems.append("%s %s %s: no result" % (r["kind"], r["case"], r.get("model", "")))
        continue
    if r["kind"] == "relabel":
        for l in r["labels"]:
            if l["id"] in by_model[r["model"]]:
                problems.append("duplicate label id %s from %s" % (l["id"], r["model"]))
            by_model[r["model"]][l["id"]] = {"id": l["id"], "label": l["label"], "cite": l["cite"]}
    else:
        items = {it["n"]: it for it in listed[r["case"]]}
        seen = set()
        for l in r["labels"]:
            it = items.get(l["n"])
            if it is None or l["n"] in seen:
                problems.append("listed %s: bad or duplicate n %s" % (r["case"], l["n"]))
                continue
            seen.add(l["n"])
            listed_out.append({"case": r["case"], "round": it["round"], "raw": it["raw"], "cls": it["cls"], "label": l["label"], "why": l["why"]})
        missing = set(items) - seen
        if missing:
            problems.append("listed %s: %d items unlabelled" % (r["case"], len(missing)))
for model, labels in by_model.items():
    missing = [n["id"] for n in notes if n["id"] not in labels]
    if missing:
        problems.append("%s: %d notes unlabelled (first ids %s)" % (model, len(missing), missing[:5]))
    with open(os.path.join(B, "labels-%s.json" % model), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(sorted(labels.values(), key=lambda x: x["id"]), fh, ensure_ascii=False, indent=1)
with open(os.path.join(B, "listed-labels.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(listed_out, fh, ensure_ascii=False, indent=1)
for p in problems:
    print(p)
print("%d notes; sonnet %d, opus %d labels; %d listed items labelled; %d problems" % (
    len(notes), len(by_model["sonnet"]), len(by_model["opus"]), len(listed_out), len(problems)))
sys.exit(1 if problems else 0)
