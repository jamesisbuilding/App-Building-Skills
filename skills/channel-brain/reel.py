#!/usr/bin/env python3
"""
reel — rip a short video (Instagram reel, TikTok, YouTube Short, …) into a *format
study card*: spoken transcript + caption + sampled keyframes, laid into the
hook / story / visuals template a persona uses to reverse-engineer what makes it work.

The tool does the GRUNT — download, transcribe, grab frames. It deliberately does NOT
do the JUDGMENT: naming the hook type, reading the visual tricks, and spotting the
pattern that repeats across your 9 study posts is the human's rep. That's the point.

  ./reel.py <url> [<url> …]                 # one study card per reel
  ./reel.py <url> --out study --frames 6    # more sampled frames
  ./reel.py <url> --cookies cookies.txt     # Instagram often needs your login cookies
  ./reel.py --selftest

Deps on PATH: yt-dlp, ffmpeg (+ ffprobe), whisper.
Output: <out>/<creator>/<id>/study-card.md  +  frame-NN.jpg  (default out: study/)
"""
import argparse, glob, json, subprocess, sys, tempfile
from pathlib import Path

from channel_brain import run, slug  # reuse

HERE = Path(__file__).resolve().parent

CARD = """---
type: ReelStudy
source: {url}
creator: {creator}
reel_id: {rid}
duration_s: {dur}
metrics: {metrics}
---

# Format study — {creator} ({rid})

> The grunt work is filled in below (spoken transcript, caption, frames). The JUDGMENT
> is YOURS — that's the rep: name the hook type, read the visual tricks off the frames,
> and once you have several cards, find the pattern that REPEATS. That repeating skeleton
> is your format. Don't let the tool do that part for you.

## 1. Hook (first 3s)
- Spoken opener (from transcript): {hook_line}
- On-screen text: _(read frame-01)_ …
- Type: _(question | negative/controversial | target-a-pain | establish-expertise | recognizable-ref | visual-angle | activity-while-talking)_ …

## 2. Story (the middle)
- The ONE idea: …
- Arc: _(pain→pursuit→payoff | list of tips | demo | …)_ …
- Full spoken transcript:

{transcript}

## 3. Visuals / packaging  _(fill by looking at the frames below)_
- Camera / angle: …
- Cut pace / editing: …
- Captions / text style: …
- Audio / music: …
- Activity-while-talking ("pope in the pool")? …

## Frames
{frame_links}

## Caption (verbatim)
{caption}
"""


SWIPE_HEADER = """# Swipe file — {creator}

One row per studied reel. Fill Hook / Story / Visuals from each card + its frames, then
read DOWN each column across your reels — the thing that REPEATS is your format.

| Reel | Hook (type) | Story (one idea / arc) | Visuals |
|---|---|---|---|
"""


def _cell(s: str, n: int = 90) -> str:
    """Make text safe for a markdown table cell."""
    s = (s or "").replace("|", "/").replace("\n", " ").strip()
    return (s[:n] + "…") if len(s) > n else (s or "…")


def append_swipe(creator_dir: Path, rid: str, hook_line: str):
    """Append this reel as a row in the creator's cross-reel comparison table (dedup by id)."""
    f = creator_dir / "swipe-file.md"
    text = f.read_text() if f.exists() else SWIPE_HEADER.format(creator=creator_dir.name)
    link = f"[{rid}]({rid}/study-card.md)"
    if link in text:
        return
    if not text.endswith("\n"):
        text += "\n"
    f.write_text(text + f"| {link} | {_cell(hook_line)} | … | … |\n")


def frame_times(dur: float, n: int):
    """n evenly-spaced sample timestamps (midpoints of n equal slices)."""
    if not dur or dur <= 0 or n <= 0:
        return []
    return [round(dur * (i + 0.5) / n, 2) for i in range(n)]


