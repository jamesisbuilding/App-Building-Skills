---
name: channel-brain
description: Turn a video channel URL into its own LLM-Wiki-v2 knowledge brain. Use when the user pastes a YouTube channel/playlist URL and wants its videos ripped, transcribed, and ingested into a wiki brain — or wants to add new uploads to, or query, an existing channel brain under brains/.
---

# channel-brain

Post a channel URL → every video ripped + transcribed (YouTube captions, whisper
fallback) → ingested into its own LLM Wiki v2 brain (OKF bundle). Script does the
rip + transcribe + batched `claude -p` ingest; you drive it and answer questions.

Base dir: this skill's repo root (two levels up from `.claude/skills/channel-brain/`).
The driver is `channel_brain.py` there; brains land in `brains/<channel>-brain/`.

## Build / update a brain

Run the driver from the repo root:

```bash
python3 channel_brain.py "<CHANNEL_OR_PLAYLIST_URL>"
```

- `--limit N|all` — max videos from the channel. **Default 30.** Offer the user
  **1 / 5 / 30 / all** when they haven't said; `all` can be hundreds of videos.
- `--jobs N` — parallel caption downloads (default 6; keep ≤8).
- `--name NAME` — brain dir name (default: derived from the channel handle).
- `--no-whisper` — captions only; skip audio transcription (fast).
- `--no-ingest` — rip + transcribe only.

Re-running the SAME url is idempotent (skips already-ripped videos by id) — so it
doubles as "update this brain with new uploads". Big channels ingest 5 videos per
`claude -p` batch; warn the user a few-hundred-video channel is many batches and
confirm before kicking it off. `--limit` first if unsure it's the right channel.

The script streams progress; the ingest runs headless. When it finishes, read the
brain's `index.md` + `log.md` and report the pages produced (sources / entities /
concepts / synthesis counts).

## Query a brain

Each brain is a self-contained LLM Wiki v2 bundle with its own `CLAUDE.md`. To
answer questions about a channel, work INSIDE that brain dir and follow its
`CLAUDE.md` (read `index.md` first, drill in, cite pages, file misses back):

```bash
cd brains/<channel>-brain
```

Then run the Query workflow from that brain's schema. Don't answer from the
transcripts directly — the wiki pages are the compiled answer.

## Notes
- Deps on PATH: `yt-dlp`, `ffmpeg`, `whisper`, `claude`. `python3 channel_brain.py --selftest` checks the caption parser.
- Standalone — not magic-brain. Each channel gets its own brain.
