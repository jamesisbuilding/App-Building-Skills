# app-set-up-infra

A Claude Code skill that sets up an iOS app's infrastructure:
- the branches: `main` (prod), `release/x.y.z` (one per version), `develop`, and `feat/` / `fix/` / `task/` branches
- a private GitHub repo
- GitHub Actions that upload every push to `main` to TestFlight, signed through an App Store Connect API key

It asks you for what only you have (repo, key ID, issuer ID, key file) with multiple-choice questions, and saves the answers in the project's git-ignored `tool/asc.env`, so the next run doesn't ask again. You run the `gh secret set` commands yourself; it never handles key contents.

## Use it

In Claude Code, inside the app's project: `/app-set-up-infra`, or "set up CI and the branches".

## Install

This folder is the skill. It's installed by a link: `~/.claude/skills/app-set-up-infra` points here. To install it on another machine:

```bash
ln -s ~/Desktop/app-set-up-infra ~/.claude/skills/app-set-up-infra
```

## What's here

| Path | What it is |
|---|---|
| `SKILL.md` | The procedure: read the project, ask, branches, CI, GitHub, watch CI until green, report |
| `RETRO.md` | The 7 Minute Math setup (2026-10-31): what worked, what went wrong, and the fixes the rules come from |
| `templates/` | The workflow, upload script, export options, saved-answers file and README sections, taken from 7 Minute Math |

Built 2026-10-31 from setting up 7 Minute Math (`jamesisbuilding/sevenminutemath`).
