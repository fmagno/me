#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-frontmatter>=1.1",
#   "markdown>=3.6",
#   "jinja2>=3.1",
#   "weasyprint>=62",
# ]
# ///
"""Render content/*.md into dist/cv.pdf (print) and dist/index.html (landing page).

    ./build.py            # build everything
    ./build.py pdf        # CV only  (dist/cv.html + dist/cv.pdf)
    ./build.py site       # landing page only (dist/index.html)
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import date
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


# ---------- markdown helpers ----------

def md(text: str) -> str:
    return markdown.markdown(text.strip(), extensions=["smarty"])


def mdi(text: str) -> str:
    """Inline markdown: render and strip the wrapping <p>."""
    html = md(text)
    return re.sub(r"^<p>(.*)</p>$", r"\1", html, flags=re.S)


def sections(body: str, level: int) -> dict[str, str]:
    """Split a markdown body on headings of the given level -> {heading: content}."""
    marker = "#" * level + " "
    out: dict[str, str] = {}
    current = None
    for line in body.splitlines():
        if line.startswith(marker):
            current = line[len(marker):].strip()
            out[current] = ""
        elif current is not None:
            out[current] += line + "\n"
    return {k: v.strip() for k, v in out.items()}


def fmt_date(value) -> str:
    s = str(value)
    if s.lower() == "present":
        return "Present"
    m = re.fullmatch(r"(\d{4})-(\d{2})", s)
    return f"{MONTHS[int(m.group(2)) - 1]} {m.group(1)}" if m else s


def fmt_year(value) -> str:
    s = str(value)
    return "Present" if s.lower() == "present" else s[:4]


# ---------- loading ----------

def load(path: Path) -> tuple[dict, str]:
    post = frontmatter.load(path)
    return dict(post.metadata), post.content


def load_dir(name: str) -> list[dict]:
    items = []
    for path in sorted((CONTENT / name).glob("*.md")):
        meta, body = load(path)
        items.append({**meta, "body": body, "slug": path.stem})
    return items


def load_all() -> dict:
    profile, summary = load(CONTENT / "profile.md")
    skills_meta, skills_body = load(CONTENT / "skills.md")
    education, _ = load(CONTENT / "education.md")

    highlights = load_dir("highlights")
    for h in highlights:
        h["parts"] = sections(h["body"], 3)  # Role / Actions / Impact
        h["lead"] = re.split(r"(?m)^### ", h["body"], maxsplit=1)[0].strip()  # text before the first heading

    experience = load_dir("experience")
    return {
        "p": profile,
        "summary": summary,
        "highlights": highlights,
        "current": [e for e in experience if e.get("featured")],
        "earlier": [e for e in experience if not e.get("featured")],
        "side": load_dir("side-projects"),
        "skills": sections(skills_body, 2),
        "skills_title": skills_meta.get("title", "Skills"),
        "edu": education,
        "built": date.today().isoformat(),
    }


# ---------- rendering ----------

def env() -> Environment:
    e = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    e.filters.update(md=md, mdi=mdi, date=fmt_date, year=fmt_year)
    return e


def build_pdf(ctx: dict) -> None:
    from weasyprint import HTML

    html = env().get_template("cv.html.j2").render(**ctx)
    (DIST / "cv.html").write_text(html)
    doc = HTML(string=html, base_url=str(ROOT)).render()
    doc.write_pdf(DIST / "cv.pdf")
    print(f"dist/cv.pdf  ({len(doc.pages)} pages)")


def build_site(ctx: dict) -> None:
    html = env().get_template("site.html.j2").render(**ctx)
    (DIST / "index.html").write_text(html)
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    (DIST / ".nojekyll").write_text("")  # GitHub Pages: serve files as-is
    print("dist/index.html")


def main(argv: list[str]) -> None:
    target = argv[1] if len(argv) > 1 else "all"
    if target not in {"all", "pdf", "site"}:
        sys.exit(__doc__)
    DIST.mkdir(exist_ok=True)
    ctx = load_all()
    if target in {"all", "pdf"}:
        build_pdf(ctx)
    if target in {"all", "site"}:
        build_site(ctx)


if __name__ == "__main__":
    main(sys.argv)
