#!/usr/bin/env python3
"""
channel_brain — post a channel URL, rip + transcribe every video, ingest into
its own LLM-Wiki-v2 knowledge brain.

Pipeline:
  1. scaffold a fresh OKF/LLM-Wiki-v2 bundle (CLAUDE.md schema + index/log + raw/)
  2. yt-dlp: enumerate the channel, pull each video's captions (YouTube auto-subs
     — free & instant). No captions? fall back to whisper on the audio.
  3. write one immutable transcript per video into raw/transcripts/
  4. `claude -p` inside the brain ingests the transcripts in sequential batches,
     each batch running CLAUDE.md's Ingest workflow (the LLM Wiki v2 SOP) end to end.

Downloads run in parallel (--jobs, default 6 — capped low because YouTube
rate-limits, not the machine). Whisper fallback is throttled separately
(--whisper-jobs, default 2 — CPU-bound). Ingest is sequential by design: each
batch is one agent following the SOP, integrating its sources into the wiki the
previous batch left, so entity/concept pages accumulate instead of colliding.

Usage:
  ./channel_brain.py "https://www.youtube.com/@channel" [--name my-brain]
  ./channel_brain.py URL --jobs 8                      # 8 parallel caption downloads
  ./channel_brain.py URL --limit 5 --no-ingest        # rip only, quick test
  ./channel_brain.py URL --no-whisper                 # captions only, never transcribe audio
  ./channel_brain.py ~/book.pdf --name my-brain       # local doc (pdf/docx/doc/rtf/odt/html/txt/md) or a folder of them
  ./channel_brain.py --selftest                       # run the vtt-parser check

Deps: yt-dlp, ffmpeg (for whisper fallback), whisper, claude — all on PATH.
Local docs: pdftotext (poppler) for PDFs, macOS textutil for docx/doc/rtf/odt/html.
"""
import argparse, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "templates" / "CLAUDE.md"
BATCH = 5  # ponytail: transcripts per SOP ingest batch — keeps one agent's context bounded. Raise if videos are short.
WIN_TOKENS = 8000  # ponytail: soft per-window target for doc ingestion (chars/4 ≈ tokens). A book splits into ~5–10k-token windows, each its OWN SOP pass (one agent per doc file already); a doc under target → one window → one pass, no overhead.
INGEST_MODEL = "claude-opus-5-5"  # pin the ingest subprocess's model (needs claude CLI ≥ 2.1.316); switch to claude-sonnet-5-5 to cut cost on bulk ingests


# ---------- vtt → clean text ----------
def vtt_to_text(vtt: str) -> str:
    """Strip a WEBVTT file (incl. YouTube rolling auto-captions) to plain text."""
    out = []
    for line in vtt.splitlines():
        line = line.strip()
        if not line or "-->" in line:
            continue
        if line in ("WEBVTT",) or re.match(r"^(Kind|Language|NOTE)\b", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)          # inline <00:00:..> / <c> tags
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        if out and out[-1] == line:                   # collapse rolling duplicates
            continue
        out.append(line)
    return "\n".join(out)


# ---------- helpers ----------
def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def tail(err, n=200):
    """Last useful line of a failed subprocess, for the skip reason."""
    lines = [l for l in (err or "").strip().splitlines() if l.strip()]
    return (lines[-1][:n] if lines else "no stderr")


# ponytail: yt-dlp needs a JS runtime or YouTube extraction degrades to fallback
# clients that 403 on media URLs. Only deno is enabled by default; reuse whatever
# runtime is already on PATH. Upgrade path: install deno and drop this.
YTDLP = ["yt-dlp"] + next(
    (["--js-runtimes", rt] for rt in ("deno", "node", "bun") if shutil.which(rt)), [])


def slug(s: str, n=60) -> str:
    s = re.sub(r"[^\w\s-]", "", (s or "").lower()).strip()
    return re.sub(r"[\s_-]+", "-", s)[:n] or "video"


