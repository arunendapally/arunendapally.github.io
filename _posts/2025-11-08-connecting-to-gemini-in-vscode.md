---
title: "Getting Started with Google Gemini AI in VSCode: A Quick Setup Guide"
author: arun
date: 2025-11-08 12:00:00 +0530
updated: 2026-05-19 12:00:00 +0530
categories: [Development Tools, AI]
tags: [gemini, vscode, ai, terminal, npm, workflow, google-ai, productivity]
seo:
  description: A straightforward guide to setting up and using Google's Gemini AI in your VSCode terminal for a better development experience
---

I've been trying out a few different AI tools lately to see how they fit into my workflow. I've been playing around with Claude, and recently I decided to give Google's Gemini a shot. I found a really simple way to use it directly from my VSCode terminal, and I wanted to share how I got it set up.

## What You'll Need

First, a few things you'll need to have ready:

*   A Google account.
*   [VSCode](https://code.visualstudio.com/) installed on your computer.
*   [Node.js and npm](https://nodejs.org/en/download/), since I used `npm` to install the Gemini CLI.

## Why the Terminal Works Well for AI

I like keeping the AI experience in the terminal because it lets me stay in the same place where I write code. Gemini is fast for quick prompts, brainstorming, and debugging without pulling me into a separate browser tab or editor pane.

## Getting Everything Set Up

Here’s how I got it all working.

### 1. Installing the Gemini CLI

The first thing I did was install the Gemini CLI tool. I opened up my terminal in VSCode and ran this `npm` command:

```bash
npm install -g @google/gemini-cli
```

If you use a newer npm version, the equivalent command is:

```bash
npm install --location=global @google/gemini-cli
```

This installs the package globally on your machine so you can call the `gemini` command from any directory.

### 2. Authenticating with My Google Account

Once the installation finished, I connected the CLI to my Google account by running:

```bash
gemini
```

That command opened a browser, prompted me to sign in, and asked for permissions. After authorization, the CLI was ready.

### 3. Using Gemini in My Terminal

Now for the fun part! With everything set up, I could start using Gemini in the VSCode terminal. The simplest invocation is just `gemini`.

Here are a few ways I’ve been using it:

**a. Generating text:**

I use it for quick drafts and code snippets. For example:

```bash
gemini -p "Write a short, inspiring quote about software development."
```

**b. Chatting with Gemini:**

For brainstorming, problem solving, or debugging, I use the CLI itself in interactive mode:

```bash
gemini
```

That opens a terminal conversation session where you can ask follow-up questions. Type `exit` or `quit` to leave.

**c. Fixing or improving code:**

You can also ask Gemini to help rewrite or explain code in place. For example:

```bash
gemini -p "Explain the following JavaScript function and suggest a cleaner version.\n\nfunction add(a, b) { return a + b; }"
```

**d. Getting help:**

When you need a quick reference, use the built-in help:

```bash
gemini --help
```

It lists available commands, options, and shortcuts so you can explore more features.

### 4. Keeping Gemini Updated

The Gemini CLI changes quickly, so it’s worth updating it regularly:

```bash
npm update -g @google/gemini-cli
```

This keeps the tool current with new commands and improvements.

## Conclusion

Using Gemini in the VSCode terminal has become a helpful part of my workflow. It lets me stay focused while still tapping into AI for writing, brainstorming, and debugging. If you want a lightweight, terminal-first way to bring AI into your development process, the Gemini CLI is a great place to start.
