---
title: "OpenWiki: Stop Your Agent Rediscovering the Same Codebase"
author: arun
date: 2026-08-26 00:00:00 +0000
categories: [AI, Developer Tools]
tags: [openwiki, langchain, claude-code, mcp, agents, documentation, context-engineering, microservices]
description: "Every new agent session rebuilds the same understanding of your repo from scratch, and across a platform of many services that costs real tokens and real time. OpenWiki writes a linked wiki you commit alongside the code, so the next session reads a page instead of the repository. How it works, how it handles going stale, and how to run it on a Claude subscription with no API key."
image: /assets/img/posts/openwiki-agent-documentation-card.png
---

You ask your agent to add a field to an endpoint. Before it touches anything, it lists the directories. It greps for the handler. It opens the router, then the controller, then the service class, then a couple of DTOs to work out what the controller actually returns.

None of that is wrong. It is exactly what a careful new joiner would do, and it is why the exploration is worth watching: you learn something about your own codebase from the order in which it looks things up.

The trouble is that it happens again tomorrow. And in the session after lunch. The agent rebuilds the same understanding every time, gets to roughly where it was, and loses all of it when the window closes. What a human does once and remembers for a year, an agent does on every prompt, and you pay for it twice over: in tokens, and in the minutes you spend watching it catch up.

It stops being a rounding error on an enterprise platform. When the service you are changing calls three others, the agent cannot answer "what can that service do, and what does it hand back" without going and reading that service too. Multiply that across dozens of microservices and micro frontends and the rediscovery, rather than the work, becomes the biggest line in your context budget.

