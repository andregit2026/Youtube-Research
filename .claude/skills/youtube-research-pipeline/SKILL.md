---
name: youtube-research-pipeline
description: >
  End-to-end YouTube research pipeline that combines YouTube video discovery with
  NotebookLM deep analysis. Use this skill whenever the user wants to research a
  topic using YouTube as the primary source, get AI analysis of what experts on
  YouTube are saying about something, build a knowledge base from video content,
  or turn YouTube search results into structured insights. Trigger when the user
  mentions "YouTube research pipeline", "research from YouTube", "analyze YouTube
  videos on", "YouTube + NotebookLM", "find and analyze YouTube videos about",
  or says anything like "research [topic] using YouTube" or "I want to learn
  about [X] from YouTube videos". Also trigger when the user wants to combine
  YouTube source discovery with deliverables like flashcards, infographics,
  quizzes, or study guides based on video content.
compatibility:
  tools: [Bash, Glob, Write]
  dependencies: [yt-dlp, notebooklm-py]
---

# YouTube Research Pipeline Skill

An orchestrated pipeline that: searches YouTube for relevant videos → loads them
into NotebookLM → runs AI analysis → optionally generates a deliverable → returns
a full markdown research report to the user.

---

## What you need from the user

When this skill is invoked, extract these three things from the user's message:

1. **Research topic** (required) — what to search for on YouTube
2. **Analysis goal** (required) — what question to answer or angle to explore
3. **Deliverable type** (optional) — if not mentioned, skip the deliverable step

If the user's message is ambiguous about the analysis goal (e.g., they just said
"research X"), ask one clarifying question: *"What specifically do you want to
understand or get out of this research?"* before proceeding. Don't ask about
deliverables — if they didn't mention one, just proceed without it.

### Deliverable type mapping

Map natural language to NotebookLM commands:

| User says | NotebookLM command |
|-----------|-------------------|
| flashcards / flash cards | `generate flashcards --wait` |
| quiz / questions | `generate quiz --wait` |
| infographic | `generate infographic --wait` |
| mind map | `generate mind-map --wait` |
| podcast / audio | `generate audio --wait` |
| slides / presentation / slide deck | `generate slide-deck --wait` |
| report / briefing / summary | `generate report --format briefing-doc --wait` |
| study guide | `generate report --format study-guide --wait` |
| data table | `generate data-table --wait` |

---

## Step-by-step workflow

### Step 1 — YouTube search

Find the `search_youtube.py` script from the youtube-search skill using Glob:

```bash
# Find the script
glob pattern: "**/youtube-search/scripts/search_youtube.py"
```

Run it with `--count 10 --months 24` (broad window ensures good research coverage):

```bash
python <path-to>/search_youtube.py "<research topic>" --count 10 --months 24
```

**Capture the output in full** — you need both the human-readable formatted text
AND structured data (URLs + metadata) for the report. Parse each result block to
extract:
- Title
- Channel name + subscriber count
- View count
- Duration
- Upload date
- Engagement ratio
- URL

If fewer than 10 results come back, that's fine — use what you got. If 0 results,
try widening to `--months 60` before giving up.

### Step 2 — Create the NotebookLM notebook

```bash
notebooklm create "<Research Topic> - YouTube Research"
notebooklm use <notebook_id>
```

Name it clearly after the topic so it's easy to find later.

### Step 3 — Add YouTube sources

Add each of the 10 video URLs as sources. YouTube URLs are auto-detected by
NotebookLM. Add them with `--wait` so each one is indexed before moving on:

```bash
notebooklm source add <youtube_url> --wait
```

Do this for all 10 videos. If a source fails to add (network error, private video),
log which one failed and continue — don't abort the whole pipeline.

### Step 4 — Run the analysis

Ask NotebookLM the user's analysis question. Save it as a note for reference:

```bash
notebooklm ask "<analysis goal>" --save-as-note --note-title "Research Analysis"
```

For richer output with source references, also use `--json`:

```bash
notebooklm ask "<analysis goal>" --json
```

