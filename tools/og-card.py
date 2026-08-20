#!/usr/bin/env python3
"""Generate social preview cards matching the existing post cards.

Template reverse-engineered from assets/img/posts/omniroute-card.png:
1200x630, dark background, Roboto Bold title over a grey subtitle,
an orange tag pill, the domain, and an orange bar along the bottom.

Usage: python tools/og-card.py [name ...]   (no args = generate all)
"""

import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (26, 26, 26)
TITLE = (245, 245, 245)
MUTED = (150, 150, 150)
ACCENT = (232, 118, 71)

MARGIN = 80
BAR_H = 12

FONTS = "C:/Windows/Fonts/"
BOLD = FONTS + "Roboto-Bold.ttf"
REGULAR = FONTS + "Roboto-Regular.ttf"

# name -> (title, subtitle, tags). Title wraps to at most two lines, so keep it
# short and let the subtitle carry the rest.
CARDS = {
    "gemini-vscode-card": (
        "Google Gemini in VSCode",
        "A quick setup guide for the terminal",
        ["gemini", "vscode", "setup"],
    ),
    "mcp-servers-card": (
        "Building MCP Servers",
        "A practical guide for .NET developers",
        ["mcp", "dotnet", "minimal apis"],
    ),
    "copilot-agents-card": (
        "Copilot Has Two Agents",
        "Most developers use the wrong one",
        ["copilot", "agent mode", "github"],
    ),
    "statusline-card": (
        "A Two-Line Status Line",
        "Model, folder, git and cost at a glance",
        ["claude code", "statusline", "node"],
    ),
    "google-drive-card": (
        "A Decade of Drive Chaos",
        "Auditing and reorganizing 642 files with Claude",
        ["claude", "google drive", "cleanup"],
    ),
    "claude-design-card": (
        "How I Am Using Claude Design",
        "Every screen on one canvas, then handed to Claude Code",
        ["claude design", "ux", "mcp"],
    ),
    "welcome-card": (
        "Arun Endapally",
        "Architecture, cloud, and getting real value from AI",
        ["architecture", "cloud", "ai"],
    ),
}


def wrap(text, font, max_width, max_lines):
    """Greedy word wrap. Raises if the text cannot fit in max_lines."""
    lines, words = [], text.split()
    while words:
        line = words.pop(0)
        while words and font.getlength(f"{line} {words[0]}") <= max_width:
            line += " " + words.pop(0)
        lines.append(line)
    if len(lines) > max_lines or any(font.getlength(l) > max_width for l in lines):
        raise ValueError(f"{text!r} does not fit in {max_lines} line(s)")
    return lines


def render(name, title, subtitle, tags):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(BOLD, 92)
    sub_font = ImageFont.truetype(REGULAR, 40)
    pill_font = ImageFont.truetype(REGULAR, 26)
    domain_font = ImageFont.truetype(REGULAR, 26)

    max_text = W - 2 * MARGIN

    # The title block grows upward from the subtitle so that one- and two-line
    # titles both leave the same gap above the pill.
    sub_top, line_h = 375, 124
    lines = wrap(title, title_font, max_text, 2)
    y = sub_top - 12 - line_h * len(lines)
    for line in lines:
        d.text((MARGIN, y), line, font=title_font, fill=TITLE)
        y += line_h

    if sub_font.getlength(subtitle) > max_text:
        raise ValueError(f"subtitle {subtitle!r} is too wide for the card")
    d.text((MARGIN, sub_top), subtitle, font=sub_font, fill=MUTED)

    # Tag pill, anchored to the bottom of the card rather than the title.
    label = "  ·  ".join(tags)
    pill_w = pill_font.getlength(label) + 60
    pill_top, pill_bot = 455, 505
    d.rounded_rectangle(
        [MARGIN, pill_top, MARGIN + pill_w, pill_bot],
        radius=(pill_bot - pill_top) // 2,
        outline=ACCENT,
        width=2,
    )
    d.text(
        (MARGIN + pill_w / 2, (pill_top + pill_bot) / 2),
        label,
        font=pill_font,
        fill=ACCENT,
        anchor="mm",
    )

    d.text((MARGIN, 548), "arunendapally.com", font=domain_font, fill=MUTED)
    d.rectangle([0, H - BAR_H, W, H], fill=ACCENT)

    path = f"assets/img/posts/{name}.png"
    img.save(path)
    print(f"wrote {path}")


if __name__ == "__main__":
    names = sys.argv[1:] or CARDS.keys()
    for n in names:
        render(n, *CARDS[n])
