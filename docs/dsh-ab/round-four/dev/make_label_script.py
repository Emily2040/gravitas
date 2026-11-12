"""Write workflows/label4.js with relabel-batches.json embedded, for the Workflow tool, which takes args only inline.

The only changes to label4.js: one line after the meta block, `const EMBEDDED = <relabel-batches.json>;`, and
`args.batches` read as `EMBEDDED.batches`. Every prompt the agents get is label4.js's own text for those batches.
    python make_label_script.py OUT.js [START END]   (a slice of the batches, to stay under the 512 KB script limit)
"""
import json
import os
import sys

B = r"W:\AgentData\logs\gravitas-dsh-ab4"
src = open(os.path.join(B, "workflows", "label4.js"), encoding="utf-8").read().replace("\r\n", "\n")
batches = json.load(open(os.path.join(B, "relabel-batches.json"), encoding="utf-8"))
if len(sys.argv) > 3:
    batches = batches[int(sys.argv[2]):int(sys.argv[3])]
end = src.index("\n}\n") + 3  # end of the meta literal
assert src[:end].startswith("export const meta = {") and src.count("args.batches") == 1
body = src[end:].replace("args.batches", "EMBEDDED.batches")
out = src[:end] + "const EMBEDDED = " + json.dumps({"batches": batches}, ensure_ascii=False) + ";\n" + body
open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(out)
print("wrote %s: %d batches, %d notes, %d bytes" % (sys.argv[1], len(batches), sum(len(b["notes"]) for b in batches), len(out.encode("utf-8"))))
