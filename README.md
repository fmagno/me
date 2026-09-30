# portfolio

Francisco's CV and landing page, generated from markdown.

```
make          # -> dist/cv.pdf (2-page A4) + dist/index.html
make serve    # preview on http://localhost:8765
```

Requires `uv` (dependencies are declared inline in `build.py`) and the system libraries
WeasyPrint needs (`brew install pango`).

## Where to edit

| File | Drives |
|---|---|
| `content/profile.md` | name, headline, contact, 4 metrics, career arc, summary (body) |
| `content/highlights/NN-*.md` | featured work: frontmatter + `### Role` / `### Actions` / `### Impact` |
| `content/experience/NN-*.md` | roles; `featured: true` marks the current employer |
| `content/side-projects/NN-*.md` | independent work tiles (`url` optional) |
| `content/skills.md` | one `## Label` per skill row |
| `content/education.md` | degree + languages |
| `drafts/` | content cut to keep the PDF at 2 pages (not built) |
| `templates/cv.html.j2` | print layout (WeasyPrint) |
| `templates/site.html.j2` | screen layout |

`NN-` prefixes set the order. Inline markdown works everywhere; `**bold**` renders in the
ink-blue accent. After content edits, re-check the PDF stays at 2 pages:

```
python3 ~/.claude/plugins/cache/kami/kami/*/scripts/build.py --check-resume-balance dist/cv.pdf
```

Design: [kami](https://github.com/tw93/kami) tokens (parchment, ink blue, Charter), MIT.
Source material: `agent81/repo/cv_rag_system/corpus`, the old Hugo site (fmagno/me), beans history.
