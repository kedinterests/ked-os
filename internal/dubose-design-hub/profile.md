---
name: "Dubose Design Hub"
status: live and locked down
stack: "Cloudflare Pages / Pages Functions / D1 / R2"
owner: "Chris"
updated: "2026-07-17"
---

# Dubose Design Hub

## Overview

Private remodel decision hub for Kenny & Monika Dubose's house remodel. Personal
project for Kenny, not a KED Interests business project — tracked here anyway
per the ked-os project convention. Organized by room; each room holds
"Selections" (faucets, tile, lighting, hardware) as cards with photo, category,
source link, cost, and a status pipeline (idea → shortlist → decided → ordered
→ installed). Also has a "Things I Like" inspiration board (paste-a-screenshot),
file upload/download for quotes and plans, a shared scratchpad, and search.

Started in a Claude.ai chat, handed off mid-build (backend + styles done,
frontend not started). Continued and finished in Claude Code.

## Goals

- Give Kenny, Monika, and their GC one shared place to track every remodel
  decision instead of scattered texts/screenshots.
- Keep total build effort around 2 hours — no gold-plating.
- Ship on Kenny's own GitHub + Cloudflare accounts, not BWW/KED infrastructure.

## Tech Stack

- Cloudflare Pages (git-connected deploy, no build step — plain HTML/CSS/JS)
- Cloudflare Pages Functions for the API (`functions/api/[[path]].js`)
- D1 database (binding `DB`) — schema in `schema.sql`
- R2 bucket (binding `BUCKET`) for photos/files, served through the API only
  (never public)
- Cloudflare Access (Zero Trust, email one-time-PIN) fronts the whole site;
  the API maps the verified login email to a role via the D1 `users` table
  (owner / editor / viewer)

## Architecture

See `HANDOFF.md` in the repo for the full decided architecture (do not change
without asking Chris). Key points: soft deletes everywhere, images served
through `/api/img/...` never directly from R2, `DEV_MODE=true` local-only dev
bypass (never set in production).

## Repos

- Local checkout: `~/dubose-design-hub/`
- GitHub: `kedinterests/dubose-design-hub` (private). Personal project for
  Kenny, pushed into the kedinterests org as a pragmatic call — a standalone
  `kennydubose` account/org didn't exist yet when this was built and Kenny
  chose to use kedinterests rather than stand up a new one.

## Deployment (2026-07-17)

Deployed to Cloudflare Pages under Chris's account
`45ae261c0e3c9f91d9fa2ba50e735ea3` (same account as mineralwise.com / MRF
directory work) via CLI, not git-integration — `wrangler pages deploy` direct
upload, since a full git-connected build wasn't scriptable non-interactively.
Reconnecting to git integration later (dashboard → Pages project → Settings)
is optional; direct-upload deploys work fine as-is, just need a manual
`wrangler pages deploy public --project-name dubose-design-hub` re-run after
future code changes instead of auto-deploy-on-push.

- Live URL: **https://dubose-design-hub.pages.dev**
- D1 database: `dubose-design-hub` (id `509dd729-ee07-44a1-899a-da096c4db4e5`), schema + seed loaded. Users table: Kenny (owner), Monika (editor), Chris (owner). GC not yet added — needs their email, then an INSERT into `users` plus adding them to the Access policy below.
- R2 bucket: `dubose-design-hub`
- D1/R2 bindings set via direct Cloudflare API call (no wrangler CLI command exists for Pages project bindings in wrangler 4.65)
- Zero Trust Access: done, via dashboard (wrangler OAuth token has no Access API scope, so this step can't be scripted). Self-hosted app on `dubose-design-hub.pages.dev`, policy "Household allow-list" (Emails: kenny@kedinterests.com, monikadubose@me.com, chris@kedinterests.com), identity providers set to "accept all available" (defaults to the account's One-time PIN provider). Confirmed enforcing — unauthenticated requests redirect to `kennyd.cloudflareaccess.com` for an email login code.

## Notes

Local dev quirk worth remembering: `wrangler pages dev --d1 DB --r2 BUCKET`
(CLI flags, no wrangler.toml) and `wrangler d1 execute DB --local` resolve to
*different* local sqlite files unless carefully matched — a wrangler.toml
only gets read for bindings if it sets `pages_build_output_dir`, and CLI flags
always win over config for the persistence hash regardless. Local dev DB was
seeded by loading `schema.sql`/`seed.sql` directly into the deterministic
sqlite file `wrangler pages dev --d1 DB` creates, via the `sqlite3` CLI
directly, bypassing `wrangler d1 execute` entirely.

## Contact

Kenny Dubose — see `memory/people/kenny-dubose.md`
