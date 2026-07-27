# Copilot Instructions - Hugo Noir Portfolio

## Project Overview

This is a **Hugo-based static site generator** for a personal portfolio/blog. It uses the **Hugo Noir** theme (subtheme in `themes/hugo-noir/`) with Tailwind CSS styling. The site is deployed to GitHub Pages at `https://alhussni-aa.github.io/`.

**Key Architecture:**
- **Configuration**: TOML-based (`hugo.toml`) with multilingual support (defaulting to English)
- **Data-Driven Content**: Portfolio data lives in TOML files (`data/en/*.toml`), not markdown
- **Content Pages**: Markdown files in `content/en/` (about, contact, projects, experience, blogs)
- **Theming**: All layouts and partials managed by theme; root `layouts/` folder is empty for customization
- **Styling**: Tailwind CSS with dark mode support (colors defined in `tailwind.config.js`)

## Content Structure & Conventions

### Data Files (Control non-blog content)
- **`data/en/author.toml`**: Author metadata (name, location, bio, social links) - synced with `hugo.toml` params
- **`data/en/tech.toml`**: Skills carousel with devicon icons (rows 1-2)
- **`data/en/experience.toml`**: Work history with role, company, period, responsibilities, technologies
- **`data/en/projects.toml`**: Portfolio projects with title, description, link, image, tech stack
- **`data/en/blogs.toml`**: Blog metadata (if needed for special handling)

### Content Pages (Markdown in `content/en/`)
- `_index.md` - Homepage (minimal front matter)
- `about.md`, `contact.md`, `projects.md`, `experience.md` - Static pages
- `blogs/_index.md` - Blog listing page
- Individual blog posts in `blogs/` with front matter: `title`, `date`, `draft`, `tags`, `categories`, `description`

### Key Pattern
**Data vs. Content**: Use TOML files for structured, reusable data (experience, projects, tech). Use markdown for narrative content (blog posts, page copy).

## Build & Development Workflows

```bash
npm install      # Install Tailwind dependencies (required after cloning)
hugo server      # Start dev server at http://localhost:1313
npm run build    # Build CSS with PostCSS/Tailwind (if needed)
```

Hugo automatically generates the `public/` folder (git-ignored). The theme's watch system recompiles on content changes.

## Theme Customization Rules

1. **DO NOT edit theme files** (`themes/hugo-noir/`). Instead:
   - Override by creating matching files in root `layouts/` directory
   - Example: Create `layouts/partials/header.html` to override theme's header

2. **Dark Mode Classes**: Uses Tailwind's `dark:` prefix
   - Colors in Tailwind config: `bg-primary-light`, `text-primary-dark`, `border-primary-light`, `accent-light`, etc.
   - Theme defaults to light mode; user can toggle via class on root element

3. **Devicon Icons**: Tech stack and project icons use devicon CDN
   - Format: `devicon-{tool}-{variant}` (e.g., `devicon-python-plain`, `devicon-react-original`)
   - Reference: https://devicon.dev/

## Configuration Management

- **`hugo.toml`**: Master config with site title, base URL, language settings, menu structure, security rules
- **Menu Structure**: Defined in `[languages.en.menu.main]` with `pageRef` and `weight` (1=top, 5=bottom)
- **Social Links**: Both in `hugo.toml` params AND `data/en/author.toml` (keep synchronized)
- **URLs**: Using `relativeURLs = true` and `canonifyURLs = true` for GitHub Pages compatibility

## Template Variables & Data Access

In theme templates:
```hugo
{{ $authorData := index site.Data .Language.Lang "author" }}
{{ $author := cond (and $authorData $authorData.author) $authorData.author site.Params }}
{{ with $author }}...{{ .name }}, {{ .location }}...{{ end }}
```

This pattern checks for author data in TOML, falls back to `hugo.toml` params. Always use this pattern when referencing author info.

## Common Tasks for AI Agents

- **Add blog post**: Create `.md` file in `content/en/blogs/` with front matter
- **Update tech skills**: Edit rows in `data/en/tech.toml` with new devicon entries
- **Add experience/project**: Add `[[experience]]` or `[[projects]]` block in corresponding TOML file
- **Update homepage**: Edit `content/en/_index.md` or theme's `layouts/index.html` (by overriding in root `layouts/`)
- **Change colors/styling**: Update `tailwind.config.js` theme colors or override in custom Tailwind directives

## Security & Build Context

- Hugo execution restricted to npm/npx/tailwindcss commands in `[security.exec]`
- PostCSS/Tailwind configured for CSS processing
- No database, no backend—purely static generation
