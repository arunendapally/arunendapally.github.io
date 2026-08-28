---
type: architecture
title: Site Structure
description: How arunendapally.com is assembled from the Chirpy theme gem plus a thin local layer, covering collections, scoped defaults, permalinks, the home and tab pages, and the git-backed last-modified hook.
tags: [jekyll, chirpy, site-structure, collections, permalinks, plugins]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-96432c8187f1a2124a5afef3
    resource: repo://_config.yml
  - id: openwiki-source-c99cee65cc4e942b41954000
    resource: repo://_layouts/post.html
  - id: openwiki-source-57dc109daa6babd441d8b47c
    resource: repo://_plugins/posts-lastmod-hook.rb
  - id: openwiki-source-02c348f8115058b66fa2ba6e
    resource: repo://_tabs/archives.md
  - id: openwiki-source-7b605bf816586d75266b50c5
    resource: repo://_tabs/categories.md
  - id: openwiki-source-98dc15526180334311e4e9bf
    resource: repo://_tabs/tags.md
  - id: openwiki-source-474ec89f2846d7756701923d
    resource: repo://.github/workflows/pages-deploy.yml
  - id: openwiki-source-d5a1739d11bdad59b9de4986
    resource: repo://Gemfile
  - id: openwiki-source-f8d10828394c4129061d5b0e
    resource: repo://index.html
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Site Structure

This repository is the source for a personal technical blog. It is a Jekyll site
that consumes the Chirpy theme as a RubyGem and adds a small layer of local
files on top. Almost everything that renders a page lives inside the gem, not in
this repository.

## The theme is a gem, not a fork

`_config.yml` selects the theme by name and the `Gemfile` pins the version:

- `theme: jekyll-theme-chirpy` (`_config.yml:4`)
- `gem "jekyll-theme-chirpy", "~> 7.6", ">= 7.6.0"` (`Gemfile:5`)

The practical consequence is that the working tree looks almost empty compared
to a typical Jekyll site. There is no `_sass/` of consequence, no `_includes/`
full of partials, no `_layouts/` directory beyond a single file. Jekyll resolves
those from the installed gem at build time, and a file only appears here when it
deliberately overrides or extends the gem's version. The set of files that do
that is small and enumerated on [Theme Overrides and Upgrades](theme-overrides.md).

Upgrading the theme is therefore a `Gemfile` edit and a `bundle update`, not a
merge. Nothing in this repository needs to change for a routine theme release
unless one of the override files diverges.

## What renders

| Path | Role |
|------|------|
| `index.html` | Home page. Front matter only, `layout: home`; the gem supplies the markup |
| `_tabs/*.md` | Sidebar navigation pages: about, archives, categories, tags |
| `_layouts/post.html` | The one layout override, a copy of the gem's post layout |
| `_includes/` | Two files: a newsletter block and a share-links override |
| `assets/css/jekyll-theme-chirpy.scss` | The theme's style entrypoint plus local additions |
| `_plugins/posts-lastmod-hook.rb` | A build-time Ruby hook |
| `_posts/` | Post content, one Markdown file per post |
| `_data/` | Author, share platform, and contact link data |

Three of the four tab pages carry front matter and nothing else. `_tabs/archives.md`,
`_tabs/categories.md`, and `_tabs/tags.md` each set only a layout name, an icon,
and a sort order; the gem's layouts generate the listings. Only `_tabs/about.md`
carries real content.

## Collections and scoped defaults

The site declares one custom collection. `collections.tabs` sets `output: true`
so each tab file becomes a page, and `sort_by: order`, which is what makes the
`order:` key in each tab's front matter drive sidebar sequence (`_config.yml:146-149`).

Two `defaults` blocks then supply front matter that posts and tabs never have to
repeat (`_config.yml:151-167`):

- Posts get `layout: post`, `toc: true`, `comments: false`, and
  `permalink: /posts/:title/`.
- Tabs get `layout: page` and `permalink: /:title/`.

`comments: false` is applied here rather than per post because no comment
provider is configured. Setting a provider under the `comments` key alone would
not enable comments; this default would still switch them off on every post.

The post permalink is deliberately date-free: a post file named
`2026-08-13-some-title.md` publishes at `/posts/some-title/`. Changing this
pattern would break every existing inbound and internal link, which is why the
config marks it as not to be modified.

Two more URL shapes are generated rather than authored. `jekyll-archives` builds
category and tag pages at `/categories/:name/` and `/tags/:name/`
(`_config.yml:190-197`), and the post layout links to them by slugifying and
URL-encoding each category and tag name at render time. The home page paginates
at ten posts (`_config.yml:127`) with an empty `baseurl`, so the site is served
from the domain root.

## The last-modified hook

`_plugins/posts-lastmod-hook.rb` is the only executable code in the site build.
It registers a `:posts, :post_init` hook and, for each post, shells out to git:
if the post's file has more than one commit, it reads the date of the most recent
commit touching that file and assigns it to `post.data['last_modified_at']`
(`_plugins/posts-lastmod-hook.rb:5-13`).

The post layout renders that value as an "Updated" line, but only when it differs
from the publication date, so a post committed once shows a single date. Because
the hook derives its answer from commit history rather than from front matter,
the build environment must have the full history available. A shallow clone would
make every post look unmodified. The CI workflow sets `fetch-depth: 0` for exactly
this reason; see [Build and Deploy](../workflows/build-and-deploy.md).

The commit count threshold of more than one is what distinguishes "created" from
"edited": the commit that introduced the file is the publication, and anything
after it is a modification.

## Where content rules live

Nothing in the layout enforces the front matter a post must carry. Those rules
are documented in `CLAUDE.md` and `.claude/skills/new-post/SKILL.md` and are
described on [Authoring a Post](../workflows/authoring-a-post.md). Two of them
fail silently rather than loudly, so they are worth reading before adding a post.

Site-wide switches, analytics, and the data files behind sharing and contact
links are covered on [Site Configuration](../operations/site-configuration.md).
