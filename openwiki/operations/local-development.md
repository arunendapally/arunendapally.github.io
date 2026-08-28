---
type: operations
title: Local Development
description: Running, serving, and testing the blog locally, including the helper scripts, the devcontainer, the deliberate absence of a committed Gemfile.lock, and the Windows limitations that shape the workflow.
tags: [local-development, jekyll, bundler, devcontainer, windows, html-proofer]
verified:
  - by: openwiki/0.4.0
    at: 2026-08-27T15:56:38.540Z
sources:
  - id: openwiki-source-57dc109daa6babd441d8b47c
    resource: repo://_plugins/posts-lastmod-hook.rb
  - id: openwiki-source-f7c89635dfc6efb0ecec007f
    resource: repo://.devcontainer/devcontainer.json
  - id: openwiki-source-2021f0fbe5ed04ba2d346fa4
    resource: repo://.devcontainer/post-create.sh
  - id: openwiki-source-ea70eb6c045047448e446296
    resource: repo://.gitignore
  - id: openwiki-source-68180d68a9748362b67ca1a4
    resource: repo://.vscode/tasks.json
  - id: openwiki-source-d5a1739d11bdad59b9de4986
    resource: repo://Gemfile
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-8975959e4c3b9c9b2137d33a
    resource: repo://THEME_UPGRADE.md
  - id: openwiki-source-dc4b9c9bad4eb70b3e61c0aa
    resource: repo://tools/run.sh
  - id: openwiki-source-672762f087717abf111b9e2d
    resource: repo://tools/test.sh
generated: {by: "claude-code", at: "2026-08-27T15:56:38.540Z"}
---

# Local Development

The site is a standard Bundler-managed Jekyll project: `bundle install`, then
`bundle exec jekyll serve` on port 4000. Ruby 3.1 or newer. Two helper scripts
and a devcontainer wrap that, and a few environment-specific constraints are
worth knowing before trusting a local result.

## Serving the site

`tools/run.sh` builds a `jekyll serve` command and evaluates it. It starts from
`bundle exec jekyll s -l`, appends the host, prefixes `JEKYLL_ENV=production`
when given `-p`, and adds `--force_polling` when it detects it is running inside
Docker by looking for `docker` in `/proc/1/cgroup`. The polling flag matters
because filesystem change notifications do not propagate reliably across a
container's bind mounts, so without it a rebuild-on-save never fires.

The default host is `127.0.0.1`; `-H` overrides it, which is what you need to
reach the dev server from another device on the network.

`tools/test.sh` is the local mirror of the CI check. It runs with `set -eu`,
deletes any existing `_site`, parses `baseurl` out of the config (walking a
comma-separated config list in reverse so the last file to define it wins),
builds with `JEKYLL_ENV=production` into `_site$baseurl`, and then runs
html-proofer over the output with external links disabled and localhost URLs
ignored. Building into a `baseurl`-suffixed directory is what makes internal
links resolve the way they will in production.

VS Code exposes both scripts as tasks: "Run Jekyll Server" is the default build
task, "Build Jekyll Site" runs the test script.

## No committed lockfile

`Gemfile.lock` is gitignored, and this is deliberate rather than an oversight.
A lockfile generated on Windows pins mingw-only builds of `google-protobuf` and
`sass-embedded`, which the Linux CI runner cannot install. Regenerating it on
Windows to fix that pulls gem versions, `json` among them, that then fail to
build locally. There is no lock that satisfies both machines, so neither gets
one and both resolve fresh against the `Gemfile`.

The consequence is that the `Gemfile` is the only version pin the project has.
That is why `jekyll-theme-chirpy` carries an explicit constraint there rather
than being left open: without it, nothing would hold the theme version steady
across a CI run. See [Theme Overrides and Upgrades](../architecture/theme-overrides.md)
for how that constraint is bumped.

It also means CI resolves dependencies independently of any local install, so a
build that works locally can still fail in CI on a freshly released transitive
dependency. The pull request build exists partly to catch that.

## Windows limitations

Several things simply do not work on Windows, and knowing which ones prevents
chasing phantom bugs:

- **`jekyll serve --livereload`** needs eventmachine's native extension. Plain
  `serve` still regenerates on save, so the workaround is to reload the browser
  manually. Note that `tools/run.sh` passes `-l` unconditionally, so on Windows
  the script itself is not usable as-is.
- **`jekyll serve --detach`** needs `fork`, which Windows lacks.
- **`htmlproofer`** needs `libcurl`, which the Ruby installer for Windows does
  not ship. The link check therefore only ever executes in CI. Locally, the
  substitute is to inspect the built `_site` for unresolved internal links,
  missing `alt` attributes, and broken anchors by hand.

That last one is the important one: a clean local build is not evidence that the
link check will pass. See [Build and Deploy](../workflows/build-and-deploy.md)
for what CI actually enforces.

## The devcontainer

`.devcontainer/devcontainer.json` uses the Microsoft Jekyll devcontainer image
and marks the workspace folder as a git safe directory on create. That last step
is not cosmetic: the last-modified plugin shells out to git during every build,
and git refuses to operate on a repository owned by a different user without it.

`post-create.sh` installs the `shfmt` formatter, adds two oh-my-zsh plugins, and
runs an npm build only if a `package.json` is present, which it is not in this
repository. The devcontainer is the most reliable way to run the full local
check, including html-proofer, from a Windows host.

## Related

- [Build and Deploy](../workflows/build-and-deploy.md) for the CI pipeline this mirrors
- [Theme Overrides and Upgrades](../architecture/theme-overrides.md) for the upgrade verification steps
