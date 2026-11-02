# new-app-info

A Claude Code skill for when App Review replies "We need additional information to better understand the app". It reads the app's code and the connected iPhone, then writes the pack Apple asks for, covering all six items:

1. An end-to-end screen recording on a physical device. You record it from the shot list; the skill then checks it frame by frame and prepares it for upload.
2. The app's purpose and target audience.
3. Setup and access to the main features, including any credentials or sample files.
4. The external services the app uses.
5. Any regional differences.
6. Any regulated industry or protected third-party material.

It also runs Apple's "Prevent common issues" checks (2.1, 2.3.3, 3.1.1, 3.2). It finishes by reminding you to paste the reply into App Review Information → Notes in App Store Connect.

## Use it

In Claude Code, inside the app's project, paste Apple's message or type `/new-app-info`. Output goes to `app-store-assets/new-app-info.md`, or `./new-app-info.md` if there is no `app-store-assets` folder.

## Install

This folder is the skill. It's installed by a link: `~/.claude/skills/new-app-info` points here. To install it on another machine:

```bash
ln -s ~/Desktop/new-app-info ~/.claude/skills/new-app-info
```

## What's here

| Path | What it is |
|---|---|
| `SKILL.md` | The procedure: the six items, code checks, device iOS check, common-issue checks, the output shape and the closing Notes prompt |

Built 2026-10-31 from the 7 Minute Math review request.
