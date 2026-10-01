# Model Routing Defaults

**Date:** 2026-04-28
**What:** Sonnet is now the default model for all KED-OS sessions; Claude must prompt Chris to downgrade (Haiku) or upgrade (Opus) at session start based on task fit.
**Why:** Chris wants explicit control over model selection rather than implicit routing. Silent mismatches either waste budget (unnecessary Opus) or produce weak output (Haiku on hard problems).
**Alternatives considered:** Auto-routing without prompting (rejected — removes Chris's visibility and control).
