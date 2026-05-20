# MRF Forum Visual Redesign — Proposal Delivered

**Date:** 2026-05-15
**Status:** Awaiting Kenny's decision on Phase 1 go-ahead

## What
Designed and delivered a full visual rebrand proposal for MineralRightsForum.com (Discourse forum). Includes six logo concepts, a full Discourse homepage mockup, a complete style guide, and a pitch deck with a three-phase zero-risk transition plan. All assets live at `directory.mineralrightsforum.com` as static HTML pages.

## Why
The MRF county directories (already live at `directory.mineralrightsforum.com`) use a polished dark navy + gold design system. The forum itself uses Discourse defaults with no brand identity. The proposal brings the forum into visual alignment with the directory brand and addresses the primary objection — member disruption — with a documented phased rollout strategy.

## Key Design Decisions

**Color system:** `#0a192f` navy + `#c5a059` gold + `#f8f6f1` off-white. These are already live in the directory pages; the proposal formalizes them as the canonical MRF brand tokens.

**Typography:** Playfair Display (headings) + Inter (UI/body). Playfair gives warmth and authority appropriate for a professional community. Inter is readable at small sizes in topic lists.

**Recommended logo:** "The Strata" (Concept A) — four horizontal bars of varying width, gold bar representing the mineral layer. Most domain-specific and distinctive of the six concepts. Doubles as a favicon effectively.

**Transition strategy:** Three phases over 7+ months — opt-in, soft switch, full migration. Kenny controls every step; the old design stays fully live until he's satisfied the data supports retiring it. This was the core objection to address.

## Alternatives Considered
- Full cutover (no transition period) — rejected, Kenny's risk tolerance is low
- New subdomain/separate Discourse instance — not possible; Discourse themes are instance-level
- Plugin approach — unnecessary; native Discourse theme system handles everything needed

## Implementation Scope
~250–300 lines of custom CSS/HTML across 4–5 theme components. No Discourse core modifications, no plugins. Realistic estimate: 1–2 days of implementation work once Kenny approves.

## Reference
Full notes, design tokens, logo descriptions, implementation checklist:
`ked-os/internal/new-directory-pages/notes/mrf-redesign-proposal.md`
