# No AI tells in drafted content: hard rule

**Date:** 2026-09-16
**Requested by:** Chris

## What

Every piece of content Claude drafts in KED-OS, for Kenny or Chris, in any
domain, must pass the checklist in `core/writing-rules-no-ai-tells.md`. Banned
words, no "it's not X, it's Y", no throat-clearing openers, no restating
closers, no reflexive rule of three, no hedge-stacking, no stacked transitions,
no self-narration. Three or more violations means revise before delivering,
without asking.

Wired in at: `CLAUDE.md` Output Rules and the "Writing for Kenny" section
(loaded every session), Kenny's profile in `memory/people/`, and the new
`core/` file. The same rule went into life-os and Brilliant OS the same day.

## Why

Anthropic's model-level watermark is invisible and only Anthropic can read it.
The real exposure is third-party detectors (Copyleaks, Originality.ai, GPTZero,
Turnitin) that pattern-match on stylistic tells. KED publishes under its own
name in a sector where credibility with operators matters. The tells also just
make the writing worse.

KED-OS already banned em dashes. This adds the rest of the list in one file.

Source: "AI Watermarking & Avoiding AI Tells" in the AI Works library.
