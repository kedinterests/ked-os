---
name: KED Technology Stack
description: Technologies, frameworks, and tools used in KED Interests projects
---

# KED Technology Stack

## Primary Platforms

### Astro
- Modern static site generator for marketing sites, docs, content platforms
- Fast performance, great SEO, minimal JavaScript shipped to client
- Use for: company sites, client portals, content-heavy projects, documentation
- Integrations: Discourse (for comments), custom APIs

### Discourse
- Community forum and discussion platform
- Full-featured, self-hosted control, customizable
- Use for: client communities, knowledge bases, discussion forums
- SSO integration possible for multi-platform experiences

### Vibe
- Hand-coded custom web sites
- Built to precise specifications and design
- Use for: unique, branded experiences that need pixel-perfect control
- Higher development cost, higher control

## Supporting Technologies

### Frontend
- **Language:** JavaScript / TypeScript
- **Runtime:** Node.js 18+
- **Package manager:** npm
- **No jQuery** unless explicitly required for legacy support
- **CSS:** Standard CSS, no preprocessors unless required
- **Templating:** Astro's `.astro` format (preferred), or standalone JS/TS

### Backend & Data
- **APIs:** RESTful, GraphQL if warranted
- **Databases:** Case-by-case (no default prescribed)
- **Authentication:** SSO, OAuth, custom as needed
- **Hosting:** Deployment case-by-case

### Development Tools
- Git for version control
- GitHub for repositories (kedinterests org)
- npm for package management
- Standard Node.js tooling (nodemon, etc.)

## Anti-Patterns

**No WordPress** — ever. KED rejects WordPress in favor of Astro, Discourse, and hand-coded solutions.

**No PHP** (except when strictly required for legacy or third-party integration).

**No jQuery** as default. Vanilla JS or Astro components preferred.

**No CSS frameworks** as default. Write standard CSS, use utility classes if performance analysis justifies it.

## Performance Standards

All KED projects must:
- Load in < 2 seconds on 4G
- Achieve Core Web Vitals: green across all metrics
- Serve only necessary JavaScript (code split if > 50KB)
- Optimize images, use modern formats (WebP)
- Test on real devices before deployment

## Security Standards

- HTTPS everywhere
- No sensitive data in client-side code
- Validate all user input
- Sanitize user-generated content
- Keep dependencies updated
- Conduct security audits per `skills/security-audit/`

---

## Deployment & Environment

- **Staging:** Accessible, full feature parity with production
- **Production:** Stable, monitored, documented deployment process
- **Monitoring:** Error tracking, performance monitoring, uptime monitoring
- **Backups:** All critical data backed up, restore tested

---

## Adding to the Stack

New tools or technologies must:
1. Solve a real problem in current projects
2. Have community support and longevity
3. Not contradict the KED philosophy (fast, modern, performant, specialized)
4. Be approved by Kenny and Chris before adoption
5. Be documented here before use

Update this file whenever the stack changes.
