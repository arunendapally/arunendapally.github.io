---
title: "Build a Two-Line Status Line for Claude Code"
author: arun
date: 2026-06-10 00:00:00 +0000
categories: [AI, Developer Tools]
tags: [claude-code, statusline, cli, git, productivity, developer-tools, nodejs]
seo:
  description: Build a custom two-line status line for Claude Code so you can see the model, folder, git status, and session cost at a glance — handy when you're juggling several Windows Terminal tabs. Includes a working Node.js script.
---

If you work the way I do, you've usually got several Windows Terminal tabs open at once — a different project in each one, each running its own Claude Code session. The problem is that every tab looks the same. You switch to one and have to stop and work out where you are: which project is this, which branch am I on, and how much has this session cost so far?

A custom status line fixes that. It sits at the bottom of each tab like a sticky footer and answers those questions at a glance, without you typing anything. Claude Code already sends your script plenty of data to work with — the model, folder, git status, session cost, and more — it just doesn't show much of it by default.

By the end you'll have something like this:

```
✦ Sonnet 4.6 │ 📁 my-project │ ⎇ main +1 ~2 │ ⇄ PR #42

▓▓▓▓▓▓▓░░░░░ 55% │ $0.34 │ ⏱ 3m5s │ ⚙ high │ 5h:24%
```

The first line answers "where am I?" — the model, the folder, the git status, and any open PR. The second line answers "how is this session going?" — a bar for context usage, plus cost, time spent, reasoning effort, and rate limit.

## What Data You Get

After most replies, Claude Code runs your script and sends it a JSON object through standard input. These are the fields worth knowing about:

| Field | What it gives you |
|---|---|
| `model.display_name` | Current model, e.g. `"Sonnet 4.6"` |
| `workspace.current_dir`, `cwd` | Working directory |
| `context_window.used_percentage` | How full the context window is (0–100) |
| `cost.total_cost_usd` | Estimated session cost |
| `cost.total_duration_ms` | Wall-clock session time |
| `effort.level` | Current reasoning effort (`low`/`medium`/`high`/etc.) |
| `rate_limits.five_hour.used_percentage` | Pro/Max rate limit usage |
| `pr.number`, `pr.review_state` | Open PR for the current branch, if any |

Git details aren't included in this data — you get those by running `git` yourself in the working folder.

## Step 1: Set Up settings.json

