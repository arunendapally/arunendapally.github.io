---
name: new-post
description: Write or edit a blog post for this Chirpy Jekyll site. Use when creating a new post in _posts, editing an existing post's front matter, or reaching for a Chirpy feature (prompt callouts, image attributes, code block filenames, embeds, mermaid, math, footnotes). Covers this repo's front matter conventions and the full Chirpy content syntax.
---

# Writing a post for this site

Theme: `jekyll-theme-chirpy` 7.6.0. Official reference: <https://chirpy.cotes.page/posts/write-a-new-post/>

Content quality rules live in [CLAUDE.md](../../../CLAUDE.md). This file is the mechanics.

## File and front matter

Filename: `_posts/YYYY-MM-DD-kebab-case-title.md`

```yaml
---
title: "Post Title in Title Case"
author: arun
date: 2026-08-13 00:00:00 +0000
categories: [AI]
tags: [claude-code, llm, developer-tools]
description: "One or two sentences. Becomes the meta description AND a visible subtitle under the title."
image: /assets/img/posts/post-slug-card.png
mermaid: true # only if the post has a mermaid diagram
---
```

### Repo conventions

| Key | Rule |
|-----|------|
| `author` | Always `arun` (defined in `_data/authors.yml`) |
| `date` | Always `00:00:00 +0000`. Never a `+0530` offset: it can land in the future in UTC and Jekyll silently drops the post |
| `categories` | Reuse existing ones. `[AI]` covers most posts; others in use are `[AI, Developer Tools]` and `[Personal]`. Max two, ordered top then sub |
| `tags` | Lowercase kebab-case, roughly 5 to 10 |
| `image` | Social card at `/assets/img/posts/<slug>-card.png`. In-post screenshots go in `/assets/img/posts/<slug>/` |
| `mermaid` | Required for mermaid to render at all. Easy to forget |
| `pin` | Never use it. The home page stays in reverse date order, newest first. Do not add `pin: true` to any post |

### The description key

Use top-level `description:`, not `seo: description:`.

Chirpy only reads `page.seo.description` for share-button text. The meta description tag and the visible post subtitle both come from `page.description`. With only `seo.description` set, jekyll-seo-tag falls back to the post's first heading, so pages ship with a meta description like `content="The token headache we all have"`.

Verify after building:

```bash
grep -o '<meta name="description"[^>]*>' _site/posts/<slug>/index.html
```

Note that `description:` also renders as visible italic subtitle text under the post title. That is intended Chirpy behaviour, not a side effect to work around.

Optional keys: `toc: false`, `comments: false`, `math: true`, `media_subpath: /assets/img/posts/<slug>/` (prefix for every relative image path in the post, which shortens screenshot-heavy posts).

## Content features

### Prompt callouts

Four types: `tip`, `info`, `warning`, `danger`.

```markdown
> **TL;DR**
>
> - First point
> - Second point
{: .prompt-tip }
```

The TL;DR block at the top of a post is our house pattern. `.prompt-warning` suits honest caveats, `.prompt-info` suits asides.

### Images

```markdown
![Alt text](/assets/img/posts/slug/screenshot.png){: w="700" h="400" }
_Caption text in italics goes right below._
```

Attributes, combinable: `{: w="700" h="400" }` sizes and reserves layout space, `{: .shadow }` adds a drop shadow (good for browser or app screenshots), `{: .normal }` `{: .left }` `{: .right }` control position, `{: .light }` `{: .dark }` show the image in one colour scheme only, `{: lqip="..." }` sets a blur placeholder.

**Always set `w`/`h` on in-post images, to the file's native pixel dimensions.** Read them off the file, do not guess or use a display size.

The theme's CSS is `img { max-width: 100%; height: auto; }`, so a declared 1878px still renders at the content column width (about 680px). Declaring native size changes nothing visually; it just lets the browser reserve the right box before the bytes arrive, which is what kills layout shift. Verify by loading a post and checking that an image's box has its final height while `img.complete` is still false.

Front matter `image:` cards do not need this. Chirpy already injects `width="1200" height="630"` on those.

Setting `w` *below* the column width is a different, deliberate choice: it renders a thumbnail. The lightbox `href` always points at the untouched original, so the full-size view survives. Use it when a screenshot is corroboration rather than something the reader must read.

Every in-post image is automatically wrapped in `<a class="popup">` and picked up by GLightbox (`GLightbox({selector: ".popup"})`), so click-to-zoom already works with no extra markup.

### Code blocks

Add a filename header:

````markdown
```json
{ "model": "claude-opus-5" }
```
{: file=".claude/settings.json" }
````

Hide line numbers on shell snippets and one-liners:

````markdown
```shell
npm run build
```
{: .nolineno }
````

Style a path in prose: `` `/assets/img/posts/`{: .filepath} ``

Escape Liquid so Jekyll does not execute it:

```liquid
{% raw %}{% if page.title %}...{% endif %}{% endraw %}
```

### Embeds

```liquid
{% include embed/youtube.html id='VIDEO_ID' %}
{% include embed/video.html src='/path/clip.mp4' poster='/path/thumb.png' muted=true %}
{% include embed/audio.html src='/path/clip.mp3' %}
```

Platforms: `youtube`, `twitch`, `bilibili`, `spotify`. Video also takes `title`, `autoplay`, `loop`, `types`.

### Mermaid

Needs `mermaid: true` in front matter, then a plain fenced block:

````markdown
```mermaid
graph TD;
  A-->B;
```
````

### Math

Needs `math: true`. Block form needs blank lines around it:

```markdown
$$ E = mc^2 $$
```

Inline form takes no surrounding blank lines. Inside a numbered list, escape the first dollar: `1. \$$ x^2 $$`

### Footnotes

Kramdown handles these, no front matter needed:

```markdown
A claim worth sourcing.[^src]

[^src]: The source, at the bottom of the post.
```

## Before publishing

1. Front matter matches the conventions table, and `description:` is top-level.
2. Run the quality checklist in [CLAUDE.md](../../../CLAUDE.md).
3. Build and check the post appears and the meta description is right:

```bash
bundle exec jekyll build && grep -o '<meta name="description"[^>]*>' _site/posts/<slug>/index.html
```

4. `mermaid: true` present if there is a diagram, `w`/`h` present on every image.