Capture the full answer text.

### Step 5 — Generate deliverable (if requested)

If the user asked for a deliverable, generate and download it:

```bash
notebooklm generate <command> --wait
notebooklm download <type> ./<topic-slug>-<deliverable-type>.<ext>
```

Use a clean filename slug: lowercase, spaces replaced with hyphens, no special chars.
For example: `ai-agents-2025-flashcards.md` or `quantum-computing-quiz.json`.

### Step 6 — Compile the research report

Write a markdown report to `<topic-slug>-research-report.md` in the current working
directory. Then present the full content inline in chat too.

### Step 7 — Generate HTML report

Always generate an HTML version of the markdown report. Write it to
`<topic-slug>-research-report.html` in the same directory, then open it:

```bash
start <topic-slug>-research-report.html   # Windows
```

**HTML design rules:**
- Dark theme: background `#0d1117`, text `#e2e8f0`, cards `#161b27`
- Fixed sidebar nav with anchor links to each section
- Color-coded sections (one accent color per major topic/chapter)
- Tables for structured data (sources, metadata, transformations)
- Numbered step lists with counter styling for how-to sequences
- Code blocks with monospace font for commands and examples
- `meta-pills` strip in the header showing date, source count, notebook ID
- Footer: "Generiert von youtube-research-pipeline skill - Claude Code - <date>"
- All external links open in `target="_blank"`
- Fully self-contained — no external CSS or JS dependencies

**Section color palette** (cycle through for multi-topic reports):
- Topic 1: amber `#f59e0b`
- Topic 2: indigo `#818cf8`
- Topic 3: emerald `#34d399`
- Topic 4: red `#f87171`
- Topic 5+: purple `#c084fc`

---

## Report format

Use this exact template (fill in all placeholders):

```markdown
# Research Report: <Research Topic>

**Date:** <today's date>
**Analysis goal:** <user's stated analysis goal>
**NotebookLM notebook:** <notebook_id>

---

## YouTube Sources

> 10 videos found via yt-dlp search: "<query>" | Last 24 months

| # | Title | Channel | Views | Duration | Uploaded | Engagement | URL |
|---|-------|---------|-------|----------|----------|------------|-----|
| 1 | <title> | <channel> (<subs>) | <views> | <duration> | <date> | <ratio>x | [Link](<url>) |
...

### Source Details

For each video, include a brief entry:
**#01 — <Title>**
- Channel: <name> | <subs> subscribers
- Views: <views> | Duration: <duration> | Uploaded: <date>
- Engagement: <ratio>x
- URL: <url>

---

## Analysis

> Question: <analysis goal>

<Full answer from NotebookLM, including any source references>

---

## Deliverable

> Type: <deliverable type> — saved to `./<filename>`

<If no deliverable was requested, omit this section entirely>

---

## Search Metadata

| Field | Value |
|-------|-------|
| Search query | <query used> |
| Tool | yt-dlp |
| Results requested | 10 |
| Results retrieved | <N> |
| Time window | Last 24 months |
| Search date | <today> |
| Sources successfully added to NotebookLM | <N of 10> |
| NotebookLM notebook ID | <id> |
| Deliverable generated | <Yes / No> |
```

---

## Error handling

- **yt-dlp not installed**: Run `pip install yt-dlp` before the search step
- **NotebookLM not authenticated**: Run `notebooklm login` and ask the user to complete browser login, then resume
- **Source add failure**: Skip that video, note it in "Search Metadata" under a "Failed sources" row
- **Analysis returns empty**: Retry once with a slightly rephrased version of the analysis goal

---

## Tips for good results

- Use the user's research topic verbatim as the search query; only clean up obviously
  problematic characters (quotes, slashes)
- When asking NotebookLM the analysis question, frame it to leverage video content:
  "Based on the YouTube videos in this notebook, <analysis goal>"
- The engagement ratio in the YouTube output is a signal — videos above 1.0x often
  contain information that spread beyond the channel's existing audience, which
  can indicate particularly high-value or novel content
