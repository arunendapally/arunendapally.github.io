---
type: tooling
title: Publishing Tools
description: The four Python scripts that produce artefacts around a post, covering the social preview cards, the LinkedIn banner, framed phone screenshots, and the dev.to export, including what each expects and where each writes.
tags: [tooling, python, pillow, social-cards, devto, cross-posting]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-96432c8187f1a2124a5afef3
    resource: repo://_config.yml
  - id: openwiki-source-daf87c769767a686ad0a4b82
    resource: repo://.claude/skills/new-post/SKILL.md
  - id: openwiki-source-be7790b7d3a31b5f94b3f3a2
    resource: repo://tools/devto-export.py
  - id: openwiki-source-23b6131f6d7612d29001e146
    resource: repo://tools/linkedin-banner.py
  - id: openwiki-source-0fe623489d191a19d11d5986
    resource: repo://tools/og-card.py
  - id: openwiki-source-8d5476bb066e2112cf6999b1
    resource: repo://tools/social-image.py
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Publishing Tools

`tools/` holds four standalone Python scripts. None of them runs during the site
build, and `tools` is in the config's `exclude` list so nothing here reaches the
published site. Each is run by hand when a post needs an artefact.

Three of them draw images with Pillow and share one visual language; the fourth
converts a post for cross-posting. They have no shared module, no package, and no
dependency file: each is a single script that imports Pillow directly.

## The shared card language

`og-card.py`, `linkedin-banner.py`, and `social-image.py` all use the same
background colour, `#1a1a1a`. The two drawing scripts also share the accent
orange `#e87647`, Roboto Bold over grey Roboto Regular, and the same furniture:
a title, a subtitle, tag pills, the domain, and an accent bar along the bottom.
`linkedin-banner.py` says outright that it reuses `og-card.py`'s palette and
layout vocabulary. That consistency is the point, so a change to one palette
should be mirrored rather than left to drift.

The two drawing scripts read Roboto from a hardcoded Windows font directory,
`C:/Windows/Fonts/`. Only `linkedin-banner.py` handles the absence of those
files: it wraps each `truetype` call and falls back to DejaVu at a Linux system
path. `og-card.py` has no fallback and will raise on any machine without Roboto
installed at that exact path. Neither script would work unchanged in CI on Linux
without Roboto present, and only the banner would degrade gracefully.

### `og-card.py`

Generates the 1200x630 social preview card for a post. Card definitions live in a
dictionary in the script keyed by output name, each holding a title, a subtitle,
and a tag list. Running it with no arguments regenerates every card; naming one
or more keys regenerates just those. Output goes to `assets/img/posts/<name>.png`,
which is where a post's `image` front matter key points.

The layout deliberately fails loudly rather than producing a bad card. The title
is greedy-wrapped to at most two lines and the wrapper raises if the text will
not fit; the subtitle raises if it is wider than the text column. Rather than
shrinking type or overflowing, the script tells you the copy is too long.

Two layout choices are worth preserving if it is edited. The title block grows
upward from a fixed subtitle position, so one-line and two-line titles leave the
same gap above the pill. The tag pill is anchored to the bottom of the card
rather than to the title, for the same reason.

### `linkedin-banner.py`

Generates the LinkedIn profile cover at 1584x396. Two differences from the card
script drive its structure.

First, it renders at three times the logical size. LinkedIn paints the cover on
high-DPI screens at two to three times its logical dimensions and re-encodes what
it is given, so a 1x render arrives upscaled and soft. Text shows that; photos
hide it. Every dimension in the script is authored in 1x units and multiplied by
a scale factor, so the upload has pixels to spare and LinkedIn only ever
downsamples.

Second, all content starts well right of the usual margin, because LinkedIn
overlays the profile photo across the bottom-left of the cover. The safe left
edge is a named constant.

Where the card carries one pill, the banner carries a tiered skill block: filled
pills for headline skills, orange outlines for supporting ones, muted outlines
for the stack. A greedy packer fills rows to a target width so the block reads as
a designed group rather than a word cloud, and each row is vertically centred on
its tallest pill. Like the card script, it raises rather than overflow when the
title or subtitle is too wide.

A light variant is defined by copying the dark banner's content and switching
themes. The light palette darkens the accent deliberately, because the card
orange does not carry enough contrast on white. Output goes to
`assets/img/<name>.png`.

### `social-image.py`

Frames a phone screenshot for LinkedIn. LinkedIn shows portrait images at 4:5 at
most, so a 1080x2400 capture at 0.45 gets cropped or shrunk with padding. The
script crops away the OS status and navigation bars using top and bottom pixel
offsets, then widens the canvas in the shared background colour until the aspect
ratio reaches 4:5 and centres the image on it.

Letterboxing rather than cropping is the deliberate choice: nothing is lost from
the screenshot, and trimming the status bar means no notification icons ship in a
public image. The result is resized to 1080 wide with Lanczos resampling. Input,
output, and the two crop offsets are positional arguments, with the offsets
defaulting to values suited to a 2400px-tall capture.

## `devto-export.py`

Converts a post in `_posts/` into Markdown ready to paste into the dev.to editor,
writing to `tools/devto/<slug-without-date>.md`. It is the reason `tools` must
stay in the build excludes: the output carries YAML front matter, so Jekyll would
otherwise publish each export as a duplicate page.

The conversions exist because Chirpy's kramdown extensions mean nothing on
dev.to:

- **Attribute blocks** (`{: .prompt-tip }`, image sizing, `.nolineno`) would
  render as literal text, so they are stripped. The one exception is a code
  block's `file="..."` label, which is not dropped but moved: dev.to has no
  equivalent, so the filename is inserted as bold text immediately above the
  block it labelled.
- **Relative paths** would resolve against dev.to's own domain and 404, so
  `/assets/` and `/posts/` links are rewritten to absolute URLs on the blog.
- **Mermaid blocks** are not rendered by dev.to. Rather than drop them, the
  script keeps the source and inserts a line above it linking to the rendered
  diagram on the canonical post.

Fence tracking is what makes the attribute stripping safe. The converter tracks
whether it is inside a fenced block and passes those lines through untouched, so
an attribute-looking line inside a code sample survives.

The emitted front matter is dev.to's, not Chirpy's: title, description, tags,
`canonical_url` pointing back at the blog post, and a `cover_image` absolutised
from the post's `image` key when present. Titles and descriptions are always
quoted, because they routinely contain a colon followed by a space, which is a
YAML parse error unquoted.

Two constraints are encoded in the script's post table. `published: false` is
always emitted, so an export lands as a dev.to draft and is never published by
accident. And the tag list is per-post configuration rather than a reuse of the
post's own tags, because dev.to allows at most four tags and requires them to be
alphanumeric.

## Related

- [Authoring a Post](../workflows/authoring-a-post.md) for the front matter these read
- [Site Configuration](../operations/site-configuration.md) for the excludes list that keeps `tools/` unpublished
