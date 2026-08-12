# Theme Sync Audit & Upgrade Roadmap

**Audit date:** 2026-08-12
**Blog theme version:** `jekyll-theme-chirpy` **7.6.0** (from `Gemfile.lock`)
**Upstream checked against:** `cotes2020/jekyll-theme-chirpy` @ `ae677a8` (2026-07-15)

## Verdict

**The blog is already up to date.** It is running the latest released Chirpy version
(7.6.0). The upstream repo HEAD is only 5 bugfix commits past the release — all
unreleased, all confined to gem-internal files, and none of them touch this blog's
override files. **No changes are required right now.**

This document exists so that when the next Chirpy release lands, the update is done
safely without breaking the blog's customizations.

---

## How this blog consumes the theme

The blog is **gem-based**, not a fork:

- `Gemfile` pins `jekyll-theme-chirpy` (`~> 7.6, >= 7.6.0`); theme code ships in the gem.
- `Gemfile.lock` is committed, so local and CI resolve identical versions.
- The blog keeps only **three** local files on top of the theme:

| File | Purpose |
|---|---|
| `assets/css/jekyll-theme-chirpy.scss` | Widens main content to **1600px** (`$main-content-max-width`) + fixes `#back-to-top` position under the wider layout |
| `_includes/post-sharing.html` | Adds a `DESCRIPTION` param to share links (pair with `_data/share.yml`) |
| `_plugins/posts-lastmod-hook.rb` | Sets `last_modified_at` from git history. The gem ships no `_plugins/`, so this is local-only; it needs `fetch-depth: 0` in CI |

## Customization inventory (the regression surface)

These are the only places this blog diverges from stock Chirpy. **Every future upgrade
must preserve all of them:**

1. **`assets/css/jekyll-theme-chirpy.scss`** — `$main-content-max-width: 1600px` and the
   `#back-to-top` `max()` fix. This file is a copy of the theme's entrypoint; if the
   theme's version of it changes structurally on upgrade, merge carefully.
2. **`_includes/post-sharing.html`** — injects `DESCRIPTION` (from page/site description)
   into share links. Upstream 7.6.0 does **not** have this.
3. **`_data/share.yml`** — share links use the `DESCRIPTION` placeholder; LinkedIn enabled.
4. **`_config.yml`** — site title/tagline/url/avatar, GoatCounter analytics, comments
   disabled site-wide, `cdn:` left empty (self-hosted assets), `CLAUDE.md` + `THEME_UPGRADE.md`
   excluded from build.
5. **`.github/workflows/pages-deploy.yml`** — Ruby 3.4, `bundler: default` (do not let it read
   the older `BUNDLED WITH` from `Gemfile.lock`), `fetch-depth: 0` for the lastmod plugin, and
   `html-proofer` (external links off).
6. **`_plugins/posts-lastmod-hook.rb`** — local-only plugin, not part of the gem. Reads git
   history for `last_modified_at`, which is why CI checks out full history.

**Hard rules from `CLAUDE.md`:** no ads. No AdSense, ad units, or `ads.txt` — do not re-add.

## Upstream changes since 7.6.0 (reference only — not to be applied manually)

5 unreleased commits on `cotes2020/jekyll-theme-chirpy` `master` (Jun 29 – Jul 15, 2026).
They will arrive automatically via `bundle update` when the next version releases.
None touch the blog's override files.

| Commit | Fix |
|---|---|
| `01c62bc` | add missing `datetime` attribute on `<time>` element |
| `99614ae` | restore formula overflow scroll for MathJax 4 |
| `3c1f7fa` | truncate overflowed code-block label with ellipsis |
| `453e23d` | add missing comma between viewport meta properties |
| `ae677a8` | add missing space between `lang` and `data-bs-theme` attrs |

Files touched: `_includes/head.html`, `_includes/datetime.html`, `_layouts/default.html`,
`_sass/base/_syntax.scss`, `_javascript/modules/components/locale-datetime.js`,
`assets/js/data/mathjax.js`.

---

## Upgrade roadmap (when a new release ships)

### Phase 0 — Preflight
1. Check the latest released version:
   `gem search "^jekyll-theme-chirpy$" --remote`
2. Read the release notes / diff: https://github.com/cotes2020/jekyll-theme-chirpy/releases
   (or `git -C C:/Code/jekyll-theme-chirpy log --oneline <old-version>..<new-tag>`).
   **Verify:** skim the commit list for any change to `_includes/*`, `_sass/*`,
   `assets/css/*`, or `_config.yml` defaults — those are what can affect overrides.
3. Ensure the working tree is clean and committed (`git status`).

### Phase 1 — Bump the gem
1. Update the constraint in `Gemfile` (e.g. `~> 7.7, >= 7.7.0`).
2. `bundle update jekyll-theme-chirpy`
3. `bundle exec jekyll build`
   **Verify:** build succeeds with no warnings/errors; `Gemfile.lock` shows the new version.

### Phase 2 — Diff the overrides against the new gem
1. `THEME=$(bundle show jekyll-theme-chirpy)`
2. `diff _includes/post-sharing.html "$THEME/_includes/post-sharing.html"`
   **Verify:** the only differences are the blog's `DESCRIPTION` lines. If upstream added
   DESCRIPTION itself, drop the override.
3. `diff assets/css/jekyll-theme-chirpy.scss "$THEME/assets/css/jekyll-theme-chirpy.scss"`
   **Verify:** only the `1600px` + `#back-to-top` additions differ. If upstream restructured
   the file, re-apply the two customizations onto the new base.

### Phase 3 — Diff config defaults
1. `diff _config.yml "$THEME/_config.yml"`
   **Verify:** no new/renamed keys that the blog must adopt (e.g. new theme options).
   Keep all blog-specific values (analytics, comments, cdn, excludes).

### Phase 4 — Local verification
1. `bundle exec jekyll serve` → open http://localhost:4000
   **Check:** widened layout renders, back-to-top button sits in the right margin,
   share links carry a description, code blocks/MathJax render, no broken glyphs.
2. `bundle exec htmlproofer ./_site --disable-external` (matches CI).
   **Note:** this does not run on Windows: html-proofer needs `libcurl`, which the Ruby
   installer does not ship. CI is the only place this step actually executes. Locally,
   check the built `_site` for unresolved internal links, missing `alt` attributes, and
   broken `#` anchors instead.
   **Verify:** zero errors (in CI).

Also note `jekyll serve --livereload` and `--detach` do not work on Windows (eventmachine's
native extension, and `fork`, respectively). Plain `serve` auto-regenerates via polling.

### Phase 5 — Ship
1. Commit (`Gemfile`, `Gemfile.lock`, any override updates).
2. Push — `pages-deploy.yml` builds on Ruby 3.4 and runs html-proofer.
3. Check the live site: layout, back-to-top, share buttons, pageview counter (GoatCounter).

---

## Post-upgrade regression checklist

- [ ] Main content still 1600px max-width on large screens
- [ ] `#back-to-top` not hidden under the scrollbar
- [ ] Share links include the post description (DESCRIPTION token replaced)
- [ ] GoatCounter analytics still fires on production
- [ ] Comments remain disabled
- [ ] No ads / AdSense anywhere
- [ ] `bundle exec htmlproofer ./_site --disable-external` passes
