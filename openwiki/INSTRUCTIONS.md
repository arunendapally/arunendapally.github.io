# OpenWiki scope brief

## What this repository is

The source for arunendapally.github.io, a personal technical blog. It is a
Jekyll site built on the Chirpy theme (consumed as a gem, not vendored),
deployed to GitHub Pages by GitHub Actions. Alongside the site there is a small
set of Python and shell tooling for publishing: generating social share images,
exporting posts to dev.to, and building LinkedIn banners.

This is a content repository with a thin layer of custom code around a
third-party theme. Document that custom layer. Do not document Chirpy itself.

## Document, in rough order of value

1. **The publishing pipeline.** How a Markdown file in `_posts/` becomes a live
   page: the Actions workflow in `.github/workflows/pages-deploy.yml`, the
   build, and the deploy target.
2. **Post authoring conventions.** The front matter contract this repo enforces
   (the `date` offset rule, `description` vs `seo.description`) and the content
   standards in `CLAUDE.md` and `.claude/skills/new-post/`. These are the rules
   that break the build when violated, so they matter most to a future agent.
3. **Theme overrides.** What this repo changes about stock Chirpy: the layout
   override in `_layouts/post.html`, the includes in `_includes/`, and the
   `_plugins/posts-lastmod-hook.rb` hook. Explain what each one changes and why
   it exists rather than restating its code.
4. **The publishing tools.** `tools/` — what each script produces, what it
   expects as input, and how it is invoked. Group them as one system.
5. **Site configuration.** The parts of `_config.yml` and `_data/` that a
   maintainer actually edits.

## Out of scope

- The Chirpy theme's own internals. It is an external gem.
- Individual blog posts. Their content is not system behaviour. Describe the
  conventions that govern posts, never the substance of any particular one.
- Vendored or generated assets: `_site/`, `assets/js/dist/`, `_sass/vendors/`.
- Anything already excluded by `.openwikiignore`.

## Hard prohibitions

- Never reproduce credentials, tokens, or API keys, even ones that appear to be
  placeholders or examples.
- Never include the author's personal contact details beyond what is already
  published on the site's own about and contact pages.

## Style

Plain, direct language. Match the repository's own voice: no writerly
flourishes, no jargon for its own sake. Prefer a short page that is correct over
a long one that pads. Do not use em-dashes.

Weight pages by what a future agent would need in order to safely add or edit a
post without breaking the build. That is this repository's primary workflow.