def vid_of(p: Path) -> str:
    """Video id from a transcript/source filename ('…-<id>.md' → '<id>')."""
    return p.name.rsplit("-", 1)[-1][:-3]


def brain_name(name_arg: str, url: str) -> str:
    """Brain dir name: explicit --name wins, else derive from the channel handle."""
    if name_arg:
        return slug(name_arg)
    m = re.search(r"@([\w.-]+)", url or "") or re.search(r"/(?:c|channel|user)/([\w.-]+)", url or "")
    return f"{slug(m.group(1)) if m else 'channel'}-brain"


def scaffold(brain: Path, url: str, title: str):
    (brain / "raw" / "transcripts").mkdir(parents=True, exist_ok=True)
    if not (brain / "CLAUDE.md").exists():  # ponytail: don't clobber a brain's co-evolved schema on re-ingest; reschema by hand if template must propagate
        schema = SCHEMA.read_text().replace("{{BRAIN_TITLE}}", title).replace("{{CHANNEL_URL}}", url)
        (brain / "CLAUDE.md").write_text(schema)
    if not (brain / "index.md").exists():
        (brain / "index.md").write_text(
            f"---\ntype: Index\ntitle: {title}\ndescription: Knowledge brain built from {url}\n---\n\n"
            f"# {title}\n\nWiki catalog. Sections appear here as videos are ingested "
            f"(see `sources/`, `entities/`, `concepts/`, `synthesis/`).\n\n"
            f"Source channel: {url}\n"
        )
    if not (brain / "log.md").exists():
        (brain / "log.md").write_text(f"# Log\n\nAppend-only. `## [YYYY-MM-DD] <op> | <title>`\n")


def list_videos(url: str):
    r = run([*YTDLP, "--flat-playlist", "-J", url])
    if r.returncode != 0:
        sys.exit(f"yt-dlp failed to read channel:\n{r.stderr.strip()[-800:]}")
    data = json.loads(r.stdout)
    entries = data.get("entries") or [data]
    # channels nest tabs (Videos/Shorts/…) → flatten one level
    flat = []
    for e in entries:
        if e and e.get("entries"):
            flat.extend(x for x in e["entries"] if x)
        elif e:
            flat.append(e)
    return [e for e in flat if e.get("id")]


def fetch_transcript(vid: str, tmp: Path, use_whisper: bool, wmodel: str, whisper_sem):
    """Return (text, info dict) for one video, or (None, info) on failure.
    Caption fetch runs freely (caller caps concurrency); whisper is throttled by
    whisper_sem — it's CPU-bound and each process already uses every core."""
    watch = f"https://www.youtube.com/watch?v={vid}"
    run([*YTDLP, "--skip-download", "--write-auto-subs", "--write-subs",
         "--sub-langs", "en.*,en", "--sub-format", "vtt", "--write-info-json",
         "-o", str(tmp / "%(id)s.%(ext)s"), watch])
    info = {}
    ij = tmp / f"{vid}.info.json"
    if ij.exists():
        info = json.loads(ij.read_text())
    vtts = sorted(glob.glob(str(tmp / f"{vid}*.vtt")), key=len)  # shortest lang tag first (en over en-orig)
    if vtts:
        text = vtt_to_text(Path(vtts[0]).read_text())
        if text.strip():
            return text, info
    if not use_whisper:
        info["_fail"] = "no captions and --no-whisper set"
        return None, info
    # fallback: download audio, whisper it (throttled — CPU-bound)
    r = run([*YTDLP, "-x", "--audio-format", "mp3", "-o", str(tmp / f"{vid}.%(ext)s"), watch])
    audio = next(iter(glob.glob(str(tmp / f"{vid}.mp3"))), None)
    if not audio:
        info["_fail"] = f"no captions; audio download failed: {tail(r.stderr)}"
        return None, info
    with whisper_sem:
        w = run(["whisper", audio, "--model", wmodel, "--output_format", "txt",
                 "--output_dir", str(tmp), "--language", "en", "--fp16", "False"])
    txt = tmp / f"{vid}.txt"
    if txt.exists():
        return txt.read_text(), info
    # ponytail: whisper dies silently on a missing model (proxy-blocked weights
    # download) — surface its stderr instead of reporting "no transcript".
    info["_fail"] = f"no captions; whisper failed: {tail(w.stderr)}"
    return None, info


