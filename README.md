# YouTube Research Skills for Claude Code

Three Claude Code skills that work together as a fully automated YouTube research pipeline: search YouTube → load videos into NotebookLM → AI analysis → styled HTML report.

```
youtube-search  ──►  youtube-research-pipeline  ──►  notebooklm
  (find videos)         (orchestrate pipeline)       (AI analysis + output)
```

---

## Skills

### `youtube-search`
Search YouTube using `yt-dlp` and return structured results with metadata and an **engagement ratio** (views ÷ subscribers) — a signal for viral reach beyond a channel's existing audience.

**Invoke with:** *"Search YouTube for X"*, *"Find the top videos about Y from the last 3 months"*, *"What's everyone watching about Z on YouTube?"*

### `youtube-research-pipeline`
End-to-end research pipeline: YouTube search → NotebookLM notebook → AI analysis → ranked HTML report with foldable transcript key points. Handles the entire workflow from a single prompt.

**Invoke with:** *"Research [topic] using YouTube"*, *"Find and analyze YouTube videos about X"*, *"YouTube research pipeline for Y"*

### `notebooklm`
Automate Google NotebookLM via the `notebooklm-py` CLI and Python API. Create notebooks, add sources (URLs, PDFs, YouTube videos, Google Drive), run Q&A, and generate podcasts, quizzes, flashcards, slide decks, infographics, mind maps, reports, and more.

**Invoke with:** *"Create a NotebookLM notebook from these sources"*, *"Generate a podcast from my docs"*, *"Make flashcards from this research"*, *"Ask NotebookLM about X"*

---

## Prerequisites

