---
type: architecture
title: Theme Overrides and Upgrades
description: The complete set of files in this repository that diverge from stock Chirpy, why each exists, and the procedure for upgrading the theme gem without losing any of them.
tags: [chirpy, theme, overrides, upgrade, regression-surface, scss]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-96432c8187f1a2124a5afef3
    resource: repo://_config.yml
  - id: openwiki-source-1b6734dd426675c67f2f0ac5
    resource: repo://_data/share.yml
  - id: openwiki-source-facda3741992028adb5ac12a
    resource: repo://_includes/newsletter.html
  - id: openwiki-source-4ead4106265a34dc2c405641
    resource: repo://_includes/post-sharing.html
  - id: openwiki-source-c99cee65cc4e942b41954000
    resource: repo://_layouts/post.html
  - id: openwiki-source-6ba48363e91928fc0523e8d4
    resource: repo://assets/css/jekyll-theme-chirpy.scss
  - id: openwiki-source-8975959e4c3b9c9b2137d33a
    resource: repo://THEME_UPGRADE.md
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Theme Overrides and Upgrades

The site runs Chirpy from a gem, so the working tree holds only the files that
deliberately change or extend it. That small set is the entire regression
surface of a theme upgrade. If an upgrade breaks something, it breaks here.

## The override set

| File | What it changes | Why |
|------|-----------------|-----|
| `assets/css/jekyll-theme-chirpy.scss` | Widens content to 1600px, repositions the back-to-top button, styles the newsletter block | The theme's style entrypoint, copied so the Sass variable can be overridden at `@use` time |
| `_layouts/post.html` | Adds `newsletter` to `tail_includes` | Layouts cannot be partially patched, so the whole file is copied |
| `_includes/post-sharing.html` | Passes a description into share links | Upstream 7.6.0 sends only title and URL |
| `_includes/newsletter.html` | New signup block | An addition, not an override; the gem has no equivalent |
| `_plugins/posts-lastmod-hook.rb` | Sets `last_modified_at` from git history | The gem ships no `_plugins/` directory at all |
| `_data/share.yml` | Enables platforms, uses the `DESCRIPTION` token | Paired with the sharing override |

## Why each one exists

**The stylesheet.** Chirpy's entrypoint is a Sass file that configures the
theme's variables module and then imports `main`. Overriding a Sass variable
requires passing it at `@use` time, which means owning the entrypoint file. This
copy sets `$main-content-max-width: 1600px`, and switches between the plain and
bundled `main` depending on the Jekyll environment.

Widening the content column has a knock-on effect. Chirpy positions the
back-to-top button by centring it in the margin left over after the sidebar and
content column, using a `calc()` expression built from those two widths. At
1600px of content plus a 300px sidebar, that expression goes negative between the
1650px breakpoint and roughly 1900px of viewport, and the button lands under the
scrollbar. The fix floors the value at `2rem` with a CSS `max()`, interpolated as
a string so Sass emits the function rather than trying to evaluate it at compile
time. The original `calc()` still wins on genuinely ultra-wide screens.

**The post layout.** This is the highest-risk override, because it is a verbatim
copy of the gem's layout rather than a patch, and its only intentional difference
is one line: `newsletter` at the head of `tail_includes`. Every other change the
theme makes to that layout, and there are many across releases, is silently
frozen at the version copied. A stale copy does not fail the build; it just stops
receiving upstream fixes. On upgrade, prefer replacing the file with the new gem
layout and re-adding that one line over diffing and patching the old copy.

**The sharing include.** Stock Chirpy substitutes only `TITLE` and `URL` into
each share link. This override adds a third substitution, resolving a description
from `page.seo.description`, then `page.description`, then the site description,
and replacing a `DESCRIPTION` token. The tokens it fills in live in
`_data/share.yml`, so the two files must be changed together: enabling a new
platform there with a `DESCRIPTION` placeholder works only because this include
substitutes it.

This is also the one place `seo.description` is read. Everywhere else, including
the meta description tag and the visible post subtitle, the top-level
`description` key is what matters. That distinction causes a specific silent
failure documented on [Authoring a Post](../workflows/authoring-a-post.md).

**The newsletter block.** A new include, gated on `site.newsletter.buttondown_user`.
When that key is empty the whole block renders nothing, so the feature ships in
the off position and is enabled by filling in one config value. Its styles live
in the stylesheet override, inheriting Chirpy's card background and shadow so
only the form row needs rules. One of those rules is deliberate: the email input
borrows Bootstrap's `--bs-border-color` rather than Chirpy's
`--main-border-color`, because the latter is near-white in light mode and would
disappear against the card.

**The last-modified plugin.** Covered on
[Site Structure](site-structure.md). It is local-only, and its dependence on git
history is what forces the CI checkout to fetch everything.

## Upgrading the theme

`THEME_UPGRADE.md` holds the full procedure and a post-upgrade regression
checklist. The shape of it:

1. **Preflight.** Check the latest released version, read the release notes, and
   skim the commit list specifically for changes to `_includes/*`, `_sass/*`,
   `assets/css/*`, or `_config.yml` defaults. Those are the only upstream areas
   that can collide with an override. Start from a clean working tree.
2. **Bump.** Edit the version constraint in the `Gemfile`, run
   `bundle update jekyll-theme-chirpy`, and build.
3. **Diff the overrides** against the new gem, using `bundle show
   jekyll-theme-chirpy` to locate it. Each diff has an expected shape: only the
   `DESCRIPTION` lines in the sharing include, only the width, back-to-top, and
   newsletter additions in the stylesheet, only the `newsletter` line in the post
   layout. Anything else means upstream restructured the file and the
   customization has to be re-applied onto the new base.
4. **Diff `_config.yml`** for new or renamed theme keys worth adopting, keeping
   all site-specific values.
5. **Verify locally**, then ship. Note that html-proofer cannot run on Windows,
   so CI is the only place the link check actually executes; see
   [Local Development](../operations/local-development.md).

If upstream ever adds a feature an override was working around, the right move is
to delete the override rather than keep carrying it. The sharing include is the
likeliest candidate.

## Related

- [Site Structure](site-structure.md) for how the gem and the local layer combine
- [Site Configuration](../operations/site-configuration.md) for the switches these overrides read
