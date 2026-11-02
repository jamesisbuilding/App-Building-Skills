---
name: reel-study
description: Rip short videos (Instagram reels, TikToks, YouTube Shorts) into format study cards — spoken transcript + caption + sampled keyframes laid into a hook/story/visuals template — so a persona (or the user) can reverse-engineer what makes them work. Use when someone wants to study a creator's format, break down a reel, or build a swipe file of what stops the scroll. The tool does the grunt; naming the pattern is the human's rep.
---

# reel-study — reverse-engineer a reel's format

Thin wrapper over `reel.py` at the repo root (reuses the yt-dlp + whisper pipeline).
It downloads a short video, transcribes the speech, grabs keyframes, and writes a
`study-card.md` with the **hook / story / visuals** template — the spoken parts filled
in, the judgment blanks left for a human.

**The split is the point:** the tool automates the grunt (download, transcribe, frames).
It does NOT name the hook type, read the visuals, or find the pattern — that's the rep
that actually teaches. Don't auto-conclude the format; coach the person to it.

## Rip cards

```bash
python3 reel.py <url> [<url> …]              # one study-card per reel
python3 reel.py <url> --frames 6            # more sampled keyframes
python3 reel.py <url> --cookies cookies.txt  # Instagram reels usually need login cookies
```

Output per reel: `study/<creator>/<id>/study-card.md` (the 3-field decomposition) +
`transcript.txt` (verbatim) + `frame-NN.jpg`. It also appends a row to
`study/<creator>/swipe-file.md` — the **cross-reel comparison table** (one row per reel,
columns Hook / Story / Visuals) you read *down* to find the repeating pattern.

Instagram often blocks anonymous downloads — if yt-dlp returns no video, ask the user for
a `cookies.txt` export (or a `--cookies-from-browser` equivalent) and retry.

## Then help fill it in

1. Read the `study-card.md` and **view the `frame-NN.jpg` images** (Read each one) — that's
   how you read the on-screen text, camera angle, cut pace, and visual hook the transcript can't show.
2. Fill the blanks WITH the person, not for them: hook type, the one idea, the arc, the visual tricks.
3. Once they have several cards (aim for the 3×3 = 9), guide them to spot **what repeats** across
   the hooks / stories / visuals. That repeating skeleton is their starter format.

## Notes
- Works for any short-video URL yt-dlp supports (reels, TikTok, Shorts), not just Instagram.
- Deps on PATH: `yt-dlp`, `ffmpeg` (+ `ffprobe`), `whisper`. `python3 reel.py --selftest` checks the frame-timing math.
- Reusable by any persona under `team/` — spawn the persona, rip the cards, feed the persona the card + frames to coach the breakdown.
