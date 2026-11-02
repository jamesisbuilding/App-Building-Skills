---
name: reel-script
description: Write the spoken script for a 20–60s explainer reel in the house format — a question hook, a real personal story from the presenter, and every concept explained like the viewer is five (via the eli5 skill), timed into beats ready for recording and for reel-motion-graphics. Use when the user asks for a reel script, a script for a paper or topic, or to turn notes, an article or a paper into something to record.
---

# Reel script

The script comes first: the presenter records it, the recording sets the timing, and `reel-motion-graphics` builds the animation from it. Write for the ear. It is spoken by one person to camera.

## Non-negotiable format

1. **The hook is always a question.** It is the first line, spoken in 0–3s, 12 words or fewer. It names a tension the viewer feels, e.g. "Why do AI labs throw away models that cost millions to train?". It is not a rhetorical "Did you know…?" and not a list.
2. **There is always a personal story.** A short first-person moment from the presenter's real life or work that makes the topic matter: 2–3 sentences, 5–8s, placed straight after the hook. **Never invent it.** If the user hasn't given one, ask for it before writing, and offer 2–3 prompts that fit the topic ("a time you waited on a long training run", "when a tool you relied on got replaced"). If they still have none, leave a marked `[STORY: …]` slot and say so.
3. **Every concept is explained like the viewer is five.** Load the `eli5` skill and use its Age-5 approach for each concept beat: say what it is in one sentence, give one everyday analogy (toys, kitchens, school, sport), and keep only the detail the next beat needs. Use no jargon unless it's defined in the same breath. One idea per sentence. Simplify, but never state something false: a simplification may leave detail out, never add an error.

## Structure (30s ≈ 75 spoken words at about 2.5 words/s)

| Beat | Time | Job | Maps to in reel-motion-graphics |
|---|---|---|---|
| Hook | 0–3s | The question | Title card (the hook can be a thesis line) |
| Story | 3–8s | The personal moment that makes it matter | Title card hold, or step 1 |
| Concepts | 8–24s | 2–4 ELI5 beats, one idea and one analogy each | Steps 1–4: heading + caption + diagram move |
| Payoff | 24–28s | The answer to the hook, with the one number or fact that proves it | Result scene (stat cards) |
| Close | 28–30s | One line that lands the takeaway | Closing caption |

Scale the concept count with length: 20s → 2 beats, 45–60s → 4–5 beats.

## Facts

Use only facts from the source the user provides (paper, article, notes) or that you can verify. Keep numbers exact as given. Put any claim you're unsure of in a "check before recording" list instead of the script.

## Output

Give the user the script and save it as `reels/<slug>/SCRIPT.md`. Include:
- **Each beat** labelled with its time range and word count, plus a total runtime estimate at 2.5 words/s.
- **The spoken lines,** written as said, with contractions and short sentences.
- **For each concept beat,** a suggested heading (plain + italic accent, ≤ about 22 characters) and caption (line 1 ≤ about 34 characters, line 2 ≤ about 40) for the reel.
- **Recording notes:** pause about half a second between beats (clean cut points), keep close to the words so the transcript lines up with the beats, and frame consistently with headroom.
- **The "check before recording" list,** if there is one.

Then the user records the script, and `reel-motion-graphics` takes the recording.
