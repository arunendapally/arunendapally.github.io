---
type: workflow
title: Authoring a Post
description: The front matter contract and content conventions a post on this blog must satisfy, leading with the two rules that fail silently, plus the Chirpy syntax the repository actually uses and the quality gate applied before publishing.
tags: [authoring, front-matter, chirpy, kramdown, content-standards, workflow]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-96432c8187f1a2124a5afef3
    resource: repo://_config.yml
  - id: openwiki-source-446798ff9f0e04a0c0fd2045
    resource: repo://_data/authors.yml
  - id: openwiki-source-4ead4106265a34dc2c405641
    resource: repo://_includes/post-sharing.html
  - id: openwiki-source-c99cee65cc4e942b41954000
    resource: repo://_layouts/post.html
  - id: openwiki-source-daf87c769767a686ad0a4b82
    resource: repo://.claude/skills/new-post/SKILL.md
  - id: openwiki-source-a2371d6362e5db4bc834ad03
    resource: repo://CLAUDE.md
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Authoring a Post

A post is one Markdown file at `_posts/YYYY-MM-DD-kebab-case-title.md`. The
mechanics are documented in `.claude/skills/new-post/SKILL.md`; the content
standards are in `CLAUDE.md`. This page is the summary and the reasoning.

Start with the two rules that fail silently, because neither produces an error.

## The two silent failures

**The date offset must be `+0000`.** Every post's `date` is written as
`YYYY-MM-DD 00:00:00 +0000`. A `+0530` offset on a midnight date resolves to the
previous evening in UTC, but the more dangerous direction is the other one: an
offset can put the timestamp in the future relative to the build, and Jekyll
silently omits future-dated posts. The build succeeds, the site deploys, and the
post is simply not there. Nothing in the build reports it.

**Use top-level `description:`, not `seo: description:`.** These look
interchangeable and are not. Chirpy reads `page.seo.description` in exactly one
place, the share-link text. The meta description tag and the visible subtitle
under the post title both come from `page.description`. Setting only
`seo.description` leaves `jekyll-seo-tag` to fall back to the post's first
heading, so the page ships with a meta description that is whatever the first
section happened to be called. That is a real published page with wrong metadata,
not a build failure.

Verifying it takes one command after a build:

```shell
grep -o '<meta name="description"[^>]*>' _site/posts/<slug>/index.html
```

Note that `description` also renders as visible italic subtitle text under the
title. That is intended theme behaviour, not a side effect to design around.

## Front matter contract

```yaml
---
title: "Post Title in Title Case"
author: arun
date: 2026-08-13 00:00:00 +0000
categories: [AI]
tags: [claude-code, llm, developer-tools]
description: "One or two sentences."
image: /assets/img/posts/post-slug-card.png
mermaid: true
---
```

| Key | Rule |
|-----|------|
| `author` | Always `arun`, the key defined in `_data/authors.yml` |
| `date` | Always `00:00:00 +0000` |
| `categories` | Reuse existing ones, at most two, ordered top then sub |
| `tags` | Lowercase kebab-case, roughly five to ten |
| `image` | Social card at `/assets/img/posts/<slug>-card.png` |
| `mermaid` | Required for any mermaid diagram to render at all |
| `pin` | Never. The home page stays in reverse date order |

`layout`, `toc`, `comments`, and `permalink` are supplied by the scoped defaults
in `_config.yml` and should not be repeated per post. See
[Site Structure](../architecture/site-structure.md).

`mermaid: true` is the third quiet failure, though a visible one: without it the
diagram renders as an unstyled code block rather than a diagram. It is easy to
forget on a post that gains a diagram during editing.

Optional keys worth knowing: `math: true`, `toc: false`, and `media_subpath`,
which prefixes every relative image path in the post and noticeably shortens a
screenshot-heavy file.

The `image` card itself is generated rather than hand-drawn; see
[Publishing Tools](../tools/publishing-tools.md).

## Content syntax in use

**Prompt callouts.** Four types, `tip`, `info`, `warning`, `danger`, written as a
blockquote followed by a `{: .prompt-* }` attribute line. The house pattern is a
`.prompt-tip` TL;DR block at the top of a post. `.prompt-warning` carries honest
caveats and `.prompt-info` carries asides.

**Images.** Every in-post image carries `w` and `h` set to the file's native
pixel dimensions, read off the file rather than guessed. This does not change how
the image renders: the theme's CSS caps images at the content column width, so a
declared 1878px still displays at roughly 680px. What it does is let the browser
reserve the correct box before the bytes arrive, which is what removes layout
shift. Setting `w` deliberately *below* the column width is a different choice
that renders a thumbnail, and the lightbox link still opens the untouched
original, so use it when a screenshot is corroboration rather than something the
reader must read.

Front matter `image:` cards are exempt, because the theme already injects their
dimensions.

Click-to-zoom needs no markup. Every in-post image is wrapped in a popup anchor
and picked up by GLightbox automatically.

Other combinable attributes: `.shadow` for browser and app screenshots, `.normal`
`.left` `.right` for position, `.light` and `.dark` to show an image in one
colour scheme only, and `lqip` for a blur placeholder.

**Code blocks.** A `{: file="..." }` attribute line after a fence adds a filename
header. `{: .nolineno }` hides line numbers, which suits shell snippets and
one-liners. In prose, `` `path`{: .filepath} `` styles a path. Liquid that should
not execute goes inside a `raw` block.

**Everything else.** Embeds via the theme's `embed/*` includes for YouTube,
video, audio, Twitch, bilibili, and Spotify. Math with `math: true`, needing
blank lines around block form and an escaped first dollar inside a numbered list.
Footnotes work through kramdown with no front matter at all.

## The quality gate

`CLAUDE.md` sets the bar a post clears before it is considered ready. In short: a
minimum of 600 words of original substantive content, no thin intro or
placeholder posts, and no scraped or near-duplicate material. Every post must
answer a real question or teach something concrete, and must contain a concrete
example, code sample, or real-world scenario. Every code sample is tested or
explicitly marked illustrative.

The gate is expressed as questions rather than a checklist, and the first is the
useful one: if you cannot say in a single sentence what the reader walks away
knowing or able to do, the post is not ready.

Two standing constraints apply beyond any single post. The voice is plain and
direct, and never cites a specific number of years of experience. And the site
runs no ads: there is no AdSense script, ad unit, or `ads.txt`, and none is to be
added without an explicit request.

## Before publishing

1. Front matter matches the table above, and `description` is top-level.
2. Run the `CLAUDE.md` quality questions.
3. Build, then grep the built page for its meta description.
4. Confirm `mermaid: true` if there is a diagram, and `w`/`h` on every image.

The link check that CI runs is not available on Windows, so a local build passing
is not the same as CI passing. See [Build and Deploy](build-and-deploy.md).
