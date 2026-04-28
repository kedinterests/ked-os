# Project Initialization — Claude Co-Work (BWW)


## What this is
This document defines the standard, automated process Claude Co-Work must follow when you request creation of a new project. The goal is to transform raw project inputs into a fully structured workspace with preserved source materials and pre-populated canonical documents that capture the project’s meaning, scope, and constraints.

This is both an intake procedure and a knowledge-distillation process.

## Trigger
Run this process when any of the following occur:

- You request creation of a new project
- You upload project-related documents and indicate they belong to a new project
- You say “create project,” “new project,” or equivalent language

## Required inputs
Claude Co-Work must attempt to obtain:

1. Call transcripts  
2. Proposal or Scope of Work  
3. Any supporting materials (emails, briefs, notes, exports, etc.)

If a transcript or proposal/SOW is missing, Claude must prompt you to provide it or confirm it does not exist.

## Project directory creation

Use a project name derived from the proposal/SOW or confirmed with you.

Create the following structure:

project-name/
- 01_intake/
  - transcripts/
  - associated_content/
- 02_context/
- 03_planning/
- 04_deliverables/
- 05_notes/
- README.md

## Source material storage

- Save call transcripts → 01_intake/transcripts/
- Save all other source materials → 01_intake/associated_content/
- Preserve originals verbatim
- Do not summarize or rewrite files in intake folders
- If content is provided as plain text, create a file and store it verbatim

## Canonical context principle

The generated markdown files in 02_context/ and 03_planning/ are the authoritative project understanding.

Raw intake materials remain reference sources only.

If sources conflict, the Proposal/SOW is the primary authority unless you explicitly override it.

## Cross-reference core OS documents first

Before extracting risks, open questions, prerequisites, or assumptions from source materials, load and check the following:

- `core/standard-stack.md` — services, platforms, plan tiers, and infrastructure BWW already uses
- `memory/glossary.md` — known terms and tooling
- Any relevant `memory/` documents

If a potential risk, blocker, or open question is already answered in the core OS documents, document it as **resolved** with a note citing the source. Do not flag known facts as open questions.

This step is mandatory. Generating risks or open questions without checking the OS context first is an error.

---

## Structured information extraction

Analyze all source materials and identify, without inventing:

- Project objectives and purpose
- Background context
- Stakeholders and roles
- Scope of work
- Deliverables
- Explicit exclusions
- Constraints
- Assumptions
- Dependencies
- Risks
- Timeline indicators or milestones
- Technical requirements (if applicable)
- Decisions already made
- Open questions or unclear areas

If information is absent, record: Information not provided.

## Generate core documents (pre-populated)

Create and populate the following files:

- 02_context/project_context.md  
- 02_context/requirements.md  
- 03_planning/scope_summary.md  
- 03_planning/risks.md  
- 03_planning/timeline.md  

No file should be empty.

### 02_context/project_context.md

Default structure:

# Project Context

## Project name
## Objective
## Background
## Stakeholders
## Success criteria
## Constraints
## Assumptions
## Dependencies
## Decisions already made
## Open questions

Populate each section using extracted information.

---

### 02_context/requirements.md

Default structure:

# Requirements

## Functional requirements
## Non-functional requirements
## Integrations
## Content inputs
## Acceptance criteria
## Out of scope

Populate each section using extracted information.

---

### 03_planning/scope_summary.md

Default structure:

# Scope Summary

## Included work
## Excluded work
## Deliverables
## Milestones
## Client responsibilities
## Agency responsibilities
## Dependencies

Populate each section using extracted information.

---

### 03_planning/risks.md

Default structure:

# Risks

## Known risks
## Potential risks
## Mitigations
## Open questions

Populate each section using extracted information.

---

### 03_planning/timeline.md

Default structure:

# Timeline

## Target dates
## Milestones
## Dependencies that affect timing
## Risks to schedule
## Open questions

Populate each section using extracted information.

## README creation

Create README.md containing:

# Project Overview

## What this project is
A brief summary derived from source materials.

## Where to find key information
- Project context: 02_context/project_context.md
- Requirements: 02_context/requirements.md
- Scope summary: 03_planning/scope_summary.md
- Risks: 03_planning/risks.md
- Timeline: 03_planning/timeline.md

## Source materials
- Call transcripts: 01_intake/transcripts/
- Associated content: 01_intake/associated_content/

## Initialization record
- Initialization date
- Source files used
- Missing required inputs (if any)

## Validation checklist

Before completion, confirm:

- Folder structure exists
- Source materials are stored
- Core documents are created and populated
- No empty files exist
- Missing information is flagged

## Completion output

Return a confirmation report including:

- Project name
- Created folder structure
- List of generated documents
- List of stored source files
- Missing or unclear information requiring follow-up

## Constraints

- Do not invent requirements or facts
- Do not discard or alter source materials
- Do not overwrite an existing project without confirmation
- Maintain neutrality and fidelity to the provided inputs