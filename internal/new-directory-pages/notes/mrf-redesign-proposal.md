# MRF Redesign Proposal

**Date:** 2026-05-15
**Status:** Proposal delivered to Kenny — awaiting decision on Phase 1
**Lives in:** `kedinterests/new-directory-pages` repo, deployed to `directory.mineralrightsforum.com`

---

## What Was Built

Three static HTML pages added to `/public` in the `new-directory-pages` project and deployed to Cloudflare Pages. They are presentation assets for a proposed visual rebrand of MineralRightsForum.com (the Discourse forum site) — not part of the directory product itself.

| Page | URL | Purpose |
|---|---|---|
| `mrf-proposal.html` | `/mrf-proposal` | Full pitch deck — opportunity, transition plan, what stays the same, Discourse implementation scope, links to assets |
| `logo-mockups.html` | `/logo-mockups` | 6 logo concepts, each shown on dark + light, with size scale |
| `mrf-redesign-mockup.html` | `/mrf-redesign` | Full Discourse homepage mockup + complete style guide |

**Routing note:** Cloudflare Pages strips `.html` extensions (clean URLs). The `[slug]` catch-all function was intercepting these. Fixed by adding explicit exclusions to `public/_routes.json`:
```json
"exclude": ["/styles.css", "/llms.txt", "/*.html", "/mrf-proposal", "/logo-mockups", "/mrf-redesign-mockup"]
```

---

## Design System

This is the canonical design language for all MRF-adjacent work. The directory pages already use it; the proposal extends it to the forum.

### Colors
| Token | Hex | Use |
|---|---|---|
| Navy | `#0a192f` | Primary background, header, text |
| Navy Mid | `#0e2040` | Card gradients, dark panels |
| Navy Light | `#1a3054` | Hover states |
| Gold | `#c5a059` | Accents, CTAs, links, active states |
| Gold Hover | `#d4b06a` | Interactive hover |
| Gold Dim | `rgba(197,160,89,0.10)` | Badge backgrounds |
| Gold Border | `rgba(197,160,89,0.25)` | Subtle borders on dark backgrounds |
| Off-white | `#f8f6f1` | Page background |
| Ink | `#0b0e14` | Body text |
| Muted | `#6b7280` | Secondary text, meta |
| Border | `#e6e7ea` | Dividers |

### Typography
| Role | Font | Weight | Size |
|---|---|---|---|
| Display / hero headings | Playfair Display | 700 | clamp(2rem, 4vw, 3.25rem) |
| Section headings | Playfair Display | 700 | 1.75rem–2.5rem |
| Card headings | Playfair Display | 700 | 1.125–1.375rem |
| Eyebrow labels | Inter | 600 | 0.6875rem, tracked 0.22em, uppercase |
| Body copy | Inter | 400 | 1rem, line-height 1.65 |
| UI / topic titles | Inter | 600 | 0.9375rem |
| Meta / timestamps | Inter | 500 | 0.8125rem, muted color |

Google Fonts import:
```
https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,700&family=Inter:wght@300;400;500;600;700&display=swap
```

---

## Logo Concepts (6 total)

All shown on both dark navy and light backgrounds with size scales.

| Concept | Name | Description | Notes |
|---|---|---|---|
| A | The Strata | 4 horizontal bars (varying width/opacity), gold bar = mineral layer | Most distinctive, domain-specific, works inline in Discourse header |
| B | The Gem | Faceted diamond SVG — girdle line, crown facets, pavilion lines | Most literal "minerals" read, good for favicons |
| C | The Seal | Circle with double ring and MRF monogram in Playfair | Most versatile — stacked + horizontal lockups, seal stands alone |
| D | The Horizon | Circle with gold horizon line and gold deposit dot below | Abstract, works at very small sizes |
| E | Pure Wordmark | Two variants: centered with gold rule / italic+bold inline | No mark needed — cleanest for small header |
| F | The Crest | Shield with strata bands inside, MRF text | Most institutional/traditional feel |

**Chris's recommendation:** A (Strata) — used in the proposal and mockup pages.

---

## Discourse Implementation Plan

The proposal is for the Discourse Default Theme (2024–2025). Implementation is ~250–300 lines of custom CSS/HTML across 4–5 theme components — no plugins, no core modifications.

### What maps to what

| Element | Effort | Mechanism |
|---|---|---|
| Color scheme (navy + gold) | 5 min | Discourse admin → Color Scheme editor |
| Fonts (Playfair + Inter) | ~5 lines CSS | Theme stylesheet |
| Header border + icon colors | ~10 lines CSS | Theme stylesheet |
| Topic list + tag styling | ~40 lines CSS | Theme stylesheet |
| Hero banner | ~60 lines HTML/CSS | `after_header` template |
| Opt-in banner + theme switcher | ~50 lines HTML/JS | Theme component |
| Custom footer | ~80 lines HTML/CSS | `footer` template |
| Logo (Strata) | Export SVG, upload | Site Settings → Logo |

### Discourse CSS variables to set
```css
:root {
  --font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  --header-font-family: 'Playfair Display', Georgia, serif;
}
.d-header { border-bottom: 3px solid #c5a059; }
/* Color scheme via admin: */
/* --primary: #0a192f */
/* --secondary: #ffffff */
/* --tertiary: #c5a059 */
/* --header_background: #0a192f */
/* --header_primary: #ffffff */
/* --highlight: #c5a059 */
```

---

## Three-Phase Transition Plan

Designed to address Kenny's concern about disrupting existing members.

**Phase 1 (Months 1–3) — Opt-in**
- Old design stays as default for all members
- Small dismissible banner: "The new Mineral Rights Forum is here — try it now"
- Members who click are switched to the new theme; their preference is saved
- Fully reversible: removing the banner ends Phase 1 with zero members forced to change

**Phase 2 (Months 4–6) — Soft switch**
- New design becomes default for all visitors and new sign-ups
- Members using the old design keep it automatically
- "Back to classic view" link in footer for anyone who wants to revert
- Old design still fully live

**Phase 3 (Month 7+) — Migration complete**
- Old design retired when adoption data shows it's time
- Kenny controls the timing; the data backs the decision

**Technical mechanism:** Discourse supports simultaneous themes natively. User theme preference is stored per account. A small JS snippet (~15 lines) in the opt-in banner can use `localStorage` + `?preview_theme_id=X` for logged-out visitors.

---

## What Doesn't Change in a Discourse Theme Swap

- All 185,000+ posts, replies, categories, and tags
- All 47,000 member accounts, trust levels, badges
- Every URL — no SEO disruption
- All integrations, plugins, admin settings
- Advertiser placements

---

## Next Steps (if Kenny approves)

1. **Kenny picks a logo direction** — A (Strata) recommended
2. **Export logo as SVG** — upload to Discourse Site Settings
3. **Create new Discourse theme** in admin, set color scheme
4. **Add Google Fonts** import to theme `<head>`
5. **Write ~40 lines of CSS** for topic list, nav pills, hover states
6. **Build hero banner** component (HTML/CSS) for `after_header`
7. **Build opt-in banner** component with theme switcher JS
8. **Build custom footer** component
9. **Phase 1 launch** — deploy opt-in banner, monitor adoption

**Reference:** The full style guide (colors, type scale, buttons, forms, components, Discourse variable mappings) is in `/mrf-redesign-mockup.html` on the live site.
