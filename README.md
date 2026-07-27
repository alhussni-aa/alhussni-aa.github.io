# alhussni-aa.github.io

Personal portfolio site for Abdullah Alhussni.

**Live:** [alhussni-aa.github.io](https://alhussni-aa.github.io/)

Built with [Hugo](https://gohugo.io/) and the [hugo-noir](https://github.com/prxshetty/hugo-noir) theme. Deployed via GitHub Actions to GitHub Pages.

## Local Development

### Prerequisites

- [Hugo](https://gohugo.io/installation/) extended v0.154.5+

### Setup

```bash
git clone --recurse-submodules https://github.com/alhussni-aa/alhussni-aa.github.io.git
cd alhussni-aa.github.io
hugo server
```

The site will be available at `http://localhost:1313/`.

The `--recurse-submodules` flag is required to pull the `hugo-noir` theme. If you already cloned without it, run:

```bash
git submodule update --init --recursive
```

### Build

```bash
hugo --gc --minify
```

Output goes to `public/`.

## Deployment

Pushes to `master` trigger the GitHub Actions workflow (`.github/workflows/hugo.yml`), which builds with Hugo extended v0.154.5 and deploys to GitHub Pages.
