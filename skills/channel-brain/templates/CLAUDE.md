# {{BRAIN_TITLE}} — Wiki schema & operating manual

This directory is a **persistent, LLM-maintained knowledge wiki** built from the
transcripts of a video channel, shaped as an
[Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
(OKF v0.1) bundle. Pattern source: LLM Wiki v2
(`~/Desktop/AI Essentials/llm_wiki_v2.md`).

**You (the LLM) own and write this wiki. The pipeline curates the sources (video
transcripts); you do the bookkeeping** — summarizing each video, extracting the
people/tools/ideas it covers, cross-referencing them, and keeping the picture of
the channel consistent as more videos are ingested.

Channel: {{CHANNEL_URL}}

## Three layers

1. **Raw sources** — immutable transcripts in `raw/transcripts/`, one file per
   video (frontmatter: title, url, upload date, duration). Read them; never edit
   them. Source of truth.
2. **The wiki** — the markdown pages *you* generate (`sources/`, `entities/`,
   `concepts/`, `synthesis/`). You create, update, and cross-link these.
3. **The schema** — this file. Co-evolve it with the human when a convention
   proves useful (e.g. once the channel's domain is clear, add domain sections).

## Structure

```
.
├── CLAUDE.md              # this schema
├── index.md              # root catalog — read FIRST on any query
├── log.md                # append-only chronological record
├── raw/transcripts/      # one .md per video (immutable)
├── raw/docs/             # one .md per added document — PDF/book/notes, text verbatim (immutable)
├── sources/              # one summary page per video
├── entities/             # people, orgs, products, tools mentioned across videos
├── concepts/             # ideas, techniques, themes, arguments the channel teaches
└── synthesis/            # cross-video theses: the channel's philosophy, recurring frameworks
```

Create section dirs / their `index.md` lazily — only when the first page needs them.

## OKF page conventions

- **One concept per file.** The file path IS the concept's identity — keep paths
  stable; renaming a file changes what it is. Filenames: kebab-case, descriptive.
- **Frontmatter on every page.** `type` is the only required field:

```yaml
---
type: Source          # Source | Entity | Concept | Synthesis | Comparison | Index | Log
title: <human title>
description: <one line>
resource: <path to the raw transcript, or the video URL>
tags: [tag1, tag2]
timestamp: 2026-01-01T00:00:00Z   # ISO 8601, last update
---
```

- **Links are the graph.** Cross-reference with plain relative markdown links to
  file paths — `[Jane Doe](../entities/jane-doe.md)`. Not `[[wikilinks]]`.
- **Reserved names.** `index.md` (per-directory catalog) and `log.md`
  (chronological) have fixed roles.

## Workflows

### Ingest (a batch of transcripts lands in `raw/transcripts/`)
The driver ingests in sequential batches; each batch is one agent that runs this exact
workflow end to end, integrating its sources into the wiki the previous batch left. Do
it the same way when a human asks you to ingest by hand:
1. Read each transcript fully.
2. Write a `type: Source` summary page in `sources/` — one per video. TL;DR, key
   points, the entities/concepts it covers (as links), notable claims/quotes.
   `resource:` → the raw transcript path.
3. Create or **update** affected `entities/` and `concepts/` pages; bump their
   `timestamp`. A recurring tool/person/idea gets one page that accumulates what
   every video says about it. Flag where a newer video contradicts an older claim.
4. As the corpus grows, maintain `synthesis/` pages: the channel's overall thesis,
   recurring frameworks, how ideas connect across videos.
5. Update the relevant `index.md`(s).
6. Append a `log.md` entry: `## [YYYY-MM-DD] ingest | <N videos: titles…>`.
   A single video may touch 5–15 pages — that's expected.

**Why sequential** — batches run one after another, never in parallel. An entity or
concept spans many videos, so two agents ingesting at once would both open, say,
`entities/jane-doe.md` and clobber each other, dropping cross-links. Running serially
means each batch sees the current wiki and *updates* the pages already there — which is
exactly how cross-video links stay complete. No staging files, no separate consolidation
pass; the workflow above is the whole thing.

### Query (human asks a question about the channel)
1. Read `index.md`, drill into section indexes, then pages.
2. Answer with citations (links to the pages/sources used).
3. **On a miss** (answer needed research beyond existing pages): file it back —
   a `synthesis/` page for a substantial answer, at minimum a fact-line on an
   existing page. Same question never researched twice.
4. Append a query entry to `log.md`.

### Lint (human says "health-check the wiki")
Scan for: contradictions, stale claims newer videos supersede (use `timestamp`),
orphan pages (no inbound links), concepts mentioned but lacking a page, missing
cross-references, bad/missing frontmatter. Report + suggest; don't auto-fix silently.

## log.md format
Append-only, greppable: `## [YYYY-MM-DD] <ingest|query|lint> | <title>`, then
bullets on what changed.

## Notes
- At this scale the `index.md` files ARE the search — no embedding/RAG infra until
  the wiki outgrows them.
- The channel's domain is not fixed up front — it emerges from the first videos.
  Add domain conventions to this file as they stabilize.
