---
name: Astro Patterns & Standards
description: Conventions and patterns for Astro projects at KED Interests
---

# Astro Patterns & Standards for KED

## Project Structure

```
my-project/
  ├── src/
  │   ├── layouts/          # Page layouts
  │   ├── pages/            # Route pages (.astro, .md)
  │   ├── components/       # Reusable components
  │   │   ├── common/       # Navigation, footer, etc.
  │   │   ├── ui/           # Buttons, cards, forms
  │   │   └── features/     # Feature-specific components
  │   ├── styles/           # Global CSS
  │   └── utils/            # Helper functions, constants
  ├── public/               # Static assets (fonts, icons, etc.)
  ├── astro.config.mjs      # Astro configuration
  ├── tsconfig.json         # TypeScript config
  └── package.json
```

## File Naming

- **Pages:** kebab-case, `.astro` extension (e.g., `contact-form.astro`)
- **Components:** PascalCase, `.astro` extension (e.g., `HeroSection.astro`)
- **Utilities:** camelCase, `.ts` extension (e.g., `formatDate.ts`)
- **Styles:** kebab-case, `.css` extension (e.g., `hero-section.css`)

## Component Patterns

### Astro Components
```astro
---
// Script section: imports, props, logic
import Button from './Button.astro';

interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---

<!-- Template section: HTML/JSX -->
<section class="hero">
  <h1>{title}</h1>
  {description && <p>{description}</p>}
  <Button text="Learn More" />
</section>

<style>
  /* Component styles — scoped by default */
  .hero {
    /* ... */
  }
</style>
```

### Props Convention
- Typed via TypeScript interfaces
- Destructure in the script section
- Document optional props with JSDoc if complex

### Event Handling
- Use `client:*` directives sparingly
- Prefer `client:only` for interactive components
- Use `client:load` only when immediate interactivity is required
- Default to static rendering (no directive) whenever possible

## Styling Standards

### Global Styles
- Define typography, colors, spacing in `src/styles/globals.css`
- Use CSS custom properties (variables) for theming
- Follow mobile-first responsive design

### Component Styles
- Scoped styles in `<style>` tags within `.astro` files
- Use BEM naming convention for class names if needed
- Keep component CSS local; avoid leakage with scoped styles

### No CSS Frameworks by Default
- Write CSS directly (vanilla CSS)
- Use utility classes (like Tailwind) only if justified by analysis
- Keep stylesheet size minimal

## Data & APIs

### Static Data
- Colocate with components or layouts
- Use TypeScript interfaces for type safety
- Keep in `src/utils/` or near the consuming component

### Dynamic Data
- Fetch in component script sections (server-side)
- Cache responses when possible
- Handle errors gracefully with fallbacks

### Content Collections (Markdown)
- Use Astro's content collections API for blog, docs, etc.
- Define schemas in `src/content/config.ts`
- Query with `getCollection()` for type-safe access

## Performance Checklist

Before deploying any Astro site:
- [ ] Images are optimized (use Astro's `<Image />` component)
- [ ] No unnecessary JavaScript shipped to client
- [ ] Fonts are optimized (preload, modern formats)
- [ ] Core Web Vitals are green
- [ ] Mobile performance tested (Chrome DevTools, Lighthouse)
- [ ] 4G load time is < 2 seconds
- [ ] No console errors or warnings

## SEO Standards

- Semantic HTML (proper heading hierarchy, etc.)
- Meta tags in each page (use a `Head.astro` component)
- Open Graph / Twitter card metadata for social sharing
- Sitemap generation (`@astrojs/sitemap`)
- robots.txt configuration
- Canonical URLs where needed

## Deployment Checklist

- [ ] Environment variables configured
- [ ] Staging site tested
- [ ] All links verified
- [ ] Forms tested (if present)
- [ ] Analytics installed and tested
- [ ] Error monitoring configured
- [ ] Backup process documented

---

## Common Gotchas

- **Client directives matter:** `client:load` vs `client:only` changes when JS executes
- **Astro Islands:** Keep interactive islands small and isolated for performance
- **No DOM access in SSR:** Write code that works at build time
- **Asset imports:** Use relative imports in `src/`; public assets use `/` paths
- **Routing is filesystem-based:** File structure = URL structure

---

## Refinement

Update this document as patterns evolve. When a new approach proves effective across projects, document it here.
