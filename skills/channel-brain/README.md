# channel-brain

Post a channel URL → every video is ripped + transcribed → ingested into its own
**LLM Wiki v2** knowledge brain (OKF bundle). One command.

```bash
./channel_brain.py "https://www.youtube.com/@channel"
```

Creates `brains/<channel>-brain/` — a self-contained wiki the LLM owns:
`CLAUDE.md` (schema) · `raw/transcripts/` (immutable sources) · `sources/`
`entities/` `concepts/` `synthesis/` · `index.md` · `log.md`.

## How it works
1. **Rip + transcribe** — `yt-dlp` enumerates the channel and pulls each video's
   captions (YouTube auto-subs: free, instant). No captions → falls back to
   `whisper` on the audio. One transcript per video lands in `raw/transcripts/`.
2. **Ingest** — runs `claude -p` inside the brain, in batches, following the
   brain's `CLAUDE.md`: it summarizes each video, builds entity/concept pages,
   cross-links them, and grows a synthesis of the channel — the LLM Wiki v2 loop.

After ripping you just query the brain like any wiki: `cd brains/<x> && claude`,
then ask questions — it answers with citations and files new answers back.

## Options
```
--name NAME        brain dir name (default: derived from the channel handle)
--limit N|all      max NEW (not-yet-ingested) videos to rip (default 30; common: 1, 5, 30, all)
--jobs N           parallel caption downloads (default 6)
--whisper-jobs N   parallel whisper transcribes (default 2)
--no-whisper       captions only; never transcribe audio (fast)
--whisper-model M  whisper model for the fallback (default: base)
--no-ingest        rip + transcribe only, skip the LLM ingest
--selftest         run the vtt-parser check
```

## Parallelism — the two ceilings
Downloads and transcription bottleneck on different things, so they have separate pools:

- **Caption downloads (`--jobs`, default 6)** — network-bound, *not* machine-bound.
  A caption fetch is tiny; the limit is YouTube's rate-limiting. Past ~8 parallel
  you hit HTTP 429 and a soft IP throttle that slows the *whole* run. Sane max **~8**.
- **Whisper transcription (`--whisper-jobs`, default 2)** — CPU-bound; each whisper
  process already uses every core. On a 6-perf-core machine, **2** for `base`, **1**
  for `small`/`medium`. More just thrashes and gets slower.
- **Ingest is sequential by design** — this is the LLM Wiki v2 SOP, not a map/reduce.
  Each batch (`BATCH`, default 5 transcripts) is one `claude` agent that runs the
  brain's `CLAUDE.md` Ingest workflow end to end: write the source page, then
  create/**update** the entity/concept pages it touches, cross-link both ways, refresh
  synthesis + `index.md`, append `log.md`. Batches run one after another so each agent
  integrates into the wiki the previous one left — that's what keeps cross-video links
  complete without a staging file or a separate consolidator. Parallel ingestion would
  race on shared pages and drop links, so it's deliberately serial.

Re-running is idempotent — already-ripped videos (by video id) are skipped, and
`--limit N` counts NEW videos, so it doubles as "update the brain with new uploads"
*and* "walk deeper into the back catalog".

Deps (all on PATH): `yt-dlp`, `ffmpeg`, `whisper`, `claude`.

Not affiliated with magic-brain — each channel gets its own standalone brain.
