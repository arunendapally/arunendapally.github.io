# arunendapally.com

Source for [arunendapally.com](https://arunendapally.com) — a technical blog on software architecture, cloud, and applying AI in engineering. Built with [Jekyll](https://jekyllrb.com/) and the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme.

## Local development

Requires Ruby 3.1+ and Bundler.

```shell
bundle install   # resolves deps from the Gemfile
bundle exec jekyll serve   # http://localhost:4000
```

`Gemfile.lock` is **not** committed. A lock generated on Windows pins mingw-only builds of
`google-protobuf` and `sass-embedded`, which the Linux CI runner cannot install; regenerating
it on Windows pulls gem versions (`json`) that fail to build locally. CI resolves fresh
against the `Gemfile`, which is why `jekyll-theme-chirpy` carries an explicit version
constraint there.

`--livereload` and `--detach` do not work on Windows: the first needs eventmachine's
native extension, the second needs `fork`. Plain `serve` still rebuilds on save, so
just reload the browser.

## Verification

- **Build**: `bundle exec jekyll build`
- **CI**: `.github/workflows/pages-deploy.yml` builds on Ruby 3.4, then runs `html-proofer` (external links disabled) on the `_site` output.

## Intentional customizations (re-diff when upgrading the Chirpy theme)

- `assets/css/jekyll-theme-chirpy.scss` — widens content to 1600px and fixes the back-to-top button position.
- `_includes/post-sharing.html` — adds the post's SEO description to share links.
- `_plugins/posts-lastmod-hook.rb` — the Chirpy last-modified plugin (from the starter). It needs `fetch-depth: 0` in CI, which the workflow sets.

## Deploy

GitHub Pages via the `pages-deploy` workflow on `main` (Source: GitHub Actions).

## License

Blog content © Arun Endapally. Theme under [MIT](https://github.com/cotes2020/jekyll-theme-chirpy/blob/master/LICENSE).
