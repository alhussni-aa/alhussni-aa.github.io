# Personalization Guide

Your Hugo Noir theme is ready! Here's what you need to customize:

## 1. **Main Configuration** → [hugo.toml](hugo.toml)
Update these sections with your info:
- `title` = Your site title
- `[params]` section:
  - `name` = Your name
  - `location` = Your location
  - `description` = Your bio
  - `github`, `linkedin`, `twitter`, `email` = Your social links
  - `profile_image` = Path to your profile photo

## 2. **Author Data** → [data/en/author.toml](data/en/author.toml)
Same info as params, but used in specific sections.

## 3. **Tech Stack** → [data/en/tech.toml](data/en/tech.toml)
- Update `row1` and `row2` arrays with your skills
- Icons from [devicon.dev](https://devicon.dev/)
- Example: `{ icon = "devicon-python-plain", name = "Python" }`

## 4. **Experience** → [data/en/experience.toml](data/en/experience.toml)
Add your work history:
```toml
[[experience]]
role = "Job Title"
company = "Company Name"
company_link = "https://company.com"
period = "Jan 2020 - Present"
country = "Country"
responsibilities = ["task1", "task2"]
technologies = ["Tech1", "Tech2"]
```

## 5. **Projects** → [data/en/projects.toml](data/en/projects.toml)
Add your portfolio projects with title, description, link, image, and technologies.

## 6. **Content Pages**
Edit these markdown files in [content/en/](content/en/):
- `_index.md` - Homepage
- `about.md` - About page
- `contact.md` - Contact page
- `projects.md` - Projects page
- `experience.md` - Experience page
- `blogs/_index.md` - Blog index

## 7. **Blog Posts**
Create markdown files in [content/en/blogs/](content/en/blogs/):
```markdown
---
title: "My First Post"
date: 2024-01-19T10:30:00
draft: false
tags: ["tag1", "tag2"]
categories: ["category"]
description: "Brief post description"
---

Your blog content here...
```

## 8. **Profile Image**
Place your profile photo at [static/images/profile.jpg](static/images/profile.jpg)

## Running the Site
```bash
npm install  # If cloning elsewhere, run this first
hugo server  # Start development server at http://localhost:1313
```

## Notes
- All files use TOML, YAML, or Markdown format
- The theme supports multilingual setup (English, Spanish, French by default)
- To add more languages, duplicate the `[languages.en]` section in hugo.toml and create corresponding data/content directories
- The site builds to `/public` folder (git-ignored)

Happy personalizing! 🎉