def probe_duration(video: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nk=1:nw=1", str(video)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def rip(url: str, tmp: Path, cookies: str):
    """yt-dlp: download the video + its info.json. Returns (video_path|None, info dict)."""
    cmd = ["yt-dlp", "--write-info-json", "-o", str(tmp / "%(id)s.%(ext)s")]
    if cookies:
        cmd += ["--cookies", cookies]
    cmd.append(url)
    r = run(cmd)
    info = {}
    ij = next(iter(glob.glob(str(tmp / "*.info.json"))), None)
    if ij:
        info = json.loads(Path(ij).read_text())
    vids = [p for p in glob.glob(str(tmp / "*.*"))
            if not p.endswith(".info.json") and not p.endswith(".json")]
    if not vids:
        print(f"  yt-dlp got no video for {url}\n  {r.stderr.strip()[-300:]}")
        return None, info
    return Path(sorted(vids, key=len)[0]), info


def transcribe(video: Path, tmp: Path, model: str) -> str:
    # whisper accepts a video file (extracts audio via ffmpeg itself)
    run(["whisper", str(video), "--model", model, "--output_format", "txt",
         "--language", "en", "--fp16", "False", "--output_dir", str(tmp)])
    txt = tmp / (video.stem + ".txt")
    return txt.read_text().strip() if txt.exists() else ""


def grab_frames(video: Path, dur: float, n: int, outdir: Path):
    times = frame_times(dur, n) or [0]  # unknown duration → at least the first frame
    names = []
    for i, t in enumerate(times, 1):
        out = outdir / f"frame-{i:02d}.jpg"
        run(["ffmpeg", "-ss", str(t), "-i", str(video), "-frames:v", "1",
             "-q:v", "2", "-y", str(out)])
        if out.exists():
            names.append(out.name)
    return names


def study(url: str, out: Path, frames: int, cookies: str, model: str):
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        video, info = rip(url, tmp, cookies)
        if not video:
            return None
        rid = info.get("id") or video.stem
        creator = slug(info.get("uploader_id") or info.get("uploader")
                       or info.get("channel") or "creator")
        dur = info.get("duration") or probe_duration(video)
        caption = (info.get("description") or info.get("title") or "").strip()
        metrics = {k: info[k] for k in ("view_count", "like_count", "comment_count") if info.get(k)}

        dest = out / creator / rid
        dest.mkdir(parents=True, exist_ok=True)
        transcript = transcribe(video, tmp, model) or "_(no speech transcribed)_"
        (dest / "transcript.txt").write_text(transcript + "\n")  # verbatim STT, immutable — never summarized
        frame_names = grab_frames(video, float(dur or 0), frames, dest)

        hook_line = next((s.strip() for s in transcript.replace("\n", " ").split(".") if s.strip()), "")
        card = CARD.format(
            url=url, creator=creator, rid=rid, dur=dur or "",
            metrics=json.dumps(metrics) if metrics else "{}",
            hook_line=hook_line + ("…" if hook_line else ""),
            transcript=transcript,
            frame_links="\n".join(f"![{n}]({n})" for n in frame_names) or "_(no frames)_",
            caption=caption or "_(none)_",
        )
        (dest / "study-card.md").write_text(card)
        append_swipe(dest.parent, rid, hook_line)  # add a row to the cross-reel comparison table
    return dest / "study-card.md"


def selftest():
    assert frame_times(10, 4) == [1.25, 3.75, 6.25, 8.75], frame_times(10, 4)
    assert frame_times(0, 4) == [] and frame_times(10, 0) == []
    assert slug("Hot High Priestess") == "hot-high-priestess"
    assert _cell("a | b\nc") == "a / b c"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        append_swipe(d, "abc", "the hook")
        append_swipe(d, "abc", "the hook")  # dedup: no second row
        append_swipe(d, "xyz", "another")
        rows = [ln for ln in (d / "swipe-file.md").read_text().splitlines() if ln.startswith("| [")]
        assert len(rows) == 2, rows
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*", help="reel / short video URLs")
    ap.add_argument("--out", default=str(HERE / "study"), help="output dir (default: study/)")
    ap.add_argument("--frames", type=int, default=5, help="keyframes to sample (default 5)")
    ap.add_argument("--cookies", help="cookies.txt (Instagram reels usually need your login)")
    ap.add_argument("--whisper-model", default="base")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not a.urls:
        ap.error("give at least one reel URL (or --selftest)")
    for tool in ("yt-dlp", "ffmpeg", "ffprobe", "whisper"):
        import shutil
        if not shutil.which(tool):
            sys.exit(f"missing dependency: {tool}")

    out = Path(a.out)
    for i, url in enumerate(a.urls, 1):
        print(f"[{i}/{len(a.urls)}] ripping {url} …")
        card = study(url, out, a.frames, a.cookies, a.whisper_model)
        print(f"  wrote {card}" if card else "  skipped (no video)")
    print(f"Done. Study cards under {out}. Fill the blanks by reading the frames; find the pattern across them yourself.")


if __name__ == "__main__":
    main()