Add a `statusLine` entry to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "node \"C:/Users/<you>/.claude/statusline-command.js\""
  }
}
```

On Windows, Claude Code runs this through Git Bash if you have it installed, or PowerShell if you don't. One thing to watch out for: Git Bash treats backslashes as special characters, so a path like `C:\Users\...` gets broken and the command fails without showing any error. Use **forward slashes** instead — they work in both Git Bash and PowerShell. With forward slashes you can point `node` straight at the script and skip any `.sh` or `.ps1` wrapper.

## Step 2: The Script

Save this as `~/.claude/statusline-command.js`. It reads the JSON from standard input, builds the first line (model, folder, git), then the second line (context bar, cost, time, effort, rate limit).

```javascript
#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const CYAN = '\x1b[36m';
const BLUE = '\x1b[34m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RED = '\x1b[31m';
const MAGENTA = '\x1b[35m';
const GRAY = '\x1b[90m';

const SEP = `${DIM} │ ${RESET}`;

let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  let data;
  try {
    data = JSON.parse(input);
  } catch (e) {
    data = {};
  }

  const modelName = (data.model && data.model.display_name) || 'Claude';
  const cwd = (data.workspace && data.workspace.current_dir) || data.cwd || process.cwd();
  const dirName = path.basename(cwd);

  // ---- Line 1: model, directory, git ----
  const line1 = [];
  line1.push(`${BOLD}${CYAN}✦ ${modelName}${RESET}`);
  line1.push(`${BLUE}📁 ${dirName}${RESET}`);

  const gitOpts = { cwd, stdio: ['ignore', 'pipe', 'ignore'], encoding: 'utf8' };
  try {
    let branch = execSync('git --no-optional-locks branch --show-current', gitOpts).trim();
    let detached = false;
    if (!branch) {
      branch = execSync('git --no-optional-locks rev-parse --short HEAD', gitOpts).trim();
      detached = true;
    }

    if (branch) {
      const statusOut = execSync('git --no-optional-locks status --porcelain', gitOpts);
      const statusLines = statusOut.split('\n').filter(Boolean);

      let staged = 0, modified = 0, untracked = 0;
      for (const l of statusLines) {
        if (l.startsWith('??')) untracked++;
        else {
          if (l[0] !== ' ') staged++;
          if (l[1] !== ' ') modified++;
        }
      }
      const dirty = statusLines.length > 0;
      const branchColor = dirty ? YELLOW : GREEN;
      const icon = detached ? '➦' : '⎇';

      let gitStr = `${branchColor}${icon} ${branch}${RESET}`;

      const badges = [];
      if (staged) badges.push(`${GREEN}+${staged}${RESET}`);
      if (modified) badges.push(`${YELLOW}~${modified}${RESET}`);
      if (untracked) badges.push(`${GRAY}?${untracked}${RESET}`);
      if (badges.length) gitStr += ` ${badges.join(' ')}`;
      else gitStr += ` ${GREEN}✓${RESET}`;

      try {
        const counts = execSync(
          'git --no-optional-locks rev-list --left-right --count HEAD...@{upstream}',
          gitOpts
        ).trim();
        const match = counts.match(/^(\d+)\s+(\d+)$/);
        if (match) {
          const ahead = parseInt(match[1], 10);
          const behind = parseInt(match[2], 10);
          if (ahead) gitStr += ` ${CYAN}↑${ahead}${RESET}`;
          if (behind) gitStr += ` ${RED}↓${behind}${RESET}`;
        }
      } catch (e) {
        // no upstream, skip
      }

      line1.push(gitStr);
    }
  } catch (e) {
    // not a git repo, skip
  }

  if (data.pr && data.pr.number) {
    const reviewColors = {
      approved: GREEN,
      changes_requested: RED,
      pending: YELLOW,
      draft: GRAY,
    };
    const c = reviewColors[data.pr.review_state] || MAGENTA;
    line1.push(`${c}⇄ PR #${data.pr.number}${RESET}`);
  }

  console.log(line1.join(SEP));

  // ---- Line 2: context bar, cost, duration, effort ----
  const pct = Math.floor((data.context_window && data.context_window.used_percentage) || 0);
  const barWidth = 12;
  const filled = Math.round((pct * barWidth) / 100);
  const empty = barWidth - filled;
  const barColor = pct >= 90 ? RED : pct >= 70 ? YELLOW : GREEN;
  const bar = `${barColor}${'▓'.repeat(filled)}${GRAY}${'░'.repeat(empty)}${RESET}`;

  const line2 = [`${bar} ${pct}%`];

  const cost = (data.cost && data.cost.total_cost_usd) || 0;
  const durationMs = (data.cost && data.cost.total_duration_ms) || 0;
  if (cost > 0) {
    line2.push(`${YELLOW}$${cost.toFixed(2)}${RESET}`);
  }
  if (durationMs > 0) {
    const totalSec = Math.floor(durationMs / 1000);
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    line2.push(`${DIM}⏱ ${mins}m${secs}s${RESET}`);
  }

  if (data.effort && data.effort.level) {
    line2.push(`${DIM}⚙ ${data.effort.level}${RESET}`);
  }

  const fiveH = data.rate_limits && data.rate_limits.five_hour && data.rate_limits.five_hour.used_percentage;
  if (fiveH != null) {
    line2.push(`${DIM}5h:${Math.round(fiveH)}%${RESET}`);
  }

  console.log(line2.join(SEP));
});
```

## A Few Design Choices

A few small decisions that make this nicer to use every day:

- **Show a part only when there's something to show.** No git repo? The first line just skips the branch part. No cost yet at the start of a session? The second line leaves out `$0.00`. An empty segment looks worse than no segment at all.
- **Colors mean something.** The branch name is green when your working tree is clean and yellow when it isn't. The context bar goes green → yellow → red at 70% and 90%, so one glance tells you how full things are getting. Staged, modified, and untracked files use the same `+` / `~` / `?` marks as `git status`, so it reads instantly if you already know git.
- **Detached HEAD gets its own icon** (`➦` instead of `⎇`) — handy when you're mid-rebase or checked out a commit and forgot.
- **The PR review state has its own color** — red for changes requested, green for approved — so you can see if your last push got flagged without switching over to GitHub.

## Testing Without Restarting Claude Code

Since the script just reads standard input, you can hand it some test JSON directly. No need to restart Claude Code every time you change something:

```powershell
$json = @{
  model = @{ display_name = "Sonnet 4.6" }
  workspace = @{ current_dir = "C:\Code\my-project" }
  context_window = @{ used_percentage = 78 }
  cost = @{ total_cost_usd = 0.34; total_duration_ms = 185000 }
  effort = @{ level = "high" }
} | ConvertTo-Json -Depth 5

$json | node "C:\Users\<you>\.claude\statusline-command.js"
```

Run it inside a git repo to see the branch and status part, and from a clean checkout to check the `✓` and the colors. This is much faster than editing, restarting Claude Code, and waiting for the next reply to refresh the bar.

## A Few Things to Watch Out For

- **Git commands need to be fast.** The status line runs after most replies, so a slow `git status` in a big repo will make the UI lag. `--no-optional-locks` keeps git from waiting on other git processes. If your repo is big enough that `status --porcelain` is still slow on its own, look at the caching pattern in the [official docs](https://code.claude.com/docs/en/statusline#cache-expensive-operations) — save the result to a temp file keyed by `session_id` and refresh it every few seconds.
- **If the JSON doesn't parse, it fails quietly.** If standard input doesn't parse, `data` falls back to `{}` and you get a plain `✦ Claude` with no folder or git info. That's on purpose — a broken status line shouldn't dump errors into your terminal — but it also means a typo in your config can be hard to spot. If the bar looks oddly empty, pipe some known-good JSON through the script by hand to check.
- **Windows paths in `settings.json`.** Use forward slashes (`C:/Users/...`), not backslashes. Git Bash strips backslashes and the command fails silently, which is no fun to debug. If your username has a space in it, keep the path inside escaped quotes like the example above.
- **`statusline skipped · restart to fix`.** Seeing this instead of your status line? You haven't accepted the workspace trust prompt for this folder yet. And accepting it isn't enough on its own — you have to restart Claude Code before the status line shows up.

## Key Takeaways

- Claude Code hands your script a lot of data — model, folder, cost, context usage, rate limits, PR state — and your script decides what to show.
- Two lines split nicely into "where am I" (model, folder, git, PR) and "how's this session going" (context, cost, time, effort).
- Use color to show state (clean vs. dirty, under vs. over a limit), not just for looks.
- Test by piping sample JSON straight into the script — no need to restart Claude Code each time.

## Further Reading

- [Customize your status line – Claude Code Docs](https://code.claude.com/docs/en/statusline)
- [ccstatusline – community pre-built status line themes](https://github.com/sirmalloc/ccstatusline)
