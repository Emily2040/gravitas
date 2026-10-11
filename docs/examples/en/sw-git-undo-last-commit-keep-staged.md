# Undoing the last Git commit

A one-line Git question. Both answers gave the right command. Only Gravitas added the one warning that matters if the commit has already been shared.

| | |
|---|---|
| Test set | Blind set: 60 everyday requests written without seeing Gravitas |
| Run | Second of two Gravitas runs on this model |
| Model | Gemini 3.8 Flash, for both answers |
| Plain Antigravity | Antigravity with Google's ten default plugins, without Gravitas |
| Gravitas | The same setup plus the previous always-on rule (v4), without the Second Opinion. The rule in Gravitas 1.0 was rebuilt after these runs |
| Graders | Gemini 3.1 Pro and Gemini 3.8 Flash, each comparing the two answers blind against an answer key written before the test |

## The request

````text
git: how do I undo my last commit but keep the changes staged?
````

## Plain Antigravity's answer

````text
To undo your last commit while keeping the changes in your staging area, run:

```bash
git reset --soft HEAD~1
```

### How it works:
* **`--soft`**: Moves `HEAD` back to the previous commit, but leaves your index (staging area) and working tree untouched. All changes from that commit will remain staged and ready to be recommitted.
* **`HEAD~1`** (or `HEAD^`): Refers to the commit immediately before the current `HEAD`.

You can verify the staged changes immediately afterward by running:
```bash
git status
```
````

## Gravitas's answer

````text
Run:

```bash
git reset --soft HEAD~1
```

This removes the commit while keeping all changes in your staging area ready to be recommitted. If you have already pushed this commit to a shared remote, rewriting that history with a force push can disrupt collaborators.
````

## How the graders voted

The answer key asked for `git reset --soft HEAD~1`, a sentence saying the changes stay staged, and a short caveat: if the commit was already pushed, undoing it rewrites shared history, which then needs a force push (preferably `--force-with-lease`), or `git revert` on a shared branch. It counted a long essay on every reset mode as wrong for a question this size.

- Gemini 3.1 Pro preferred Gravitas, by a decisive margin. Plain Antigravity left out the caveat about pushed commits and added formatting the question didn't need.
- Gemini 3.8 Flash preferred Gravitas, by a clear margin, for the same two reasons.

Across all four Gravitas runs of this question (two on each model), Gravitas got 7 of the 8 grader votes. The warning is a Flash result. On Gemini 3.8 Flash, Gravitas included it in both runs, and plain Antigravity left it out in all three of its runs on either model. On Gemini 3.1 Pro, Gravitas's answers left it out as well, and the graders gave Gravitas 3 of 4 votes there, by slight margins, for the shorter answer.

## What happened

### What plain Antigravity missed

It gave the right command and explained each part clearly. It never mentioned the one situation where this command causes trouble: when the commit has already been pushed, meaning copied to the shared repository on a server that teammates pull from. Undoing it on your own machine then leaves your copy and the shared copy disagreeing. Making the shared copy match takes a force push, which overwrites the branch on the server and can throw away work someone else pushed in the meantime.

### What Gravitas did

The same command, one sentence on what it does, and one sentence of warning: "If you have already pushed this commit to a shared remote, rewriting that history with a force push can disrupt collaborators." The whole answer is about half the length of plain Antigravity's.

### Which part of Gravitas did it

Move 3, fitting the answer to the person: a one-line answer to a one-line question. Under it sits the floor that applies to every answer: say plainly when acting on it could hurt. The line in the v4 rule:

> A question whose whole answer fits in a line or two gets that line, plus one sentence when acting on it could hurt them: something deleted, overwritten, pushed or shared, a dose, or a fact they assumed.

### Why it matters to the person asking

People ask this right after committing something they didn't mean to. If they have already pushed it, the quick fix is safe on their own machine and becomes everyone's problem once they force-push it. One sentence is enough to make them stop and think first.
