---
layout: post
title: How I Set Up Gemini in My VSCode Terminal
date: 2025-11-08 12:00:00 +0000
categories: [Gemini, VSCode, AI]
tags: [gemini, vscode, ai, terminal, npm, workflow]
---

I've been trying out a few different AI tools lately to see how they fit into my workflow. I've been playing around with Claude, and recently I decided to give Google's Gemini a shot. I found a really simple way to use it directly from my VSCode terminal, and I wanted to share how I got it set up.

## What You'll Need

First, a few things you'll need to have ready:

*   A Google account.
*   [VSCode](https://code.visualstudio.com/) installed on your computer.
*   [Node.js and npm](https://nodejs.org/en/download/), since I used `npm` to install the Gemini CLI.

## Getting Everything Set Up

Here’s how I got it all working.

### 1. Installing the Gemini CLI

The first thing I did was install the Gemini CLI tool. I opened up my terminal in VSCode and ran this `npm` command:

```bash
npm install -g @google/gemini-cli
```

This installed the package globally on my machine, which means I can call the `gemini` command from anywhere.

### 2. Authenticating with My Google Account

After the installation finished, I needed to connect it to my Google account. This was super easy. I just typed `gemini` into the terminal:

```bash
gemini
```

That command automatically opened my web browser and prompted me to log in with my Google account and grant the necessary permissions. Once I did that, the CLI was authenticated and ready to go.

### 3. Using Gemini in My Terminal

Now for the fun part! With everything set up, I could start using Gemini directly from my VSCode terminal. The main command is just `gemini`.

Here are a couple of ways I've been using it:

**a. Generating Text:**

I often use it to generate quick text snippets or even code. For example, I asked it for an inspiring quote:

```bash
gemini generate text "Write a short, inspiring quote about software development."
```

**b. Chatting with Gemini:**

This is probably my favorite feature. I can start an interactive chat session to brainstorm ideas, debug code, or just ask questions.

```bash
gemini chat
```

This drops you into a chat session right in the terminal. To leave, you just type `exit` or `quit`.

**c. Getting Help:**

If I ever forget a command, the built-in help is super useful.

```bash
gemini --help
```

This gives a nice list of all the available commands and what they do.

## Conclusion

Bringing Gemini into my VSCode terminal has been a valuable addition to my workflow. It's made it much easier to get quick assistance and generate ideas without losing focus. If you're looking to integrate AI into your coding environment, I highly recommend exploring the Gemini CLI.
