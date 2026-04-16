---
name: notebooklm
description: >
  Automate Google NotebookLM using the notebooklm-py CLI and Python API.
  Use this skill whenever the user wants to create or manage NotebookLM notebooks,
  add sources (URLs, PDFs, YouTube videos, Google Drive docs), ask questions about
  their documents, or generate any kind of content from notebooks — podcasts, videos,
  quizzes, flashcards, slide decks, infographics, mind maps, data tables, or reports.
  Also trigger when the user mentions "NotebookLM", "notebook podcast", "audio overview",
  "generate a quiz from my docs", "study guide", "briefing doc", or anything that
  involves feeding documents to AI and getting structured output. This skill covers
  the full notebooklm-py CLI (shell commands) and Python async API.
compatibility:
  tools: [Bash]
  dependencies: [notebooklm-py]
---

# NotebookLM Skill

Automate Google NotebookLM via `notebooklm-py` — an unofficial Python SDK and CLI
that exposes features not available in the web UI (batch downloads, PPTX export, etc.).

---

## Setup

### Install
```bash
pip install notebooklm-py          # CLI + Python API
pip install "notebooklm-py[browser]"  # Required for initial browser login
playwright install chromium
```

### Authenticate (one-time)
```bash
notebooklm login    # Opens Chromium; log in with your Google account
```
After login, credentials are saved to `~/.notebooklm/storage_state.json`.
Subsequent commands use stored credentials automatically (`NotebookLMClient.from_storage()` in Python).

### Check status
```bash
notebooklm status   # Shows active notebook and conversation context
```

---

## Core workflow patterns

### Pattern 1 — Research assistant (load docs, Q&A)
```bash
notebooklm create "My Research"          # Create notebook
notebooklm use <notebook_id>             # Set as active (supports partial ID)
notebooklm source add https://example.com --wait
notebooklm source add ./paper.pdf
notebooklm ask "What are the key themes?"
notebooklm ask "Compare the methodologies" --save-as-note
```

### Pattern 2 — Generate a podcast from sources
```bash
notebooklm use <notebook_id>
notebooklm generate audio "deep dive, casual tone" --format deep-dive --wait
notebooklm download audio ./podcast.mp3
```

### Pattern 3 — Build a study kit
```bash
notebooklm use <notebook_id>
notebooklm generate quiz "focus on key concepts" --difficulty hard --wait
notebooklm generate flashcards --quantity more --wait
notebooklm generate report --format study-guide --wait
notebooklm download quiz ./quiz.json
notebooklm download flashcards ./flashcards.md --format markdown
notebooklm download report ./study-guide.md
```

### Pattern 4 — Create a presentation
```bash
notebooklm generate slide-deck "executive summary" --format presenter --wait
notebooklm download slide-deck ./slides.pptx --format pptx
```

### Pattern 5 — Auto-research a topic and generate content
```bash
notebooklm source add-research "quantum computing" --mode deep --import-all
notebooklm research wait
notebooklm generate report --format briefing-doc --wait
```

---

## Command reference

### Notebook management
```bash
notebooklm list                         # List all notebooks
notebooklm create "Name"                # Create notebook
notebooklm use <id>                     # Set active notebook (partial ID OK)
notebooklm rename <id> "New Name"
notebooklm delete <id>
notebooklm summary                      # AI-generated notebook summary
```

### Sources
```bash
notebooklm source add <url|file|"text"> [--title "Title"] [--wait]
notebooklm source add <youtube_url>     # YouTube auto-detected
notebooklm source add-drive <drive_url> # Google Drive doc
notebooklm source add-research "query" [--from web|drive] [--mode fast|deep] [--import-all]
notebooklm source list
notebooklm source get <source_id>
notebooklm source guide <source_id>     # AI-generated source summary + keywords
notebooklm source fulltext <source_id>  # Full indexed text
notebooklm source refresh <source_id>   # Re-fetch URL/Drive source
notebooklm source delete <source_id>
```

Source types are auto-detected from content. Use `--type url|text|file|youtube` to override.

### Chat
```bash
notebooklm ask "question"               # Ask the active notebook
notebooklm ask "question" --json        # Structured output with source references [1][2]
notebooklm ask "question" -s <src_id>   # Limit to specific sources (repeatable)
notebooklm ask "question" --save-as-note [--note-title "Title"]
notebooklm history                      # Show conversation history
```

### Content generation
All `generate` commands support `--wait` (block until done) and `--json` (structured output).
Use `--no-wait` to kick off and check status later.

