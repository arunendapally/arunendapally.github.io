---
title: Why I'm Starting This Blog
author: arun
date: 2025-11-08 00:00:00 +0000
categories: [Personal]
tags: [welcome, software-development, ai, cloud]
pin: true
seo:
  description: Arun Endapally — Senior Technical Architect writing about architecture and AI in engineering, based on many years building enterprise-scale systems
---

Many years of building software teaches you a few things. Clean architecture is rare. Most complexity is accidental. And the tools change faster than the underlying problems do.

I'm Arun — a Senior Technical Architect who has spent many years building and modernising enterprise-scale platforms across fintech and global SaaS products. I've been the person responsible for the decisions that are hard to reverse: how systems are decomposed, how APIs are versioned, how teams are structured around code.

This blog is where I write about what I've learned doing that work.

## What keeps going wrong

The same problems appear everywhere, regardless of company size or tech stack.

**Systems that weren't designed to grow.** The most common thing I've done in my career is help organisations break apart monoliths that were built for a world that no longer exists. Decomposing legacy products into microservices, migrating monolithic UIs to micro-frontends, rebuilding multi-tenant platforms from the ground up. The technical steps differ but the underlying problem is the same: an architecture that made sense at one scale becomes a liability at another.

**APIs that nobody can actually use.** Most API problems aren't technical. They're communication problems that show up as technical problems. Teams produce endpoints that are internally consistent but impossible to integrate against from the outside. Establishing OpenAPI standards and versioning practices that third parties can depend on is harder than it sounds. The lesson: an API is a promise. Design it like one.

**Non-functional requirements treated as optional.** Performance, security, observability — these get deferred to "after we ship" and then never come back. Governing NFRs is part of my day job and the reason I've spent real time with tools like OpenTelemetry, DataDog, and Veracode. If you don't build these in from the start, you pay for them twice.

## Where AI actually helps

I've been running workshops on AI adoption for engineering teams for a couple of years now. The honest version of what I've found:

AI tools are genuinely useful for code generation, automated test scaffolding, and requirement analysis. They save real time on well-defined tasks with clear inputs and outputs. Where they fall down is anywhere that requires understanding system context — knowing which change will break something three layers away, or why a particular architectural decision was made three years ago.

The teams that get the most out of AI tools treat them as accelerators for work they already understand well. The teams that struggle treat them as a replacement for that understanding.

I'm writing about this because the signal-to-noise ratio in "AI for developers" content is terrible. Most of it is either uncritical enthusiasm or blanket scepticism. What's missing is practical assessment based on real use.

## What I'll write here

Two things:

**Architecture** — the decisions that are hard to reverse and the tradeoffs behind them. Microservices vs. monolith, API design, micro-frontends, event-driven architecture. Concrete tradeoffs from real systems, not pattern catalogues.

**AI in engineering** — code generation, agentic workflows, automated testing. What I've seen work in practice, what's overhyped, and how to evaluate both honestly.

I keep things practical. If I can't make it concrete, I don't post it.
