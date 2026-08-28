---
type: workflow
title: Build and Deploy
description: How a commit on this blog becomes a live page, covering the GitHub Actions pipeline, the html-proofer gate, the build and deploy job split that lets pull requests be tested without shipping, and the concurrency and permission model.
tags: [ci, github-actions, github-pages, deployment, html-proofer, jekyll]
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
  - id: openwiki-source-4d323772649941a55df7f8cd
    resource: repo://CNAME
  - id: openwiki-source-672762f087717abf111b9e2d
    resource: repo://tools/test.sh
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Build and Deploy

There is one workflow, `.github/workflows/pages-deploy.yml`, and one deployment
target, GitHub Pages with GitHub Actions as the source. A push to `main` builds
the site, checks its links, uploads the result as a Pages artefact, and deploys
it. No other path publishes anything.

## Triggers

The workflow runs on three events:

- **Push to `main` or `master`**, with `.gitignore`, `README.md`, and `LICENSE`
  in `paths-ignore` so documentation-only commits do not spend a deploy.
- **Pull requests targeting those branches**, so dependency and configuration
  errors surface before they reach `main`.
- **Manual dispatch** from the Actions tab.

The pull request trigger matters more here than in most repositories, because no
`Gemfile.lock` is committed and CI resolves dependencies fresh on every run. A
newly released transitive dependency can break the build without anything in the
repository changing. See [Local Development](../operations/local-development.md).

## The two jobs

**`build`** does everything except publish:

1. Checkout with `fetch-depth: 0`.
2. `actions/configure-pages` to learn the Pages base path.
3. Ruby 3.4 with `bundler-cache: true`, which installs gems and caches them
   between runs.
4. `jekyll b` into `_site<base_path>` with `JEKYLL_ENV=production`.
5. `htmlproofer` over `_site`.
6. Upload the Pages artefact, but only when the event is not a pull request.

**`deploy`** needs `build`, is gated on the event not being a pull request, and
runs `actions/deploy-pages` in the `github-pages` environment.

The pull request path is therefore gated twice: the artefact is never uploaded
and the deploy job never runs. Both conditions test the same thing, which is
deliberate belt and braces. A pull request gets the full build and the full link
check with no way to publish.

## Why full history

`fetch-depth: 0` is not caution, it is a hard requirement. The
`posts-lastmod-hook.rb` plugin shells out to `git rev-list` and `git log` for
every post during the build to derive `last_modified_at`. Under the default
shallow checkout, every post would appear to have exactly one commit and no post
would ever show an updated date. Nothing would fail; the dates would just quietly
be wrong. See [Site Structure](../architecture/site-structure.md).

## The link check

`htmlproofer` runs with external links disabled and with loopback URLs ignored,
so it validates internal links, anchors, and image references only. It does not
detect a broken outbound link, and it cannot notice that the site's configured
`url` points at the wrong domain, because those are absolute.

The build directory is suffixed with the Pages base path from `configure-pages`,
so internal links resolve exactly as they will once served. With an empty
`baseurl` that suffix is empty, but the mechanism is what keeps the check honest
if a base path is ever introduced.

`tools/test.sh` is the local equivalent and shares the same html-proofer flags
and production build. Two differences are worth knowing: the local script derives
the suffix by parsing `baseurl` out of the config files itself rather than from
the Pages action, and it deletes `_site` first, which CI never needs to do on a
fresh runner. The larger difference is availability: html-proofer needs libcurl
and does not run on Windows, so CI is the only place the link check reliably
executes.

## Concurrency and permissions

The concurrency group is `pages-${{ github.ref }}` with `cancel-in-progress`.
Keying by ref rather than using a single global group is what stops a pull
request run from cancelling an in-flight production deploy. Two pushes to `main`
in quick succession still collapse to the latest, which is the intent.

Permissions are the minimum Pages needs: `contents: read`, `pages: write`, and
`id-token: write` for the deployment's OIDC token. The workflow needs no write
access to the repository.

## The domain

`CNAME` at the repository root holds the custom domain and is copied into the
built site, which is how Pages knows to serve it there. It must agree with the
`url` key in `_config.yml`; nothing in the pipeline checks that they match. See
[Site Configuration](../operations/site-configuration.md).

`.nojekyll` sits at the repository root as well. With Actions as the Pages source
the site is built by the workflow rather than by Pages' own Jekyll, so this file
is inert belt and braces rather than load-bearing.

## Related

- [Local Development](../operations/local-development.md) for reproducing the CI check locally
- [Authoring a Post](authoring-a-post.md) for what must be true of a post before it is pushed