[OpenWiki](https://github.com/langchain-ai/openwiki) is LangChain's answer. Its own description is a good one: *the self-maintaining wiki, built for agents, explored by humans*. It reads your sources, writes a linked Markdown wiki that you own and commit, and keeps it current as the code moves.

> **TL;DR**
>
> - The exploring is fine. The **re-exploring** is the waste, and it is paid for in tokens and in waiting, on every prompt. Committed documentation makes it a one-off.
> - One giant instructions file does not solve it, because it is all or nothing. A **linked wiki with an index** lets the agent open only the page the task needs. Progressive disclosure, applied to documentation.
> - Staleness is handled by **Grounded Claims**: each fact cites a versioned source span, so the tool knows which statements to recheck when that code changes.
> - **You do not need an API key.** `openwiki integrations install claude` makes OpenWiki an MCP server and lets Claude Code do the thinking on the subscription you already have.
> - The **scheduled CI refresh does need a key**, because CI has no agent session. Local updates do not.
{: .prompt-tip }

## Why one big instructions file is not the answer

The obvious fix is to write it all down in `CLAUDE.md`{: .filepath} or `AGENTS.md`{: .filepath}. Most of us have tried. It starts as fifteen honest lines and six weeks later it is four hundred, including a paragraph nobody remembers adding.

The length is not really the problem. The problem is that the file is **indivisible**. It is read in full on every task, whether the task is fixing a typo or redesigning a schema. You end up choosing between giving the agent too little context and paying for the whole file on a one-line fix, and you make that choice again on every request.

A wiki with an index changes the shape of the choice. The index is small and always affordable. Each page is opened only when the task points at it. Working on authentication? Read the auth page, and nothing else.

This is progressive disclosure, the principle good API documentation has used for years: a short overview, then depth on demand. What is new is the reader. It used to be about not overwhelming a person. Now it is about not filling a context window with material the task will never touch.

## What actually gets committed

After a run you have an `openwiki/`{: .filepath} directory:

```text
openwiki/
├── INSTRUCTIONS.md         # your scope brief, hand-written, preserved across runs
├── index.md                # generated entry point
├── quickstart.md           # orientation and a task-routing table
├── architecture/           # one directory per area, each with its own index.md
├── workflows/
├── operations/
├── tools/
└── .claims/                # evidence sidecars, one JSON per page
```

Plus a short pointer block appended to `AGENTS.md`{: .filepath} and `CLAUDE.md`{: .filepath} at the repo root. That pointer is the whole integration mechanism. No protocol, no plugin: the agent finds the wiki the way it finds anything else, by reading the instructions file and following a link.

The page that surprised me by being most useful is `quickstart.md`{: .filepath}, because it carries a task-routing table:

| If you are... | Read |
|---|---|
| Changing a formula or a target | The domain core page |
| Adding an API endpoint | The tool surface page, then the catalog |
| Writing a query that touches user data | The data access page |
| Wondering why a test is failing | The testing page |

That is the index of the index. An agent lands, matches its task to a row, opens one page and starts working. It is also why the wiki has to be committed rather than regenerated per session: generating it fresh each time would cost more than the exploration it replaces.

## Where it helps most: services that call other services

Say you are adding a discount to checkout. Checkout calls pricing, and pricing calls inventory. To make one change in one repository, your agent needs to know what pricing accepts, what it returns when an item is out of stock, and which of those fields it is safe to depend on.

Today it finds out by reading pricing. It clones the repo, opens the controller, follows the response type, and infers the contract from the code. Then inventory, the same way. Tomorrow, in a new session, it does it again.

The alternative is to run OpenWiki in each service and commit the wiki beside that service's own code. Now checkout's agent reads a few hundred words of pricing's wiki, which already says what pricing exposes and what it guarantees, and never opens pricing's source at all.

The reason this works is that the two documents have different readers. A README is written for a person deciding whether to adopt your service. These pages are written for something that needs to know what a call returns and what it must not break. We have historically only written the first kind.

Two things to be straight about. I ran this on two individual repositories, not across a real estate, so this section is reasoning from the shape of the output rather than a result I measured. And it only holds while every service's wiki is current, because a stale wiki for a downstream service is worse than none: the agent will believe it and will not go and check.

## Staleness is the whole problem

Generated documentation has always failed the same way. Accurate on Tuesday, wrong by Friday, and nobody can tell which sentences went bad. Once people stop trusting it they stop reading it, and untrusted documentation is worse than none, because it still costs a read.

OpenWiki's answer is **Grounded Claims**. A Claim is one falsifiable statement tied to versioned source evidence, and every reference is a `repo://`{: .filepath} URI with a line span rather than a bare path:

```json
{
  "statement": "The load-history filter keys on null rather than falsiness, so a genuine zero-weight set is kept as a real data point.",
  "evidence": [{ "resource": "repo://src/domain/summary.ts#L150-L160" }]
}
```

These live in `openwiki/.claims/`{: .filepath} beside the pages. When the cited lines change, OpenWiki knows exactly which propositions to recheck. It is closer to a citation than to a comment.

The trust marker is earned rather than assumed. A page only receives its `verified:` front matter after a submission reconciles a complete Claims set, passes a final evidence recheck, and persists the sidecar. A clean run alone never stamps it.

Be clear about what this buys. It does **not** make documentation self-maintaining, whatever the tagline says. It converts staleness from an invisible problem into a reviewable one. That is a smaller claim and a far more useful one, because it removes the dangerous failure: a page that is confidently wrong with nothing to show which part.

### Keeping it fresh: two options

**A scheduled workflow.** OpenWiki ships templates for GitHub Actions, GitLab CI and Bitbucket Pipelines. They run `openwiki code --update`, which diffs `HEAD` against the commit last documented, regenerates what moved, and opens a pull request. The update arrives as a diff you review rather than a chore you forget.

> **The scheduled workflow needs a paid API key.** Unattended means no agent session to hand the work to, so OpenWiki has to call a model itself. I removed the workflow from my own repo for exactly this reason.
{: .prompt-warning }

**Updating locally.** In a session started in the repository, just ask for an update. Same diffing, same Claims reconciliation, no key, but it happens when you remember rather than on a schedule. For a personal repo that is a fine trade. For a shared service whose stale wiki would mislead other people's agents, the scheduled job is worth the money.

One practical note. `--update` only revisits pages whose evidence moved, so a file that was skipped and has not changed since gives it nothing to react to. The lever there is `INSTRUCTIONS.md`{: .filepath}, the hand-written scope brief, which is preserved across runs. Do not hand-edit generated pages; the next run overwrites them.

## Seeing it: the visualizer

`openwiki visualize` turns the wiki into an interactive node graph with a live Markdown reader beside it. It needs no model, no key and no completed run: it worked for me on an interrupted set of pages before finalization had ever succeeded.

```shell
openwiki visualize openwiki --port 4500
```
{: .nolineno }

![The OpenWiki visualizer showing a generated wiki, with a node graph on the left and a rendered page on the right](/assets/img/posts/openwiki-agent-documentation/visualizer.png){: w="1600" h="1000" .shadow }
_Nodes grouped by each page's `type`, edges from declared related pages and inline links, live reader on the right._

It serves on a local loopback address and is never exposed to the network. Edits to the wiki refresh the browser as you make them. `--export <dir>` produces a self-contained static build for GitHub Pages, MkDocs or any static host. Two gotchas: the export must be served rather than opened over `file://`, or the graph script stays inert, and the viewer pulls its graph and diagram libraries from a public CDN, so it needs an internet connection even locally.

## Running it without an API key

Every guide I found says the same thing: run `openwiki --init`, pick a provider, paste a key. That is real advice for a real path, and it is the wrong path if you already pay for a coding agent.

There are two execution modes, and only one of them buys inference:

| | Standalone CLI | Agent integration |
|---|---|---|
| **Command** | `openwiki --init` | `openwiki integrations install claude` |
| **Who does the thinking** | OpenWiki calls a model | **Your coding agent does** |
| **Credentials** | A provider key, billed per token | The session you already have |
| **What OpenWiki is** | The whole tool | An MCP server plus a skill |
| **Runs** | Unattended, so CI works | Inside a session |

In the second mode OpenWiki stops being an AI tool at all. Its skill file says so, addressing the agent directly:

> OpenWiki owns run state, the page queue, Claims validation and persistence, indexes, provenance, and finalization. You own semantic repository research and the prose for the single page OpenWiki assigns you.

That "you" is Claude Code. OpenWiki becomes a work queue with a filing system. Integrations exist for Codex and OpenCode on the same terms.

### Why a Claude subscription cannot drive `--init`

Worth stating plainly, because it confused me for a while. You can run `openwiki --init`; it just cannot run on a Claude Pro or Max plan, and that is a limit on Anthropic's side rather than a gap in OpenWiki.

| Provider | Credential |
|---|---|
| OpenAI (ChatGPT login) | Browser sign-in, spends your plan's included Codex usage |
| GitHub Copilot | Your existing `gh` CLI session |
| Anthropic | `ANTHROPIC_API_KEY`, and nothing else |

The first two exist because OpenAI and GitHub each publish an OAuth-authenticated inference endpoint that third-party programs may call. Anthropic has no equivalent. A Claude subscription entitles you to Claude's own apps, Claude Code among them; it is not a general-purpose API credential, and Claude Code's session token authenticates Claude Code rather than any other binary on your machine.

So, the sentence that trips everybody: **a Claude Code subscription is not an API key.** Separate products, separate billing. A key means a console account with a card on it, and a per-token charge for every documentation run on top of the subscription.

The integration path sidesteps the question entirely. Instead of OpenWiki borrowing your subscription, it stops doing inference and hands the work to the process that already holds one.

### The commands

Node 22 or newer. On Windows install through npm or pnpm rather than bun, because the native dependencies do not compile cleanly.

```shell
npm install -g openwiki
openwiki integrations install claude --project
```
{: .nolineno }

That writes a `.mcp.json`{: .filepath} declaring the OpenWiki MCP server, plus a skill under `.claude/`{: .filepath}. Restart your agent in that directory, check the server is connected, then ask:

```text
Initialize this repository's OpenWiki from the current source and tests.
```

The agent gets five tools and a strict sequence: `openwiki_begin`, `openwiki_submit_plan`, then `openwiki_next_page` and `openwiki_submit_page` in a loop, then `openwiki_finish`. The planning step decides whether the output is any good, because that is where the taxonomy is designed around meaningful systems rather than mirroring your source folders.

## Two things to do before the first run

**Write `.openwikiignore`{: .filepath}.** This is the one that matters. OpenWiki reads your **working tree**, not your tracked files. Every secret your `.gitignore`{: .filepath} protects is still on disk and fully visible to it: local env files, credential scratch files, database dumps, personal exports. Mirror your gitignore secrets rules into `.openwikiignore`{: .filepath} before the first pass, then read the generated pages for anything that leaked.

**Write `openwiki/INSTRUCTIONS.md`{: .filepath}.** The scope brief, preserved across runs. Name what the system is for, rank what to document by value, rule out directories that are background rather than behaviour, and state any hard prohibitions. Without it you get a beautifully formatted tour of your config files.

## The caveat that cost me two passes

Source drift invalidates the **entire plan**, not just the page whose evidence moved.

I finished thirteen pages on a busy repository, called finish, and got a conflict: someone had committed while I worked. The completed count reset to zero. I redid every page, called finish again, and hit the same wall, this time because a commit had added files that were primary evidence for two pages.

Then I ran it on a repository nobody else was touching, and it completed first time. So this is not a guess. The only variable that changed between the two runs was whether anyone else was committing.

The README is upfront about the CI version of this: interrupted runs can resume when the same checkout persists, but ephemeral CI runners keep no uncommitted run state after a failure.

> **Run it on a quiet tree.** A branch nobody else is touching, or a moment when your working copy is settled.
{: .prompt-warning }

## What it catches, and what it misses

The most useful output was not a page. It was a contradiction.

Generated documentation reads the source every time, so it is unusually good at catching the gap between what a project says about itself and what is actually in the tree. The pattern to expect:

- **A note that has quietly gone out of date.** A hand-written status line saying a feature is not built yet, while its migration, its modules and its tests are all sitting in the repository. Nobody lied. The note was accurate the day it was written and the code moved underneath it.
- **Invariants that only exist in tests.** Rules nobody wrote down in prose, discoverable only because a test asserts them, which is exactly the sort of thing a new agent breaks by accident.
- **Dead configuration and unreachable options** that survive because no human reads a config file end to end.

And it misses things, which is why you review the output rather than merging it blind:

- **The odd file out.** It will describe a directory by its dominant file type and quietly skip the one or two that do not fit, including, in my case, a script I run most days.
- **Why, as opposed to what.** It reads code, so it recovers behaviour and not the argument that produced it. The reasoning behind a decision lives in your hand-written notes and nowhere else.
- **Anything outside the repository.** Runbooks, incidents, the conversation where a trade-off was settled.

OpenWiki is honest about this in the pointer block it writes into `AGENTS.md`{: .filepath}: the wiki is "optional just-in-time context, not required startup reading", and agents are told to treat source and tests as authoritative. That is a more modest claim than most coverage makes, and it is the right one.

Keep both kinds of document. Just know which to trust about what.

## Where this leaves me

I would run this on any service I inherited, before writing a line, and read the index first. It tells you what your agent is going to believe about the codebase, which is worth knowing whether or not it turns out to be correct.

For a repo I know cold, the hand-written instructions file stays. It holds judgement and taste no generator produces.

The pattern underneath will outlive this particular tool. We are learning to write for a reader that never skims, never guesses from a variable name, and never asks the person at the next desk. It reads exactly what you committed, and believes it.

Sources: [OpenWiki on GitHub](https://github.com/langchain-ai/openwiki), [OpenWiki docs](https://docs.langchain.com/oss/openwiki/overview)
