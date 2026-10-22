"""Unblind round-two grades and measure length and hedging (criteria.md, frozen before the runs)."""
import glob, json, os, re, statistics as st
B = os.path.dirname(os.path.abspath(__file__))
H = ["可能","大概","也许","或许","以.{0,12}为准","建议.{0,6}核实","建议.{0,6}确认","不确定","请咨询","仅供参考",
     r"\bmay\b",r"\bmight\b",r"\bprobably\b",r"\bcheck with\b",r"\bconfirm with\b",r"\bnot sure\b",r"\bverify\b"]
def hedges(t): return sum(len(re.findall(p, t, flags=re.I)) for p in H)
def load(p):
    t = open(p, encoding="utf-8").read(); return json.loads(t[t.find("["):t.rfind("]")+1])
def tally(mapfile, gradefiles, sides, label):
    m = json.load(open(mapfile)); votes = {s: 0 for s in sides}; votes["tie"] = 0
    rows = []; errs = {s: 0 for s in sides}; scores = {s: [] for s in sides}
    for gf in gradefiles:
        g = os.path.basename(gf).split("-")[1].split(".")[0]
        for r in load(gf):
            pid = r["pair"]; w = r["winner"]
            win = "tie" if w == "tie" else m[pid][w]
            votes[win] += 1
            for lab in "AB":
                s = m[pid][lab]; errs[s] += len(r[lab].get("added_claim_errors") or [])
                scores[s].append(sum(v for k, v in r[lab].items() if k in ("correct","trap","honest","useful","concise") and isinstance(v,(int,float))))
            rows.append((pid, g, win, r["margin"]))
    print("==", label); print(" votes", votes); print(" added-claim errors listed", errs)
    print(" mean score /50", {s: round(st.mean(v), 2) for s, v in scores.items()})
    return rows
rows = tally(os.path.join(B,"blind-map.json"), sorted(glob.glob(os.path.join(B,"blind","grades-*-r?.json"))), ["gv-plain","gv-grav"], "held-out (20 pairs x 2 graders)")
bycase = {}
for pid, g, win, mar in rows:
    bycase.setdefault(pid.rsplit(".",1)[0], []).append("%s:%s/%s(%s)" % (pid.rsplit(".",1)[1], g, win.replace("gv-",""), mar))
for c in sorted(bycase): print("  ", c, " ".join(sorted(bycase[c])))
rrows = tally(os.path.join(B,"regress","blind-map.json"), sorted(glob.glob(os.path.join(B,"regress","blind","grades-*.json"))), ["plain-round1","grav-branch"], "regression (12 pairs x 2 graders)")
bycase = {}
for pid, g, win, mar in rrows:
    bycase.setdefault(pid.rsplit(".",1)[0], []).append("%s:%s/%s(%s)" % (pid.rsplit(".",1)[1], g, win.replace("-round1","").replace("-branch",""), mar))
for c in sorted(bycase): print("  ", c, " ".join(sorted(bycase[c])))
print("== length and hedging, held-out")
res = {}
for side in ("gv-plain","gv-grav"):
    L = []; R = []
    for f in sorted(glob.glob(os.path.join(B,"raw","*.%s.r?.txt" % side))):
        t = open(f, encoding="utf-8").read(); L.append(len(t)); R.append(hedges(t)*1000/len(t))
    res[side] = (st.median(L), st.mean(R)); print(" ", side, "median chars", st.median(L), "hedge/1000", round(st.mean(R),2))
lr = res["gv-grav"][0]/res["gv-plain"][0]; hr = res["gv-grav"][1]/res["gv-plain"][1]
print("  ratio chars %.2f (limit 1.24) -> %s; ratio hedges %.2f (limit 1.35) -> %s" % (lr, "REGRESSION" if lr>1.24 else "ok", hr, "REGRESSION" if hr>1.35 else "ok"))
L = [len(open(f,encoding="utf-8").read()) for f in glob.glob(os.path.join(B,"regress","raw","*.txt"))]
R1 = [len(open(f,encoding="utf-8").read()) for f in glob.glob(os.path.join(B,"..","gravitas-dsh-ab","raw","*.gv-grav.r1.txt"))]
print("== regression lengths: branch median", st.median(L), "round-one Gravitas median", st.median(R1))
