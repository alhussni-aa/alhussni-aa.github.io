# Agent Context — alhussni-aa.github.io

## Project Overview

Personal portfolio site for Abdullah Alhussni, built with Hugo + the `hugo-noir` theme (git submodule). Deployed to GitHub Pages at `https://alhussni-aa.github.io/`.

## Hard Rules

- **NEVER modify files under `themes/hugo-noir/`** — use Hugo layout overrides in `layouts/`
- GitHub repos are fetched **client-side via JS** (not build-time, not static TOML data)
- Altium Designer and Cadence Virtuoso use **custom SVG images** (Devicon has no icons for them)
- Primary email: `aa10108@nyu.edu` (same as `abdullah.alhussni@nyu.edu`); personal: `alhussni.aa@gmail.com`
- GPA is **3.641** (not 3.74)
- Leadership is a **separate page** from Experience — has its own template + data file
- Motto/description: **"Wannabe polymath. Full-time caffeinator."**
- Only 5 public repos in GitHub section (skip homework forks)
- CppCheckers is **commented out** in projects.toml per user request

## Architecture

```
hugo.toml                    # Master config: site params, nav menu, social links
data/en/
  author.toml                # Author bio, social links, honors[], certifications[], voluntary[]
  experience.toml            # 6 entries: NYUAD, Gelfand, NYU Admissions, Weyak, CQTS, Physics Olympiad
  leadership.toml            # 7 entries: MSA, ASA, Al-Diwan, SYE, Al Muntaha, Paper Airplanes
  projects.toml              # 1 featured (Hisham FC w/ image) + 2 public + 12 private (text-only cards) + 1 commented out
  github.toml                # username + 5 repo names (fetched client-side)
  tech.toml                  # Skills carousel rows, includes custom SVG icons
  blogs.toml                 # Blog metadata
content/en/
  _index.md                  # Homepage
  about.md                   # Bio, capstone, research, coursework
  experience.md              # Stub for experience page
  leadership.md              # Stub for leadership page
  projects.md                # Stub for projects page
  contact.md                 # Contact page
  blogs/                     # Blog posts (markdown)
layouts/
  index.html                 # Homepage override (carousel SVG fix, GitHub preview, dark mode CSS, experience expand/collapse)
  _default/projects.html     # Projects override (featured cards + public cards + private text cards + GitHub JS fetch)
  _default/leadership.html   # Custom leadership timeline template with expand/collapse
  _default/experience.html   # Custom experience timeline (no stat boxes) with expand/collapse
  _default/contact.html      # Custom contact page with 11 icon cards (3 emails, 2 phones, 6 socials) from author.toml
static/images/icons/
  altium-designer.svg        # Custom icon, viewBox cropped to "5 66 180 59"
  cadence.svg                # Custom icon, viewBox cropped to "32 68 153 61"
.github/workflows/hugo.yml   # GitHub Actions: Hugo build + Pages deploy on push to master
```

## Data File Schemas

### experience.toml
```toml
[[experience]]
role = "..."
company = "..."
company_link = "..."
period = "..."
country = "..."
responsibilities = ["...", "..."]
technologies = ["...", "..."]
```

### leadership.toml
```toml
[[leadership]]
role = "..."
organization = "..."
organization_link = "..."
period = "..."
responsibilities = ["...", "..."]
```

### projects.toml
```toml
[[projects]]
title = "..."
description = "..."
link = ""           # empty for private
image = ""          # empty = compact text card; non-empty = full image card
tech = "Python, MATLAB"
private = true      # optional flag
```

### github.toml
```toml
username = "alhussni-aa"
repos = ["repo-name-1", "repo-name-2"]
```

### author.toml (arrays)
```toml
[[honors]]
institution = "..."
title = "..."
date = "..."

[[certifications]]
title = "..."
url = "..."
date = "..."

[[voluntary]]
organization = "..."
url = "..."
role = "..."
period = "..."
description = "..."
```

## Known Gotchas

1. **TOML structure**: Scalar keys (like `github_username`) and `[[array]]` tables in the same file causes Hugo to not expose scalars at root level. Keep them in separate files (hence `github.toml` is separate from `projects.toml`).
2. **Template context**: Inside `{{ with ... }}` or `{{ range ... }}` blocks, `.Language.Lang` fails because `.` is rebound. Use `$.Language.Lang` to access page context.
3. **SVG carousel**: Custom SVG icons use `width: auto; height: 2.25rem; max-width: 6rem;` in CSS to handle non-square viewBoxes (Altium/Cadence are ~3:1 aspect ratio).
4. **Theme @apply bug**: The theme's original `projects.html` uses `@apply` in a `<style>` block which may not work without PostCSS. Our override avoids this by using inline Tailwind classes.
5. **Layout front matter required**: Hugo pages in `content/en/` need explicit `layout: "name"` in front matter to use custom layout overrides in `layouts/_default/`. Without it, Hugo falls back to the theme's default single template.

## Deployment

- GitHub Actions workflow (`.github/workflows/hugo.yml`) triggers on push to `master`
- Builds with Hugo extended v0.154.5, deploys via `actions/deploy-pages`
- Requires Pages source set to "GitHub Actions" in repo settings (Settings > Pages > Source)

## Progress / What's Done

- [x] Full resume data populated (experience, leadership, about, honors, certs, volunteering)
- [x] Projects page: featured image cards + private text-only cards + GitHub API fetch
- [x] Leadership page with custom timeline template + expand/collapse toggle
- [x] Experience page with custom timeline template (no stat boxes) + expand/collapse toggle
- [x] Contact page with 11 icon cards (3 emails, 2 phones, 6 socials) from author.toml
- [x] Nav menu with all 6 sections (About, Experience, Leadership, Projects, Blog, Contact)
- [x] Altium/Cadence Virtuoso custom SVG icons with cropped viewBoxes
- [x] Dark mode CSS fix for custom SVG icons (`filter: invert(1)`)
- [x] GitHub Actions workflow for Hugo + Pages deployment
- [x] Cleaned stale `themes/aafu` submodule reference
- [x] Deleted old forked repo, created fresh repo, pushed to master
- [x] GitHub Pages live at https://alhussni-aa.github.io/
- [x] Deleted 10 sample blog posts (only `_index.md` remains + `_template.md` draft for future posts)
- [x] All data files rewritten to match actual resume (experience, leadership, author, projects, about)
- [x] Layout front matter added to projects.md, leadership.md, contact.md
- [x] Experience & leadership templates render bullet points (list-disc)
- [x] Projects ordered: featured → public → private
- [x] Stack Exchange network profile link (replaces Stack Overflow)
- [x] Projects template three-way split: featured (image) / public (link, no image) / private (no link)
- [x] Leadership links fixed: removed wrong MSA/ASA/Al-Diwan links, added SYE + Al Muntaha links, fixed Paper Airplanes URL
- [x] Stack Exchange URL corrected to network profile with username
- [x] Homepage experience section: expand/collapse dropdowns with responsibilities bullets (collapsed by default)
- [ ] Screenshots for 5 private projects (user will provide later)