| Requirement | Install |
|---|---|
| [Claude Code](https://claude.ai/code) | Download the desktop app or CLI |
| Python 3.9+ | [python.org](https://www.python.org) |
| `yt-dlp` | `pip install yt-dlp` |
| `notebooklm-py` | `pip install notebooklm-py "notebooklm-py[browser]"` |
| Playwright (Chromium) | `playwright install chromium` |
| Google account | For NotebookLM authentication |

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/andregit2026/Youtube-Research.git
cd Youtube-Research
```

### 2. Copy the skills to Claude Code

Skills must live inside a `.claude/skills/` directory that Claude Code walks up from your working directory (or in your global user-level config).

**Option A — Copy to your project:**
```bash
# From inside your project folder
cp -r /path/to/Youtube-Research/.claude/skills/youtube-search         .claude/skills/
cp -r /path/to/Youtube-Research/.claude/skills/youtube-research-pipeline .claude/skills/
cp -r /path/to/Youtube-Research/.claude/skills/notebooklm              .claude/skills/
```

**Option B — Copy to your global user-level skills (available in ALL projects):**
```bash
# macOS / Linux
cp -r .claude/skills/youtube-search         ~/.claude/skills/
cp -r .claude/skills/youtube-research-pipeline ~/.claude/skills/
cp -r .claude/skills/notebooklm              ~/.claude/skills/

# Windows (Git Bash)
cp -r .claude/skills/youtube-search         ~/AppData/Roaming/Claude/skills/
cp -r .claude/skills/youtube-research-pipeline ~/AppData/Roaming/Claude/skills/
cp -r .claude/skills/notebooklm              ~/AppData/Roaming/Claude/skills/
```

> **Tip:** Global installation (Option B) is recommended — the skills then work in every Claude Code session without copying files per project.

### 3. Install Python dependencies

```bash
pip install yt-dlp
pip install notebooklm-py "notebooklm-py[browser]"
playwright install chromium
```

### 4. Authenticate with NotebookLM (one-time)

```bash
notebooklm login
```

This opens a Chromium browser window. Log in with your Google account. Credentials are saved to `~/.notebooklm/storage_state.json` and reused automatically from then on.

---

## Quick Start

Once installed, just talk to Claude Code naturally — it detects and invokes the right skill automatically.

### Search YouTube

```
Search YouTube for "Claude Code tutorials" from the last 3 months, top 15 results
```

Claude will run the search and return a formatted table with views, duration, channel size, upload date, and engagement ratio for each video.

### Full research pipeline (search + analysis + HTML report)

```
Research "Claude Code" using YouTube — I want to understand the latest
features and what developers are actually building with it.
Give me the top 10 videos from the last 6 months.
```

Claude will:
1. Search YouTube and find the top 10 videos
2. Create a NotebookLM notebook and add all videos as sources
3. Ask NotebookLM your analysis question
4. Write a ranked HTML report (`Output/YYYYMMDD_<topic>.html`) with:
   - All videos ranked by content depth (not view count)
   - Click-to-expand key points from each transcript
   - Newest features section
   - Coverage gaps section

### NotebookLM directly

```
Create a NotebookLM notebook from these 3 PDFs and generate a podcast from them
```

```
Add this YouTube video to my existing notebook and ask it: what are the main
techniques demonstrated?
```

```
Generate flashcards from the current notebook, download them as markdown
```

---

## How the Pipeline Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                    youtube-research-pipeline                         │
│                                                                      │
│  1. YouTube Search (yt-dlp)                                         │
│     └─ search_youtube.py → top N videos with metadata + engagement  │
│                                                                      │
│  2. NotebookLM Setup                                                 │
│     └─ create notebook (or reuse existing) → add all video URLs     │
│                                                                      │
│  3. AI Analysis                                                      │
│     └─ notebooklm ask "..." --json → extract key points per video   │
│                                                                      │
│  4. HTML Report (Python generator script)                            │
│     └─ YYYYMMDD_<topic>.html                                         │
│        ├─ Sticky top nav                                             │
│        ├─ Header + meta pills + section jump buttons                 │
│        ├─ Ranked table (click row → expand transcript key points)    │
│        ├─ Newest Features section                                    │
│        └─ Gaps & Criticisms section                                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Engagement Ratio

The search skill calculates `views ÷ subscribers` for every video:

| Ratio | What it means |
|---|---|
| `> 1.0×` | Video spread beyond the channel's existing audience — strong recommendation signal |
| `0.1 – 1.0×` | Normal performance |
| `< 0.1×` | Underperformed for this channel |
| `N/A` | Subscriber count not available (small/private channel) |

### Ranking Philosophy

Videos in the HTML report are ranked by **content depth and insight quality**, not by raw view count. A 5-minute video with 1M views that covers a topic superficially ranks below a 30-minute deep-dive with 50K views. The ranking rationale note in the report explains the methodology with a concrete example.

---

## Output Files

All output is saved to an `Output/` folder in your working directory:

| File | Description |
|---|---|
| `YYYYMMDD_<topic>.html` | Styled HTML research report (self-contained, dark theme) |
| `gen_<topic>.py` | Python generator script that produced the HTML (re-runnable) |
| `yt_<topic>.json` | Raw yt-dlp search results |
| `notebooklm_response.json` | Raw NotebookLM analysis JSON |

---

## Repo Structure

```
.claude/
└── skills/
    ├── youtube-search/
    │   ├── SKILL.md                   ← Skill instructions for Claude
    │   ├── scripts/
    │   │   └── search_youtube.py      ← yt-dlp wrapper script
    │   └── evals/
    │       └── evals.json
    ├── youtube-research-pipeline/
    │   ├── SKILL.md
    │   └── evals/
    │       └── evals.json
    └── notebooklm/
        └── SKILL.md
```

---

## Troubleshooting

**`yt-dlp` returns no results or times out**
- Try widening the time window: `--months 24` instead of `--months 6`
- Reduce `--count` if fetching 50+ results is slow
- Wait a few minutes and retry if you get bot-detection errors — do not retry in a tight loop

**`notebooklm login` fails or credentials expire**
- Delete `~/.notebooklm/storage_state.json` and run `notebooklm login` again

**`UnicodeEncodeError` on Windows with emoji in video titles**
- Always pass `--json` to `notebooklm` commands and write output to a file:
  `notebooklm ask "..." --json > output.json`, then parse with `open(..., encoding="utf-8")`

**NotebookLM `source add` fails for a video**
- Private, age-restricted, or unavailable videos cannot be indexed
- Skip and continue — the pipeline logs which sources failed

**`notebooklm-py` API errors after a package update**
- Run `pip install --upgrade notebooklm-py` — the upstream API changes occasionally

---

## License

MIT — free to use, modify, and share.