```bash
# Audio overview (podcast)
notebooklm generate audio ["description"] [--format deep-dive|brief|critique|debate]
    [--length short|default|long] [--language <code>] [-s <source_id>]

# Video
notebooklm generate video ["description"] [--format explainer|brief]
    [--style auto|classic|whiteboard|kawaii|anime|watercolor|retro-print|heritage|paper-craft]
    [--language <code>]

# Quiz
notebooklm generate quiz ["description"] [--difficulty easy|medium|hard]
    [--quantity fewer|standard|more]

# Flashcards
notebooklm generate flashcards ["description"] [--difficulty easy|medium|hard]
    [--quantity fewer|standard|more]

# Slide deck
notebooklm generate slide-deck ["description"] [--format detailed|presenter]
    [--length default|short]

# Report
notebooklm generate report ["description"] [--format briefing-doc|study-guide|blog-post|custom]
    [--append "extra instructions"]

# Infographic
notebooklm generate infographic ["description"] [--orientation landscape|portrait|square]
    [--detail concise|standard|detailed]

# Mind map
notebooklm generate mind-map [-s <source_id>]

# Data table
notebooklm generate data-table ["description"]
```

### Downloads
```bash
notebooklm download audio <path.mp3>
notebooklm download video <path.mp4>
notebooklm download slide-deck <path> [--format pdf|pptx]
notebooklm download quiz <path> [--format json|markdown|html]
notebooklm download flashcards <path> [--format json|markdown|html]
notebooklm download report <path.md>
notebooklm download infographic <path>
notebooklm download mind-map <path.json>
notebooklm download data-table <path.csv>
```

### Research monitoring
```bash
notebooklm research status             # Non-blocking check
notebooklm research wait [--import-all] # Block until complete
```

### Notes
```bash
notebooklm note list
notebooklm note create "content" [--title "Title"]
notebooklm note get <id>
notebooklm note save <id> "new content"
notebooklm note delete <id>
```

### Sharing
```bash
notebooklm share public                # Create public link
notebooklm share add <email> [--role viewer|editor]
notebooklm share remove <email>
notebooklm share status
```

### Language
```bash
notebooklm language set <code>         # e.g. "en", "de", "ja"
notebooklm language show
```

---

## Python API

Use the async Python API when you need to integrate NotebookLM into a script,
chain operations programmatically, or process results in code.

```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with await NotebookLMClient.from_storage() as client:
        # Create and populate a notebook
        nb = await client.notebooks.create("Research")
        src = await client.sources.add_url(nb.id, "https://example.com", wait=True)

        # Q&A with structured references
        result = await client.chat.ask(nb.id, "What are the main points?")
        print(result.answer)  # answer text
        print(result.references)  # source citations

        # Generate audio and wait
        status = await client.artifacts.generate_audio(nb.id, instructions="casual and fun")
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "podcast.mp3")

asyncio.run(main())
```

Key client namespaces: `client.notebooks`, `client.sources`, `client.chat`,
`client.artifacts`, `client.notes`, `client.sharing`, `client.research`.

---

## Tips and edge cases

- **Partial IDs** — All ID arguments support prefix matching. `notebooklm use abc`
  matches `abc123def456...`. Very useful; avoids copy-pasting full UUIDs.

- **Generation is async by default** — `generate` commands return immediately unless
  you pass `--wait`. Use `notebooklm artifact poll <id>` or add `--wait` for blocking.

- **Multiple sources in one command** — Pass `-s <id>` multiple times to limit
  generation or chat to specific sources.

- **Unofficial API warning** — This uses undocumented Google APIs. If commands fail
  unexpectedly, the API may have changed. Check `pip install --upgrade notebooklm-py`.

- **Rate limits** — Use `--retry N` on generate commands for automatic exponential
  backoff if you hit rate limits.

- **Language** — Set once with `notebooklm language set <code>` and all subsequent
  generations use that language. Override per-command with `--language`.

---

## Workflow guidance

When the user describes a goal (e.g., "turn these PDFs into a podcast"), think through:

1. **Is there an active notebook?** Run `notebooklm status` to check; create/use one if not.
2. **Are sources loaded?** Run `notebooklm source list`; add anything missing with `source add`.
3. **What output format fits the goal?** Audio for passive listening, quiz/flashcards for studying,
   report for reading, slide deck for presenting, infographic for visual summary.
4. **Wait or poll?** For interactive use, `--wait` is simpler. For long jobs, use `--no-wait`
   and check `notebooklm artifact list` or `research status`.
5. **Save the output.** Always download artifacts after generation — they may expire.
