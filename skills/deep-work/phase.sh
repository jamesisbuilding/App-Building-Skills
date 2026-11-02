#!/bin/sh
# deep-work: UserPromptSubmit hook. Tells Claude the elapsed time, phase, and
# what the USER should be doing, while ~/.claude/deep-work/current.md exists.
# Claude is the timekeeper, not the one being timed. Silent when no block is active.
f="$HOME/.claude/deep-work/current.md"
[ -f "$f" ] || exit 0
start=$(sed -n 's/^start: *//p' "$f" | head -1)
case "$start" in ''|*[!0-9]*) exit 0 ;; esac
D=$(sed -n 's/^duration: *//p' "$f" | head -1)
case "$D" in ''|*[!0-9]*) D=90 ;; esac
m=$(( ($(date +%s) - start) / 60 ))

# phase boundaries scale from the 90-min shape 10/60/75/85/90, rounded
b1=$(( (D*10 + 45) / 90 )); b2=$(( (D*60 + 45) / 90 )); b3=$(( (D*75 + 45) / 90 )); b4=$(( (D*85 + 45) / 90 ))
end=$(date -r $((start + D*60)) +%H:%M 2>/dev/null)  # ponytail: BSD date; use -d @ on Linux

if   [ "$m" -lt "$b1" ]; then p=ORIENT;   w="0-$b1";    r="user should be: reading the ticket/spec, inspecting only the code it touches, writing current state in one line, picking the smallest path. If current_state is empty in the session file, ask for it."
elif [ "$m" -lt "$b2" ]; then p=BUILD;    w="$b1-$b2";  r="user should be: building the smallest complete version toward the Outcome and parking everything else. Stuck 15 min = call Stall, suggest a change of approach. Second stall = BLOCKED, suggest Verify. DoD met = suggest Verify. Past $b2 = flag once, then help."
elif [ "$m" -lt "$b3" ]; then p=VERIFY;   w="$b2-$b3";  r="user should be: testing actual behaviour, not writing features. Happy path, failure path, persistence, integration, logs, existing tests. Record issues as BLOCKS or NOT."
elif [ "$m" -lt "$b4" ]; then p=HARDEN;   w="$b3-$b4";  r="user should be: hardening only what they built, in order: fix BLOCKS, remove debug code, handle errors, tests for new behaviour, naming, lint/build."
elif [ "$m" -lt "$D" ];  then p=CLOSE;    w="$b4-$D";   r="run the close-out: offer commit, draft the log entry, append to log.md, delete current.md."
else                          p=OVERTIME; w="past $D";  r="the block is over. Run the close-out now. PARTIAL or BLOCKED is fine; honesty matters more than the label."
fi

# a different project's session: remind, don't drive
proj=$(sed -n 's/^project: *//p' "$f" | head -1)
[ -t 0 ] || cwd=$(jq -r '.cwd // empty' 2>/dev/null)
if [ -n "$cwd" ] && [ -n "$proj" ] && [ "$cwd" != "$proj" ]; then
  echo "[deep-work] a block is active in $proj (${m}/${D} min, $p). This session is outside it."
  exit 0
fi

last=$(sed -n 's/^last_phase: *//p' "$f" | head -1)
if [ "$last" != "$p" ]; then
  if grep -q '^last_phase:' "$f"; then sed -i '' "s/^last_phase: .*/last_phase: $p/" "$f"; else echo "last_phase: $p" >> "$f"; fi
  echo "[deep-work] PHASE CHANGE: $p ($w). Tell the user in one line, first, then answer them."
fi
echo "[deep-work] ${m}/${D} min | phase: $p ($w) | block ends $end | $r | session file: $f"
