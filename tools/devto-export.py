#!/usr/bin/env python3
"""Convert a Chirpy post into markdown ready to paste into the dev.to editor.

Chirpy's kramdown attribute blocks ({: file="..." }, {: .prompt-tip }, image
sizing) mean nothing to dev.to and would show up as literal text, and relative
paths would 404 there. This rewrites all of that and emits dev.to front matter
with a canonical_url pointing back at the blog.

dev.to does not render mermaid, so those blocks keep their source and gain a
line pointing at the rendered diagram on the canonical post.

Usage: python tools/devto-export.py [slug ...]   (no args = all configured)
"""

import re
import sys
from pathlib import Path

SITE = "https://arunendapally.com"
# `tools` is in _config.yml's exclude list, so these never reach the build.
OUT = Path("tools/devto")

# dev.to allows at most four tags and they must be alphanumeric, so the post's
# own tag list cannot be reused directly. One broad high-traffic tag each.
POSTS = {
    "2026-08-07-omniroute-free-tier-routing-and-compression": ["ai", "claudecode", "llm", "productivity"],
    "2026-07-24-spec-driven-development-with-spec-kit": ["ai", "claudecode", "programming", "productivity"],
    "2026-07-15-get-more-out-of-claude-memory": ["ai", "claude", "llm", "programming"],
}

ATTR = re.compile(r"^\{:\s*(.+?)\s*\}$")
FILE_ATTR = re.compile(r'file="([^"]+)"')


def split_front_matter(text):
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError("no front matter")
    fm = {}
    key = None
    for line in parts[1].splitlines():
        m = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip().strip('"')
        elif key and line.startswith(" "):
            fm[key] += " " + line.strip()
    return fm, parts[2]


def convert_body(body, canonical):
    lines = body.splitlines()
    out = []
    fence_starts = []  # index in `out` of each opening fence
    in_fence = False

    for line in lines:
        if line.startswith("```"):
            if not in_fence:
                fence_starts.append(len(out))
                in_fence = True
                if line.strip() == "```mermaid":
                    out.append(
                        f"_[Rendered diagram in the original post]({canonical})._\n"
                    )
                    fence_starts[-1] = len(out) - 1
            else:
                in_fence = False
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        m = ATTR.match(line.strip())
        if m:
            # A code block's filename label belongs above the block on dev.to.
            fm = FILE_ATTR.search(m.group(1))
            if fm and fence_starts:
                out.insert(fence_starts[-1], f"**`{fm.group(1)}`**")
            # Every other attribute block (prompt callouts, image sizing,
            # .nolineno) has no dev.to equivalent and is simply dropped.
            continue

        out.append(line)

    text = "\n".join(out)
    # Relative paths resolve against dev.to's own domain otherwise.
    text = text.replace("](/assets/", f"]({SITE}/assets/")
    text = text.replace("](/posts/", f"]({SITE}/posts/")
    return text.strip()


def convert(slug, tags):
    fm, body = split_front_matter(Path(f"_posts/{slug}.md").read_text(encoding="utf-8"))
    canonical = f"{SITE}/posts/{slug[11:]}/"

    # Titles and descriptions here contain ": ", which is a YAML parse error
    # unquoted, so both are always quoted.
    def q(s):
        return '"' + s.replace('"', "'") + '"'

    header = [
        "---",
        f"title: {q(fm['title'])}",
        "published: false",
        f"description: {q(fm['description'])}",
        f"tags: {', '.join(tags)}",
        f"canonical_url: {canonical}",
    ]
    if "image" in fm:
        header.append(f"cover_image: {SITE}{fm['image']}")
    header.append("---")

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{slug[11:]}.md"
    path.write_text("\n".join(header) + "\n\n" + convert_body(body, canonical) + "\n",
                    encoding="utf-8")
    print(f"wrote {path}  ({len(body.split())} words)")


if __name__ == "__main__":
    for s in sys.argv[1:] or POSTS:
        convert(s, POSTS[s])
