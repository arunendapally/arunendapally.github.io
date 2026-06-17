---
title: "Getting Started with Google Gemini AI in VSCode: A Quick Setup Guide"
author: arun
date: 2025-11-08 00:00:00 +0000
categories: [Development Tools, AI]
tags: [gemini, vscode, ai, terminal, npm, workflow, google-ai, productivity]
seo:
  description: A straightforward guide to setting up and using Google's Gemini AI in your VSCode terminal — including when it's worth reaching for over other tools
---

I've been running a few different AI tools in parallel to see how they actually fit into a developer workflow. Claude for longer sessions and architecture thinking, Copilot for in-editor completions. When Google released the Gemini CLI I added it to the mix and found it earns its place for a specific kind of work — fast, lightweight, no context overhead. Here's how to set it up and when I actually reach for it.

## What You'll Need

- A Google account
- [VSCode](https://code.visualstudio.com/) installed
- [Node.js and npm](https://nodejs.org/en/download/) — the Gemini CLI installs via npm

## Installing the Gemini CLI

Open your VSCode terminal and run:

```bash
npm install -g @google/gemini-cli
```

On newer npm versions the equivalent is:

```bash
npm install --location=global @google/gemini-cli
```

This installs the `gemini` command globally so it's available from any directory.

## Authenticating

Run `gemini` once to authenticate:

```bash
gemini
```

This opens a browser, prompts you to sign in with your Google account, and asks for permissions. After that it drops you into an interactive session. You're ready.

## How I Use It Day-to-Day

There are three modes worth knowing:

**Interactive session** — just run `gemini` with no arguments. Good for back-and-forth conversations, debugging sessions, or working through a problem:

```bash
gemini
```

Type `exit` or `quit` to leave.

**One-shot prompt** — pass a prompt with `-p` when you want a single answer and don't need a session:

```bash
gemini -p "What's the difference between Task and ValueTask in C#?"
```

This is the one I use most. It's fast and stays out of the way.

**Inline code questions** — you can pass code directly in the prompt string:

```bash
gemini -p "Explain this and suggest a simpler version:\n\nvar result = items.Where(x => x != null).Select(x => x.Value).ToList();"
```

**Keeping it updated** — the CLI moves quickly, so update it regularly:

```bash
npm update -g @google/gemini-cli
```

## When It's Worth Reaching For

After a few months of using this alongside other tools, here's where Gemini CLI actually earns its place:

**Quick lookups without leaving the terminal.** When I'm in the middle of something and need a fast answer — a regex pattern, a flag I've forgotten, an API signature — the `-p` flag is faster than switching to a browser. No new tab, no context switch, answer comes back in the same window I'm working in.

**Language-agnostic questions.** The CLI is useful for questions that span languages or tools — shell scripts, quick SQL, Dockerfile syntax, things that aren't the primary language of whatever project is open. It doesn't depend on your workspace context, which is sometimes exactly what you want.

**Brainstorming without committing to a session.** When I want to think through a problem without starting a full conversation, a one-shot `-p` prompt is enough. I'm not loading context, I'm not in a session that I'll want to continue — just a question and an answer.

**Where it's not the right choice:** anything that requires understanding your codebase. The CLI has no access to your files unless you paste content directly into the prompt. For refactoring, code review, or multi-file work, an editor-integrated tool or a tool with file access (like Claude Code) is the better fit. The CLI is deliberately lightweight — that's both its strength and its limit.

## A Few Practical Notes

- The Gemini CLI uses your Google account's Gemini access. If you're on a free tier, there are rate limits — they're generous for occasional use but you'll hit them in heavy sessions.
- For sensitive code or internal projects, be aware that prompts go to Google's servers. The same consideration applies to any cloud-based AI tool, but worth keeping in mind.
- The interactive mode doesn't have persistent memory across sessions. Each `gemini` invocation starts fresh — no thread history from yesterday's session.

The Gemini CLI fits best as a lightweight complement to heavier tools, not a replacement for them. For terminal-first developers who want a fast AI lookup without leaving their workflow, the setup is five minutes and the payoff is immediate.
