# Skill — Code Verification (AI-Generated Code)

This skill runs a three-pass verification sweep on AI-generated code. It is not a general security audit — it is specifically for code that an AI produced, where the AI did not hold a complete mental model of the whole system.

Working code is not ready code. This skill closes the gap.

---

## When to use this skill

Use after any AI-generated code session, scaled to scope:

**Simple snippet (< ~20 lines, no user input, no external calls):**
The security checklist in `skills/scaffold-function/` is sufficient. Skip this skill.

**Function with user input, DB queries, form handling, or API calls:**
Run Pass 1 (Security) and Pass 2 (Optimization). Skip Pass 3.

**Full plugin, multi-file build, or anything with a frontend-to-backend stack:**
Run all three passes. Pass 3 (Traceability) is where AI-generated code breaks most often.

---

## The three passes

### Pass 1 — Security

**Framing matters.** Without adversarial framing, AI tends to trust its own work. Reset that assumption explicitly.

Run this as a sub-agent with the instruction:

> Assume a junior developer wrote this code. Your best security expert is now reviewing it. Go deep. Every input is suspect. Every endpoint needs validation. Every database query should be checked for injection. Categorize all issues as Critical, High, Medium, or Low.

AI-generated code can look clean and professional while hiding real security exposure. The framing shift from "review my code" to "a junior wrote this" is what produces an adversarial review rather than a self-congratulatory one.

---

### Pass 2 — Optimization

Run this as a sub-agent with the instruction:

> Review for code that is never called, functions that do the same thing in slightly different ways across multiple files, implementations that are too verbose or too terse, and performance bottlenecks. Flag dead code, redundant logic, and consolidation opportunities.

AI-generated code has a specific tendency toward duplication. When the AI loses context between files or sessions, it solves the same sub-problem differently in multiple places. A human would notice the utility function already exists. The AI may not.

---

### Pass 3 — Traceability

**Use one sub-agent per layer.** A shallow pass across the whole stack misses the details.

Run with this instruction:

> For every link, button, or form submission in the UI that calls code: verify it calls the right function, passes the right arguments with the right names and types, that those arguments are passed correctly to the next layer, and so on through every layer down to the database query and back up to the response the user sees. Use one sub-agent per layer. Report every mismatch in function names, argument names, argument types, or response shapes between layers.

This is where AI-generated code breaks most often. The AI may generate a frontend that calls `getUserProfile(userId)` and a backend that exposes `get_user_profile(user_id)`. Both work in isolation. Neither works together. These bugs don't show up in a demo — they show up when a real user does something slightly unexpected.

---

## The full prompt (copy-paste ready)

Use this verbatim after code generation is complete:

```
Now I want you to create and use as many sub-agents as makes sense to dig into three areas. You may get away with one sub-agent for each of the first two areas, but you'll need several (one per layer) for the last area.

1. Security — I want you to go deep and do a full and complete security analysis — like a jr developer wrote the code rather than a senior engineer did — and now your best security expert is reviewing and looking for any issues. Categorize them into critical, high, medium and low.

2. Optimization — I want you to go deep and do a full and complete analysis of the code — looking for code that's never called, functions that are replicated in a lot of different places, places where the code could be optimized because it's either too long or too short, performance tweaks and more.

3. Traceability — This is where you'll likely want one sub-agent per layer. I want every link or button in the UI that calls our code, to be reviewed to make sure it actually calls our code. And it calls it with the right signature, passing the right arguments, and that those arguments are the right name / right type. From that layer, to the next, and so on, until you're hitting the database, I want to make sure that we can go from every call to every other call, from one layer to another and then all the way back, without any issues. Functions are called correctly, passed data correctly, and deliver what's expected.

Once you have all of this detail, pull it all together into a report that I will understand, but also that will make it easy for you to create a task markdown artifact that sub-agents can read and pick items to work on from there.
```

---

## Output format

The verification produces two artifacts:

**Human-readable report** — overall state of the codebase, where the risk is, what needs attention first, severity for each issue. This is for Nathan or Chris to review and prioritize.

**Task artifact** — a punch list that sub-agents can work through to remediate. This turns the review into a pipeline: generate → verify → remediate.

---

## Remediation

After reviewing the report, decide what to prioritize. Critical and High issues should be resolved before deployment. Medium issues should be scheduled. Low issues can be tracked.

Feed the task artifact back to the AI with instruction to work through specific items. Do not re-run the full verification prompt — go back to design-time conversation with Claude to understand why the output was wrong, then fix it at the source.

---

## Why this is separate from security-audit

`skills/security-audit/` is for auditing any code — existing, inherited, legacy, or third-party. It applies regardless of how the code was written.

This skill is specifically for AI-generated code, where:
- The AI didn't maintain a complete mental model of the full system
- Seams between pieces are where problems hide
- Code looks clean and professional but may have structural issues invisible on inspection
- The adversarial framing for security is required because the AI trusts its own work by default

---

## Definition of success

This skill succeeds when:

- Security exposures are found before production
- Dead code and duplication are caught before they become maintenance debt
- Layer-to-layer contracts are verified before real users hit broken flows
- The team ships with confidence, not hope
