# Directory Category Order: Spreadsheet-Driven via Categories Sheet

**Date:** 2026-05-19
**What:** Category display order on directory pages is now controlled by a Categories sheet in the Google Spreadsheet (row order = display order), not by `sites.json` or the Sites sheet `category_order` column.
**Why:** Kenny needs to reorder categories without touching code or config files. The spreadsheet is his primary interface.
**Alternatives considered:** Editing `sites.json` directly (rejected -- not accessible to non-technical users); editing the Sites sheet `category_order` column (still works as fallback but superseded by the Categories sheet approach).
