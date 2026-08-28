---
type: operations
title: Site Configuration
description: The configuration a maintainer of this blog actually edits, covering identity and SEO keys, analytics, the switches whose empty value silently disables a feature, the build excludes, and the data files behind sharing and contact links.
tags: [configuration, jekyll, seo, analytics, feature-switches, data-files]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-96432c8187f1a2124a5afef3
    resource: repo://_config.yml
  - id: openwiki-source-446798ff9f0e04a0c0fd2045
    resource: repo://_data/authors.yml
  - id: openwiki-source-3c1d386619fcfeec04a46e8d
    resource: repo://_data/contact.yml
  - id: openwiki-source-4ead4106265a34dc2c405641
    resource: repo://_includes/post-sharing.html
  - id: openwiki-source-c99cee65cc4e942b41954000
    resource: repo://_layouts/post.html
  - id: openwiki-source-474ec89f2846d7756701923d
    resource: repo://.github/workflows/pages-deploy.yml
  - id: openwiki-source-4d323772649941a55df7f8cd
    resource: repo://CNAME
  - id: openwiki-source-be7790b7d3a31b5f94b3f3a2
    resource: repo://tools/devto-export.py
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Site Configuration

Nearly all site-level configuration lives in `_config.yml`, with four small data
files under `_data/` supplying list-shaped content. The theme reads all of it;
this repository owns none of the code that consumes it. What follows is the
subset a maintainer changes, and the parts where an empty value means something
specific.

## Identity and SEO

The keys that feed `jekyll-seo-tag` and the Atom feed sit in one block near the
top: `title`, `tagline`, `description`, and `url`. The site description here is
the last fallback for a post's share text and meta description, so it is the
value that appears when a page supplies neither.

`url` is the canonical origin, and it must match the custom domain. The domain
itself is declared in `CNAME` at the repository root, which GitHub Pages reads
directly. Changing one without the other produces a site that serves correctly
but emits absolute URLs pointing somewhere else, and the internal link check will
not catch it because it only inspects relative paths.

`avatar` and `social_preview_image` point at files under `assets/img/`. The
preview image is the site-wide `og:image` and is overridden per post by that
post's `image` front matter key.

`lang: en` and `timezone` complete the block. The timezone governs how post dates
are interpreted, which interacts with the date rule described on
[Authoring a Post](../workflows/authoring-a-post.md).

## Switches that disable rather than error

Several keys are safe to leave blank, and blank is meaningful rather than
broken. Knowing which is the difference between a feature being off and a
feature being misconfigured:

| Key | Empty means |
|-----|-------------|
| `webmaster_verifications.google` / `.bing` | No verification meta tag is rendered at all |
| `comments.provider` | Comments are off; posts also carry `comments: false` from defaults |
| `newsletter.buttondown_user` | The signup block renders nothing |
| `cdn` | Media paths stay site-relative; setting it rewrites every root-relative media URL |
| `theme_mode` | Follow the visitor's system preference and show the light/dark toggle |
| `assets.self_host.enabled` | Falsy; assets are not self-hosted |

The verification keys are the ones to be careful with. They take the `content`
attribute value from a search console's HTML tag method, not the whole tag. They
are absent from this repository's configuration, and there is no reason to
populate them speculatively.

`cdn` is the highest-blast-radius empty value: once assigned, the CDN origin is
prepended to every media resource path starting with `/`, including the avatar
and every post image.

## Analytics and page views

Analytics is GoatCounter, configured by site code under `analytics.goatcounter`,
with `pageviews.provider` set to the same. Those are two separate keys and both
are required: the first loads the tracking script, the second is what makes the
post layout render a view counter. The layout only renders the counter when
`pageviews.provider` is set *and* the matching analytics ID exists, so removing
either one silently drops the counter without breaking the page.

## Rendering and output

`toc: true` is the global switch for the table of contents, reinforced by the
posts `defaults` block. `paginate: 10` sets the home page size. Kramdown is
configured with Rouge highlighting, line numbers on for block code and off for
spans, and a custom footnote backlink glyph. Sass output is compressed, and
`compress_html` strips whitespace and comments in every environment except
development, which is why the served development HTML looks different from
production output.

PWA support is enabled with offline caching, and `pwa.cache.deny_paths` exists
for excluding a path prefix shared with another site on the same domain. It is
empty here.

## The excludes list

`exclude` keeps files out of the built site. Beyond the generic gem patterns, it
names `tools`, `README.md`, `LICENSE`, `CLAUDE.md`, and `THEME_UPGRADE.md`.

This is load-bearing for the publishing tools. The dev.to exporter writes its
converted Markdown into `tools/devto/`, and those files carry YAML front matter.
Without `tools` in this list, Jekyll would treat each one as a page and publish
a duplicate of every exported post. See
[Publishing Tools](../tools/publishing-tools.md).

Adding a new top-level Markdown file that is documentation rather than content
means adding it here too.

## Data files

Four files under `_data/` supply list content the theme iterates over:

- **`authors.yml`** defines the `arun` key that every post's `author` front
  matter refers to. The post layout resolves an author's name and optional URL
  through this file and falls back to the site social name when a post names no
  author. A post naming an author absent from this file renders an empty byline
  rather than failing.
- **`share.yml`** lists the share platforms and their link templates. Four are
  active; the rest are commented out. Its templates use a `DESCRIPTION`
  placeholder that only this repository's sharing override substitutes, so the
  two files are coupled. See [Theme Overrides and Upgrades](../architecture/theme-overrides.md).
- **`contact.yml`** lists sidebar contact links. Entries with no `url` derive it
  from the corresponding `_config.yml` value, which is why the GitHub, Twitter,
  email, and RSS entries carry only a type and an icon while LinkedIn carries an
  explicit URL. Two entries set `noblank: true` to open in the current tab.

## Related

- [Site Structure](../architecture/site-structure.md) for collections, defaults, and permalinks
- [Authoring a Post](../workflows/authoring-a-post.md) for the per-post front matter contract