MEDIA_EXT = {".mp3", ".mp4", ".m4a", ".webm", ".mkv", ".opus", ".wav", ".aac", ".part", ".ytdl"}


def purge_media(root: Path) -> int:
    """Delete any downloaded audio/video under root. Transcripts (.md) are the
    immutable source and are never touched."""
    n = 0
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in MEDIA_EXT:
            try:
                p.unlink()
                n += 1
            except OSError:
                pass
    return n


def process_video(e, brain, tmp, use_whisper, wmodel, whisper_sem):
    """Fetch + write one transcript; clean its temp files. Returns (entry, path|None)."""
    vid = e["id"]
    try:
        text, info = fetch_transcript(vid, tmp, use_whisper, wmodel, whisper_sem)
        f = write_transcript(brain, e, text, info) if text and text.strip() else None
        if not f:
            e["_fail"] = info.get("_fail") or "captions empty"
    finally:
        for junk in glob.glob(str(tmp / f"{vid}*")):
            try:
                os.remove(junk)
            except OSError:
                pass
    return e, f


def write_transcript(brain: Path, e: dict, text: str, info: dict):
    vid = e["id"]
    title = info.get("title") or e.get("title") or vid
    date = info.get("upload_date") or ""  # YYYYMMDD
    dstr = f"{date[:4]}-{date[4:6]}-{date[6:]}" if len(date) == 8 else "unknown"
    dur = info.get("duration")
    # Long transcripts split into WIN_TOKENS windows like docs (each its own SOP pass); short ones stay one file.
    wins = windows(text)
    out = []
    for i, w in enumerate(wins, 1):
        tag = "" if len(wins) == 1 else f"-p{i:02d}"
        part = "" if len(wins) == 1 else f"window: {json.dumps(f'{i}/{len(wins)}')}\n"
        head = title if len(wins) == 1 else f"{title} — part {i}/{len(wins)}"
        fn = brain / "raw" / "transcripts" / f"{date or '0'}-{slug(title)}{tag}-{vid}.md"
        fn.write_text(f"---\ntype: Transcript\ntitle: {json.dumps(title)}\n"
                      f"resource: https://www.youtube.com/watch?v={vid}\n"
                      f"upload_date: {dstr}\nduration_s: {dur or ''}\n{part}---\n\n"
                      f"# {head}\n\n{w.strip()}\n")
        out.append(fn)
    return out


