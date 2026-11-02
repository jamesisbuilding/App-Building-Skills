# app-keyword-research

A Claude Code skill that validates an app idea against the App Store before you build it. It turns the idea into search phrases, measures demand (App Store autocomplete) and competition (the current top 10 apps) for each, ranks keywords by opportunity, and maps which apps own the market. It ends with a verdict, keywords to target, and an App Store title, subtitle and keyword field. It uses only Apple's public data, with no account or API key.

## Use it

In Claude Code, ask for keyword research, ASO, "is there demand for…", or competitors for an idea. Or run the script directly:

```bash
python3 -I scripts/keyword_research.py \
  --seeds "mental math, math game, brain training" \
  --country us --max-terms 120 --out research/<idea>-us-<yyyy-mm-dd>
```

It takes about 6 seconds per phrase at first, less as the same apps keep ranking, because of Apple's rate limit. Results save as it goes, and re-running into the same `--out` resumes.

## Install

```bash
ln -s ~/Desktop/app-keyword-research ~/.claude/skills/app-keyword-research
```

## What's here

| Path | What it is |
|---|---|
| `SKILL.md` | The workflow: seeds, the run, reading the results, the verdict and the store metadata |
| `scripts/keyword_research.py` | The research script (autocomplete demand, top-10 competition, opportunity ranking) |
| `scripts/test_keyword_research.py` | Its tests |
| `scripts/check_metadata.py` | Checks a title, subtitle and keyword field: character limits, Apple product names, wasted characters |
| `scripts/test_check_metadata.py` | Its tests |

`Side Projects/App Skills/app-keyword-research` is a symlink to this folder, so there's one copy to edit.
