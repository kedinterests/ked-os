# KED-OS Index Tooling

**Date:** 2026-04-29
**What:** Built `ked-os-index.json` and `scripts/ked.py` as the canonical index and query layer for KED-OS.
**Why:** Sessions were loading files blind with no fast way to answer "what projects exist", "what stack does X use", or "has this been built before." The index solves cold-start orientation without loading every file.
**Alternatives considered:** Using CLAUDE.md alone as the index — rejected because it bloats the always-loaded context and can't be queried programmatically.
