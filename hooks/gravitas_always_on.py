#!/usr/bin/env python3
"""PreInvocation hook: remind the agent to consider the `gravitas` skill.

This hook ONLY injects a transient reminder message into the conversation so the
skill is considered even when the user forgets to name it. It makes no permission
decisions, approves nothing, and never alters a tool call. Its entire output is a
single `ephemeralMessage`.

Contract (agy-customizations/docs/hooks.md):
  stdin  -> {"invocationNum": N, "initialNumSteps": N, ...common fields}
  stdout -> {"injectSteps": [{"ephemeralMessage": "..."}]}
"""
import json
import sys

# Re-assert at these invocation numbers. invocationNum is ZERO-indexed (verified
# empirically against the agy CLI), so 0 is the opening turn; 1 is kept in case another
# Antigravity surface numbers from 1. The later
# points counter drift on long runs without spamming context every step.
INJECT_AT = {0, 1, 20, 45}

REMINDER = (
    "[gravitas] Before proceeding, classify this task. Load the `gravitas` skill for any "
    "substantive request in any field, including mathematics, physics, law, medicine, "
    "statistics, finance, history, research, writing, design, colour, editing, and software. "
    "Load it whenever being wrong is expensive, the answer will be relied on, or the result "
    "must actually work. Then follow it: build the work list first; find the independent "
    "check that does not route through your own reasoning (evaluate it numerically, pull the "
    "primary source, run it and look at it, reconcile the totals, check the limiting case); "
    "and refuse the convenient proxy, asking whether your check could pass while the thing "
    "you care about is false. Report each claim with its evidence tier, using the words "
    "observed, executed, read, inferred, and state what was not covered. Skip the skill only "
    "for trivial edits, quick definitions and conversational questions."
)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(json.dumps({"injectSteps": []}))
        return

    try:
        n = int(payload.get("invocationNum", 0))
    except (TypeError, ValueError):
        n = 0

    if n in INJECT_AT:
        print(json.dumps({"injectSteps": [{"ephemeralMessage": REMINDER}]}))
    else:
        print(json.dumps({"injectSteps": []}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never disrupt the loop if this reminder fails.
        print(json.dumps({"injectSteps": []}))
