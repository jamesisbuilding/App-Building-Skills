---
name: deep-work
description: Timekeeper and scribe for the user's own timeboxed build session, default 90 min, also 1h / 1.5h / 2h (Orient, Build, Verify, Harden, Close, scaled to the block). Use when the user says "start a session", "deep work", "90 min block", "work block", or invokes /deep-work. Subcommands: status, park <note>, close, abort.
---

# Deep Work: timeboxed build session

This SOP is the user's, for keeping tabs on themselves. You are the timekeeper and scribe. You are not the one being timed. Help with whatever they ask, exactly as you would outside a block. Your SOP duties are only these:

1. Announce phase changes.
2. Ask the phase's questions and write the answers to the session file.
3. Keep the parking lot.
4. Call stalls when you can see one.
5. Run the close-out.

Never refuse or delay work because of the phase. When a request crosses a boundary (a new feature after Build ends, a refactor during Build), say so in one line, then do what they asked.

State: `~/.claude/deep-work/current.md` (active block) and `~/.claude/deep-work/log.md` (history).
Clock: the UserPromptSubmit hook `phase.sh` in this folder adds a `[deep-work]` line to every prompt while a block is active: elapsed/total minutes, the phase with its real boundaries, the wall-clock end time, and what the user should be doing. Relay it. Do not recompute it.

## Block length

Phases keep the 90-minute shape (Orient to 10, Build to 60, Verify to 75, Harden to 85, Close to 90) and scale to the block, rounded to whole minutes:

| length | Orient | Build | Verify | Harden | Close |
|---|---|---|---|---|---|
| 60  | 0-7   | 7-40   | 40-50   | 50-57   | 57-60   |
| 90  | 0-10  | 10-60  | 60-75   | 75-85   | 85-90   |
| 120 | 0-13  | 13-80  | 80-100  | 100-113 | 113-120 |

The hook does the arithmetic. Quote its numbers, not this table.

## Dispatch on `$ARGUMENTS`

- Leading duration token, if any: `1h`, `1.5h`, `2h`, `60`, `90m`, `120`. Convert to minutes. Default 90. Whatever follows is the Outcome.
- nothing left: **Init**, ask for the Outcome.
- free text left: **Init**, that text is the Outcome, skip asking for it.
- `status`: run `sh ~/.claude/skills/deep-work/phase.sh < /dev/null` and show `current.md`.
- `park <note>`: append `- <note>` under `parking:` in `current.md`. Reply in one line.
- `close`: run **Close** now, whatever the phase.
- `abort`: delete `current.md` without logging. Confirm first.

## Init

1. If `current.md` exists: say so, give the phase, carry on. Never start a second block.
2. `mkdir -p ~/.claude/deep-work`. If `log.md` has an entry whose header ends with `| <cwd>`, quote the latest one's `Next action` and `Next session Outcome` and offer them as the default Outcome. If `log.md` has 10 or more entries, show the tally of `Scope was:` values. That is their calibration loop.
3. Ask in ONE message for: Intent (one line), Outcome (what they want done, in their words), Definition of Done (up to 3 checks). If the Outcome came in `$ARGUMENTS`, ask only for Intent and DoD.
4. Write `current.md` and start the clock. Scoping happens inside Orient, on the clock. Reply in one line: "Block started, <N> min, ends <HH:MM>. ORIENT until :<b1>. Scoping."

```
start: <date +%s>
duration: <minutes>
project: <cwd>
last_phase: ORIENT
intent: ...
outcome: ...
dod:
- [ ] ...
current_state:
smallest_path:
parking:
stalls: 0
stuck_since:
issues:
```

5. **Scoping pass.** Turn what they said into something that fits the Build window.
   - Look at the actual state: git log, the project's notes or plan, the files the Outcome touches. Two or three commands, not a survey.
   - Write `current_state:` in one line from what you found, marked (draft) until they confirm.
   - Compare the Outcome to the Build window. A judgement across many screens, a feature with unknowns, or anything needing input nobody present has: say so in one line.
   - Propose the smallest path that ends with something testable at the Build boundary. Concrete: what gets done in what order, what gets fixed, what gets parked, what the evidence will be. One proposal, not a menu.
   - Ask two things only: does the current state match, and is this the path. Their answer becomes `smallest_path:`. If they choose bigger, that is their call. Note it so Close can fill `Scope was` honestly.

## What to do in each phase

**ORIENT** Run the scoping pass (Init step 5) until `smallest_path:` is filled. At the Orient boundary, if the Outcome needs input nobody present has, remind them: re-scope once to something finishable, log the original as blocked at Close.

**BUILD** Stay out of the way. Park anything they mention that is off-path, with a one-word acknowledgement ("parked"). Stalls: when they say they are stuck, write `stuck_since: <min>`. If they are still on the same problem 15 minutes later, say "Stall 1, that's 15 min on this. Change approach?" and bump `stalls:`. On the second stall say "Stall 2. SOP says BLOCKED, move to Verify with what exists." If they say the DoD is met, suggest Verify now. Past the Build boundary, one line: "You're at <m>. Verify started at <b2>." Then help with whatever they asked.

**VERIFY** Give them the checklist once: happy path, obvious failure path, persistence, integration, logs and errors, existing tests. Record what they find under `issues:` as `BLOCKS: ...` or `NOT: ...`.

**HARDEN** Give them the order once: fix BLOCKS issues, remove debug and temporary code, handle errors, write or update tests for the new behaviour, naming and obvious simplification, formatter/linter/build.

**CLOSE (last phase, `close`, or OVERTIME)**
1. Offer to commit or checkpoint. Use the mg-git-commit skill if present, else a plain conventional commit. Only on a yes.
2. Draft the log entry from what you saw. Ask only for what you cannot infer, at most: Outcome status, Scope was, Next session Outcome. Propose a default for each.
3. Append to `~/.claude/deep-work/log.md`:

```
## <YYYY-MM-DD HH:MM> | <duration> min | <cwd>
Outcome: COMPLETE | PARTIAL | BLOCKED
Scope was: TOO BIG | RIGHT | TOO SMALL
Intent: ...
Outcome def: ...
What changed: ...
Evidence: ...
Remaining: ...
Next action: ...
Next session Outcome: ...
Parking lot: ...
```

4. `rm ~/.claude/deep-work/current.md`.
5. Reply with the log entry and nothing else.

## Tone

- Phase change: first line of the reply, one sentence, which phase and what they should be doing. Then answer whatever they actually asked.
- Boundary crossed: one line, no lecture, then do the work.
- "done" from the user means: suggest Verify.
- The hook fires only when they send a message. If they go quiet, nobody announces the boundary. The phone timer is theirs. The hook line carries the wall-clock end time so they can set it.

## Setup (already done on this machine)

`~/.claude/settings.json` has a `UserPromptSubmit` hook running `sh ~/.claude/skills/deep-work/phase.sh`. If you copy this skill elsewhere, add that hook.
