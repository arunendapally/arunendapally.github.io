---
type: quickstart
title: Quickstart
description: Orientation for this blog repository, covering what it is, how the site is assembled, and which wiki page to read for each common task from writing a post to upgrading the theme.
tags: [quickstart, orientation, jekyll, chirpy, blog, task-routing]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-96432c8187f1a2124a5afef3
    resource: repo://_config.yml
  - id: openwiki-source-57dc109daa6babd441d8b47c
    resource: repo://_plugins/posts-lastmod-hook.rb
  - id: openwiki-source-474ec89f2846d7756701923d
    resource: repo://.github/workflows/pages-deploy.yml
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
  - id: openwiki-source-d5a1739d11bdad59b9de4986
    resource: repo://Gemfile
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-8975959e4c3b9c9b2137d33a
    resource: repo://THEME_UPGRADE.md
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Quickstart

This repository is the source for arunendapally.com, a personal technical blog on
software architecture, cloud, and applying AI in engineering. It is a Jekyll site
using the Chirpy theme, deployed to GitHub Pages by GitHub Actions.

## The shape of it in three facts

**The theme is a gem, not a fork.** `_config.yml` names the theme and the
`Gemfile` pins the version. Layouts, includes, and styles live inside the
installed gem, which is why the working tree looks nearly empty. Only a handful
of files override or extend it.

**Most of the repository is content.** `_posts/` holds the posts, `_data/` holds
list content, `_tabs/` holds four navigation pages that are mostly front matter.
The only executable code in the build is a fourteen-line Ruby hook.

**Almost nothing fails loudly.** The rules that matter most on this site are the
ones that produce a successful build and a wrong result: a post that silently
does not publish, a page with the wrong meta description, a diagram that renders
as a code block. Read [Authoring a Post](workflows/authoring-a-post.md) before
touching `_posts/`.

## Where to go

| Task | Page |
|------|------|
| Write or edit a post | [Authoring a Post](workflows/authoring-a-post.md) |
| Run or serve the site locally | [Local Development](operations/local-development.md) |
| Understand what CI does before a deploy | [Build and Deploy](workflows/build-and-deploy.md) |
| Change a site-wide setting, analytics, or a share link | [Site Configuration](operations/site-configuration.md) |
| Understand layouts, permalinks, or the last-modified dates | [Site Structure](architecture/site-structure.md) |
| Upgrade the Chirpy gem without regressions | [Theme Overrides and Upgrades](architecture/theme-overrides.md) |
| Generate a social card, banner, or dev.to export | [Publishing Tools](tools/publishing-tools.md) |

## Getting it running

```shell
bundle install
bundle exec jekyll serve   # http://localhost:4000
```

Ruby 3.1 or newer. `Gemfile.lock` is deliberately not committed, so both local
and CI resolve fresh against the `Gemfile`. On Windows, `--livereload` and
`--detach` do not work and html-proofer cannot run at all, so a clean local build
is not proof that CI will pass. [Local Development](operations/local-development.md)
has the details.

## Two standing rules

Content standards live in `CLAUDE.md` and post mechanics in
`.claude/skills/new-post/SKILL.md`. Both are excluded from the build. Two
constraints from them apply to any change, not just to posts:

- The site runs no ads. There is no AdSense script, ad unit, or `ads.txt`, and
  none is to be added without an explicit request.
- Post voice is plain and direct, and never cites a specific number of years of
  experience.
