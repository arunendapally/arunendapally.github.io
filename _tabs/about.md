---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

I'm Arun, a Senior Technical Architect. I build and modernize large software platforms, and I spend a good deal of my own time on AI tooling: what it can do, where it falls short, and how to tell the difference.

Architecture is mostly judgement under incomplete information. Working out what the business actually needs before anyone has settled on how to describe it. Choosing between approaches that are all defensible, under constraints (time, budget, legacy, the skills on hand) that rule out the textbook answer. Setting standards and guardrails so several teams can move at once without the platform pulling apart. Knowing which problems to solve now and which to leave alone. And staying close enough to the code that the decisions still hold when someone builds them.

A fair share of it is people rather than systems. Most architecture decisions are carried out by teams that don't report to you, so the work is as much about building agreement as about being right.

Lately much of that runs through spec-driven development: specification first, tradeoffs recorded, then AI agents on the parts they are genuinely good at. The interesting question isn't whether AI makes you faster. It's whether the rigour survives the speed.

## What I work on

- **Requirements to target-state design**: working with product and engineering to turn business intent into a concrete target state, and getting it through review
- **Microservices and API design**: resource-oriented REST, OpenAPI standards, and versioning practices that third parties can depend on; decomposing systems that have outgrown their original shape
- **Micro-frontends**: moving monolithic UIs to modular, independently deployable frontends using React and Web Components
- **Architecture as written artifacts**: ADRs, C4 models, domain models, and migration strategies, because a decision nobody recorded is a decision nobody can revisit
- **Observability and NFRs**: making performance, security, and reliability first-class concerns rather than afterthoughts, with OpenTelemetry, DataDog and Grafana
- **Mentoring**: architecture and code reviews, hiring and interviewing, and coaching engineers toward decisions they can defend

## Experiments

I'm curious about a lot of things, so I run experiments on my own workflows and projects. Some of them turn out to be useful to other people:

- A Claude plugin that manages my stock portfolio: daily briefings, stop-loss audits, and risk checks, in about five minutes a day.
- Claude Code running entirely on free-tier models, with routing and compression layered on top, to find the practical limits.
- A two-line status line for Claude Code showing the model, folder, git state and session cost at a glance.

Most of what I know about using these tools in practice came from side projects rather than from a roadmap.

**Certifications:** SAFe® 6 Architect, Microsoft Azure (AI Fundamentals, Data Fundamentals, Fundamentals), Agentic AI.

On this blog I write mostly about applying AI to real engineering work: the tools I'm testing, what held up, and what didn't. Occasionally architecture, when I have something concrete to say.
