---
name: cb-ingest
description: Ingest anything into a channel brain — a video URL, a channel/playlist URL, or a local document (PDF, docx/doc/rtf/odt, html, txt/md) or folder of them — via the channel-brain pipeline, then update that brain's wiki. Use when the user pastes a link or attaches/names a file and wants it added to a knowledge base. If the target brain is unclear, ask which brain under brains/ to ingest into.
---

# cb-ingest — add a URL or document to a channel brain

Transcribe a video or channel/playlist URL, or extract a local document, with the existing
pipeline and ingest it into a chosen brain under `brains/`. Thin wrapper over `channel_brain.py` — same
rip → transcribe → SOP ingest (sequential batches, each following the brain's
`CLAUDE.md` Ingest workflow), just targeted at a specific brain.

Base dir: this skill's repo root (two levels up from `.claude/skills/cb-ingest/`).
Driver: `channel_brain.py` there; brains live in `brains/<name>-brain/`.

## Steps

1. **Get the input** — a single video (`watch?v=…`), a channel/playlist, or a local path
   to a document or a folder of documents (pdf, docx, doc, rtf, odt, html, txt, md).

2. **Pick the target brain.** List `brains/*/`:
   - User named one → use it.
   - Exactly one brain and the user didn't say → confirm it's the target before running.
   - Otherwise (video URL, ambiguous, or several brains) → **ask with `AskUserQuestion`**:
     options are the existing brain dir names, plus "New brain from this URL" when the
     URL is a channel/playlist.
   - Never guess silently — the whole point is not ingesting into the wrong brain.

3. **Run the pipeline** into that brain (`--name` = the brain dir name):

   ```bash
   python3 channel_brain.py "<URL or path>" --name <brain-dir>
   ```

   - Local document/folder → text extracted verbatim into `raw/docs/<slug>-<hash>.md`
     (PDF via `pdftotext`, Office/RTF/HTML via macOS `textutil`), then ingested one doc
     per agent. `--name` is required. Same file again (same bytes) is skipped.
   - Scanned PDF with no text layer → reported as "no text"; OCR it first (not built in).
   - Author isn't the brain's subject (e.g. a companion book) → the ingest banners it
     `external-author` and keeps its claims attributed to that author.

   - Single video → one transcript. Channel/playlist → obeys `--limit` (default 30);
     for a channel confirm the count first (offer 1 / 5 / 30 / all).
   - Idempotent: already-ripped videos (by id) are skipped, so re-ingesting is safe.
   - Re-passing a channel already partly done continues with the NEXT not-yet-ingested
     videos — `--limit N` counts NEW videos, so repeat runs walk deeper into the back
     catalog (e.g. run `--limit 30` again to grab the next 30 you don't have yet).
   - The brain's own `CLAUDE.md` is preserved — only written for a brand-new brain.
   - New brain from a channel URL: omit `--name` to let it derive from the handle
     (this is what the `channel-brain` skill does).

4. **Report.** When it finishes, read the brain's `index.md` + `log.md` and summarise
   what was added (new sources / entities / concepts / synthesis).

## Notes
- Deps on PATH: `yt-dlp`, `ffmpeg`, `whisper`, `claude`; for docs `pdftotext` (poppler).
- No captions on a video → whisper fallback transcribes the audio (slower).
- To query the brain afterwards, use the `channel-brain` skill's Query flow.