def _claude(brain: Path, prompt: str, label: str) -> str:
    print(f"  {label}…")
    r = subprocess.run(["claude", "-p", prompt, "--permission-mode", "acceptEdits",
                        "--model", INGEST_MODEL],
                       cwd=brain, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  {label}: claude returned non-zero; continuing.")
    return r.stdout or ""


INGEST_PROMPT = """Read CLAUDE.md and follow its **Ingest** workflow END TO END for the raw sources \
below. This is the LLM Wiki v2 SOP: integrate each source into the EXISTING wiki — do not dump and do \
not defer any step.

For the batch:
- Read each raw source in full.
- Write its `type: Source` summary page in sources/ — one per raw file; KEEP the raw filename's trailing \
id (the text after its last '-') at the end of the source filename — it is the resume key.
- Files under raw/docs/ are documents (books, PDFs, notes), not videos. If a document's author is not \
the person/channel this brain is about, say so in a banner at the top of its source page, tag it \
`external-author`, attribute its claims to that author everywhere, and flag where it contradicts the \
brain's subject. A document is often a whole book: extract EVERY distinct teaching/idea into its own \
concept page (a book typically yields 10–20), not just a chapter summary on the source page.
- Create or UPDATE every entity (person/org/product/tool/place) and concept (idea/theme/method) page it \
touches: one page per unique thing, merge aliases, ACCUMULATE new facts onto the existing page, bump its \
`timestamp`, and flag where a newer video contradicts an older claim.
- Cross-link both directions — source ↔ its entities/concepts, and related entities/concepts to each other.
- Update or add synthesis/ pages for the cross-video theses.
- Refresh the affected index.md files and append ONE log.md ingest entry for this batch.
Work only inside this wiki directory. A single video may touch 5–15 pages — that's expected.

Raw sources:
{rels}
"""


# ---------- local documents ----------
DOC_EXT = {".pdf", ".docx", ".doc", ".rtf", ".odt", ".html", ".htm", ".txt", ".md"}


def doc_text(p: Path) -> str:
    ext = p.suffix.lower()
    if ext in (".txt", ".md"):
        return p.read_text(errors="replace")
    # ponytail: textutil is macOS built-in; swap for pandoc if this ever runs on Linux
    cmd = ["pdftotext", "-enc", "UTF-8", str(p), "-"] if ext == ".pdf" else \
          ["textutil", "-convert", "txt", "-stdout", str(p)]
    r = run(cmd)
    if r.returncode != 0:
        raise RuntimeError(tail(r.stderr))
    return r.stdout


def windows(text: str, target: int = WIN_TOKENS):
    """Pack paragraphs into ~target-token windows (chars/4 ≈ tokens), never splitting a
    paragraph. A doc under target yields ONE window, so short docs stay a single pass.
    Boundary-respecting at paragraph granularity — no book-specific chapter detection."""
    out, cur, size = [], [], 0
    for p in re.split(r"\n\s*\n", text.strip()):
        t = len(p) // 4
        if cur and size + t > target:
            out.append("\n\n".join(cur)); cur, size = [], 0
        cur.append(p); size += t
    if cur:
        out.append("\n\n".join(cur))
    return out or [text.strip()]


def add_docs(brain: Path, src: Path):
    """Extract text from a local doc (or every doc under a folder) into raw/docs/, verbatim.
    Id = content hash, so re-adding the same file is a no-op. Returns the new raw files."""
    files = sorted(f for f in (src.rglob("*") if src.is_dir() else [src])
                   if f.is_file() and f.suffix.lower() in DOC_EXT)
    if not files:
        sys.exit(f"no supported documents at {src} ({', '.join(sorted(DOC_EXT))})")
    ddir = brain / "raw" / "docs"
    ddir.mkdir(parents=True, exist_ok=True)
    done = {vid_of(p) for p in ddir.glob("*.md")}
    new = []
    for f in files:
        did = hashlib.sha1(f.read_bytes()).hexdigest()[:10]
        if did in done:
            print(f"skip (already in brain)  {f.name}")
            continue
        try:
            text = doc_text(f)
        except Exception as e:
            print(f"no text  {f.name}  — {e}")
            continue
        words = len(text.split())
        if words < 50:  # ponytail: scanned PDF with no text layer — OCR it first (e.g. ocrmypdf); not built in
            print(f"no text  {f.name}  — only {words} words; scanned without a text layer? OCR it first")
            continue
        wins = windows(text)
        for i, w in enumerate(wins, 1):
            # ponytail: hash stays the LAST filename token so vid_of()/skip still work; -pNN keeps window files (and their source pages) distinct
            tag = "" if len(wins) == 1 else f"-p{i:02d}"
            part = "" if len(wins) == 1 else f"window: {json.dumps(f'{i}/{len(wins)}')}\n"
            head = f.stem if len(wins) == 1 else f"{f.stem} — part {i}/{len(wins)}"
            out = ddir / f"{slug(f.stem)}{tag}-{did}.md"
            out.write_text(f"---\ntype: Document\ntitle: {json.dumps(f.stem)}\n"
                           f"resource: {json.dumps(str(f.resolve()))}\nformat: {f.suffix.lower()[1:]}\n"
                           f"{part}words: {len(w.split())}\n---\n\n# {head}\n\n{w.strip()}\n")
            new.append(out)
        print(f"ok  {f.name}  ({words} words, {len(wins)} window{'' if len(wins) == 1 else 's'})")
    return new


def ingest(brain: Path, files):
    """SOP-driven ingest: each batch is one claude agent running the brain's CLAUDE.md
    Ingest workflow end to end, integrating sources into the EXISTING wiki (source page +
    entity/concept updates + synthesis + index + log).

    Batches run SEQUENTIALLY on purpose — each agent sees the wiki the previous one left,
    so it updates existing entity/concept pages instead of racing another agent on the same
    file. That is what makes cross-video links complete without a staging/consolidate detour.
    ponytail: serial is the SOP done straight — fine for tens–low-hundreds of videos. If
    ingest wall-time ever dominates, shard batches by disjoint entity namespace (never
    reintroduce a parallel free-for-all on shared pages).
    """
    files = sorted(files)
    # Resume: a video already has a source page ⇒ it's ingested. Skip it. This makes any
    # interrupted ingest restartable — just re-run; --fresh (which wipes sources/) forces a
    # full rebuild. ponytail: source-page-exists is the resume signal, no extra state file.
    done = {vid_of(p) for p in (brain / "sources").glob("*.md")}
    todo = [f for f in files if vid_of(f) not in done]
    if len(todo) < len(files):
        print(f"  ingest: {len(files) - len(todo)}/{len(files)} already ingested, resuming with {len(todo)} left")
    if not todo:
        print("  ingest: nothing to do — every transcript already has a source page")
        return
    # ponytail: docs and windowed (long) transcripts get one agent per file; short transcripts go BATCH at a time
    windowed = lambda f: re.search(r"-p\d\d$", f.stem.rsplit("-", 1)[0])
    docs = [f for f in todo if f.parent.name == "docs" or windowed(f)]
    vids = [f for f in todo if f not in docs]
    batches = [[d] for d in docs] + [vids[i:i + BATCH] for i in range(0, len(vids), BATCH)]
    print(f"  ingest: {len(todo)} sources in {len(batches)} batches (SOP, sequential)")
    for idx, batch in enumerate(batches, 1):
        rels = "\n".join(f"- {f.relative_to(brain)}" for f in batch)
        _claude(brain, INGEST_PROMPT.format(rels=rels),
                f"ingest batch {idx}/{len(batches)} ({len(batch)} sources)")


GENERATED = ("sources", "entities", "concepts", "synthesis")  # the LLM-written layer (raw/ + CLAUDE.md are kept)


def reingest(a):
    """Re-run the SOP ingest over transcripts already in raw/ — no rip, no re-download.
    Recovers a brain after a failed/partial ingest. With --fresh, wipe the generated
    layer first so the rebuild is clean (raw/ is the source of truth and is never touched)."""
    if not shutil.which("claude"):
        sys.exit("missing dependency: claude")
    brain = Path(a.out) / brain_name(a.name, a.url)
    files = sorted([*(brain / "raw" / "transcripts").glob("*.md"), *(brain / "raw" / "docs").glob("*.md")])
    if not files:
        sys.exit(f"no raw sources to reingest in {brain / 'raw'}")
    if not (brain / "CLAUDE.md").exists():
        sys.exit(f"brain has no CLAUDE.md schema: {brain}")
    if a.fresh:
        for sub in GENERATED:
            shutil.rmtree(brain / sub, ignore_errors=True)
        for f in ("index.md", "log.md"):
            (brain / f).unlink(missing_ok=True)
        print(f"--fresh: wiped generated layer, kept {len(files)} transcripts + CLAUDE.md")
    print(f"Re-ingesting {len(files)} transcripts into {brain} (SOP, sequential) …")
    ingest(brain, files)
    print(f"Done. Open the brain: {brain}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", nargs="?", help="channel / playlist / video URL, or a local document or folder of documents")
    ap.add_argument("--name", help="brain dir name (default: derived from channel)")
    ap.add_argument("--out", default=str(HERE / "brains"), help="parent dir for brains")
    ap.add_argument("--sort", choices=("channel", "views"), default="channel",
                    help="channel order (newest first, default) or most-viewed first. "
                         "YouTube's own ?sort=p URL param is ignored by yt-dlp, so we sort locally.")
    ap.add_argument("--limit", default="30", metavar="N|all",
                    help="max NEW (not-yet-ingested) videos to rip: a number or 'all' (default 30). "
                         "Re-running the same channel walks deeper into the back catalog.")
    ap.add_argument("--no-whisper", action="store_true", help="captions only; skip audio transcription")
    ap.add_argument("--whisper-model", default="base")
    ap.add_argument("--no-ingest", action="store_true", help="rip + transcribe only")
    ap.add_argument("--reingest", action="store_true",
                    help="don't rip; re-run the SOP ingest over the transcripts already in raw/ "
                         "(needs --name or a url to locate the brain). Use to rebuild after a failed ingest.")
    ap.add_argument("--fresh", action="store_true",
                    help="with --reingest: wipe the LLM-generated layer first (sources/entities/concepts/"
                         "synthesis + index.md/log.md), keeping raw/ transcripts + CLAUDE.md, for a clean rebuild.")
    ap.add_argument("--jobs", type=int, default=6,
                    help="parallel caption downloads (default 6; >8 risks YouTube 429 throttling)")
    ap.add_argument("--whisper-jobs", type=int, default=2,
                    help="parallel whisper transcribes (default 2; CPU-bound, 1 for small/medium models)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.reingest:
        return reingest(a)
    if not a.url:
        ap.error("channel URL required (or --reingest --name … / --selftest)")

    src = Path(a.url).expanduser()
    if src.exists():
        return docs_main(a, src)

    for tool in ("yt-dlp",) + (() if a.no_whisper else ("whisper", "ffmpeg")):
        if not shutil.which(tool):
            sys.exit(f"missing dependency: {tool}")

    if str(a.limit).lower() == "all":
        cap = None
    else:
        try:
            cap = max(1, int(a.limit))
        except ValueError:
            sys.exit("--limit must be a number or 'all'")
    print(f"Reading channel: {a.url}")
    vids = list_videos(a.url)
    if not vids:
        sys.exit("no videos found")
    if a.sort == "views":
        # ponytail: flat-playlist already carries view_count — sort here rather than
        # asking YouTube. Missing counts (live/premieres) sort last, not first.
        vids.sort(key=lambda e: e.get("view_count") or 0, reverse=True)
    name = brain_name(a.name, a.url)
    brain = Path(a.out) / name
    title = name.replace("-", " ").title()
    scaffold(brain, a.url, title)

    tdir = brain / "raw" / "transcripts"
    done = {vid_of(p) for p in tdir.glob("*.md")}  # video ids already ripped
    todo = [e for e in vids if e["id"] not in done]  # not-yet-ingested, newest first
    already = len(vids) - len(todo)
    if already:
        print(f"{already} of {len(vids)} already ingested, skipping.")
    if cap:
        todo = todo[:cap]  # cap NEW videos, not the channel window — re-runs walk deeper into the back catalog
    print(f"Brain: {brain}  ({len(todo)} to ingest, {len(vids)} on channel)")
    jobs = max(1, a.jobs)
    if jobs > 8:
        print(f"warning: --jobs {jobs} > 8 risks YouTube rate-limiting (429) which slows the whole run.")
    whisper_sem = threading.Semaphore(max(1, a.whisper_jobs))
    print(f"Ripping {len(todo)} videos — {jobs} parallel downloads"
          + ("" if a.no_whisper else f", {max(1, a.whisper_jobs)} parallel transcribes") + " …")
    new_files = []
    with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(max_workers=jobs) as ex:
        tmp = Path(td)
        futs = {ex.submit(process_video, e, brain, tmp, not a.no_whisper, a.whisper_model, whisper_sem): e
                for e in todo}
        for n, fut in enumerate(as_completed(futs), 1):
            e, f = fut.result()
            title = e.get("title") or e["id"]
            if f:
                new_files.extend(f)
                print(f"[{n}/{len(todo)}] ok  {title}")
            else:
                why = (e.get("_fail") or "unknown")
                print(f"[{n}/{len(todo)}] no transcript  {title}  — {why}")

    print(f"Ripped {len(new_files)} new transcripts.")
    if new_files and not a.no_ingest:
        print("Ingesting into wiki brain via claude -p …")
        ingest(brain, new_files)
    # media never persists: audio is deleted per-video after transcription; this is
    # the end-of-run guarantee for anything a crash left behind (stray .part / audio).
    purged = purge_media(brain)
    if purged:
        print(f"Purged {purged} leftover media file(s).")
    print(f"Done. Open the brain: {brain}")
    if a.no_ingest and new_files:
        print(f"To ingest later:  cd {brain} && claude   (then: 'ingest raw/transcripts')")


def docs_main(a, src: Path):
    """Local file/folder → raw/docs/ → SOP ingest, into an existing (or new) brain."""
    if not a.name:
        sys.exit("local documents need --name <brain-dir> (which brain to add them to)")
    need = ["claude"] if not a.no_ingest else []
    if any(f.suffix.lower() == ".pdf" for f in ([src] if src.is_file() else src.rglob("*.pdf"))):
        need.append("pdftotext")
    for tool in need:
        if not shutil.which(tool):
            sys.exit(f"missing dependency: {tool}")
    brain = Path(a.out) / brain_name(a.name, "")
    scaffold(brain, str(src), brain.name.replace("-", " ").title())
    new_files = add_docs(brain, src)
    print(f"Added {len(new_files)} new document(s) to {brain / 'raw' / 'docs'}.")
    if new_files and not a.no_ingest:
        print("Ingesting into wiki brain via claude -p …")
        ingest(brain, new_files)
    print(f"Done. Open the brain: {brain}")


def selftest():
    vtt = """WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000 align:start position:0%
hello<00:00:00.500><c> there</c>

00:00:02.000 --> 00:00:04.000 align:start position:0%
hello there

00:00:04.000 --> 00:00:06.000
welcome to the channel
"""
    got = vtt_to_text(vtt)
    assert got == "hello there\nwelcome to the channel", repr(got)
    assert slug("Hello, World! #1") == "hello-world-1"
    paras = [f"para {i} " + "x" * 3996 for i in range(5)]  # ~1000 tokens each
    ws = windows("\n\n".join(paras), target=2500)
    assert len(ws) == 3 and "\n\n".join(ws) == "\n\n".join(paras), ws  # packs whole paragraphs, loses nothing
    assert windows("short") == ["short"]
    with tempfile.TemporaryDirectory() as td:
        doc = Path(td) / "My Notes.txt"
        doc.write_text("word " * 60)
        brain = Path(td) / "b"
        [f] = add_docs(brain, doc)
        assert f.parent.name == "docs" and vid_of(f) == hashlib.sha1(doc.read_bytes()).hexdigest()[:10], f
        assert "words: 60" in f.read_text()
        assert add_docs(brain, doc) == []  # same content → skipped
    print("selftest ok")


if __name__ == "__main__":
    main()
