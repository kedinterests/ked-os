# Skill: KED Industry News

Pulls oil & gas, mineral rights, and drilling industry news to inform KED Interests project direction and technology decisions. Surfaces trends, regulatory changes, market shifts, and competitive intelligence relevant to KED's energy sector focus.

## When to invoke

When Chris or Kenny say anything like: "prep industry news", "pull this week's news", "what's happening in O&G", "get me drilling news", "mineral rights updates", or "industry news prep."

## What this skill covers

- Oil & gas industry news and trends
- Mineral rights management and transactions
- Drilling operations and exploration updates
- Energy sector technology and digital transformation
- Regulatory changes affecting the energy sector
- Competitive landscape and market shifts
- Industry events and conferences

## Audience

KED Interests developers and decision-makers. Practical, focused on:
- Technology trends relevant to energy sector web development
- Mineral rights digitization and automation opportunities
- Drilling operations workflow and data needs
- Regulatory landscape that affects energy sector clients
- Competitive intelligence in energy tech
- Business opportunities and market shifts

De-prioritize: pure stock market news (unless company-specific), weather/environmental news unrelated to operations, non-energy tech news.

## Sources

**Source 1 — Apple Notes ("KED Industry News")**
Chris or Kenny save relevant articles manually to an Apple Notes note called "KED Industry News" throughout the week. These are hand-picked and highest priority. Retrieve via AppleScript:

```applescript
tell application "Notes"
  set theNote to first note whose name is "KED Industry News"
  return body of theNote
end tell
```

**Source 2 — Industry Newsletter Label**
All emails in the KED Gmail account with the `industry-news` label from the past 7 days. Priority order:
1. Oil & Gas Journal (`*@ogjournal.net`)
2. World Oil (`*@worldoil.com`)
3. Mineral Rights Magazine / platforms
4. Drilling Contractor News
5. Energy tech newsletters (Crunchbase, TechCrunch energy coverage)
6. Other energy sector sources

**Source 3 — General tech/business news (secondary)**
Selected items from general tech newsletters that mention energy sector or relevant technologies (Astro, Discourse, web performance).

## Full Process — Run in Order

### Step 1 — Check history for recently covered topics

Before pulling this week's pool, read `internal/news-tracking/index.md`. When a story closely matches something covered in the past 8 weeks, flag it: "⚠️ Covered [date]".

### Step 2 — Pull this week's pool

1. Run AppleScript to read "KED Industry News" note. Parse all entries into title + URL pairs.
2. Search Gmail for emails with `industry-news` label from past 7 days.
3. Read each source, extract distinct items with title, summary bullets, and source link.
4. Deduplicate across sources.
5. Filter for relevance to KED's focus (energy tech, mineral rights, drilling, regulatory).
6. Surface 10–15 items ranked by relevance. Items from Notes are always included.

**Output format:** No preamble. Group by source:
1. **Your Notes** (from Apple Notes) — always first
2. **Oil & Gas Journal**
3. Other newsletters in priority order

Within each section:
```
- **[Title]**
  [URL]
  - [Bullet: what happened]
  - [Bullet: why it matters to KED]
  - [Bullet: nuance or caveat, if any]
  - [Bullet: practical angle for web development / mineral rights opportunity]
```

3–4 bullets per item. Keep bullets as full sentences.

After outputting the pool, ask: "Want me to save this to the news tracking folder?"

### Step 3 — Fetch articles and output summaries

After Kenny or Chris selects items, fetch each article and output summaries as plain text in the chat for review before saving.

**Output format per item:**
```
**[Headline]**
[URL]

- [What happened]
- [Why it matters to KED / energy sector tech]
- [Nuance or practical angle]
- [Business implication or opportunity]
```

3–4 bullets per item.

### Step 4 — Save and track

If approved:
1. Save to `internal/news-tracking/YYYY-MM-DD-pool.md`
2. Update `internal/news-tracking/index.md` with date and headlines covered
3. Ask: "Clear the KED Industry News note for next week?" If yes, reset it via AppleScript

---

## Hard writing rules

- No em dashes. Use commas, colons, or periods.
- No semicolons. Break into two sentences if needed.
- No preamble bullets ("This is the story of..."). Lead with fact.
- Clear, scannable prose — bullets should read as full sentences, not fragments.

---

## Next Steps

After each news pool review, recommend 1–2 items that could influence KED project decisions or technology choices. Flag emerging trends that might affect the roadmap.
