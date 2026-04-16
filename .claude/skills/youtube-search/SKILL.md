---
name: youtube-search
description: >
  Search YouTube and return structured video results with metadata and engagement metrics.
  Use this skill whenever the user wants to search YouTube, find videos, research channels,
  compare video performance, analyze YouTube trends, or get video metadata like views,
  subscribers, duration, or upload date. Also use it when the user mentions yt-dlp,
  wants to find the most popular or most engaging videos on a topic, needs YouTube
  analytics data, or asks about video content discovery. Trigger even if the user says
  things like "look up YouTube videos about X", "find me some videos on Y", or "what
  are people watching about Z on YouTube".
compatibility:
  tools: [Bash]
  dependencies: [yt-dlp]
---

# YouTube Search Skill

Search YouTube using `yt-dlp` and return structured results with rich metadata and an
engagement metric — all formatted for easy scanning.

---

## Prerequisites

Check that `yt-dlp` is installed before running the script:

```bash
yt-dlp --version
```

If it's missing, install it:

```bash
pip install yt-dlp
```

---

## The search script

The bundled script is at `scripts/search_youtube.py` (relative to this skill's directory).
Run it from the command line:

```bash
python scripts/search_youtube.py "your search query" [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--count` | 20 | Number of results to return |
| `--months` | 6 | Filter to videos uploaded in the last N months |

**Examples:**

```bash
# Top 20 results from the last 6 months (default)
python scripts/search_youtube.py "rust programming tutorial"

# Top 10 results, last 3 months
python scripts/search_youtube.py "AI agents 2025" --count 10 --months 3

# 30 results, no time filter (set months high)
python scripts/search_youtube.py "cooking pasta" --count 30 --months 120
```

---

## What the output looks like

Each result is separated by a horizontal divider and shows:

```
YouTube Search Results: 'python tutorial'
Last 6 months  |  Showing 20 result(s)
────────────────────────────────────────────────────────────────────────────────
#01  Python for Beginners – Full Course
      Channel:    Tech With Tim  (1.2M subscribers)
      Views:      890.5K   Duration: 1:42:15   Uploaded: Nov 03, 2025
      Engagement: 0.74x (views / subscribers)
      URL:        https://www.youtube.com/watch?v=...
--------------------------------------------------------------------------------
```

**Engagement ratio** = `views / subscribers`.
- Values **above 1.0x**: the video attracted more views than the channel's subscriber
  base — a strong signal of recommendation performance or viral reach.
- Values **below 0.1x**: the video underperformed relative to the channel's audience.
- `N/A`: subscriber count was not available.

---

## Workflow

When a user asks you to search YouTube, follow these steps:

1. Identify the **query** and any constraints the user mentioned (time window, result count).
2. Resolve the path to `search_youtube.py`:
   - It lives at `scripts/search_youtube.py` inside this skill's directory.
   - Use `Glob` or your own knowledge of where skills live to find the absolute path.
3. Verify `yt-dlp` is available (`yt-dlp --version`); install if missing.
4. Run the script with the appropriate arguments.
5. Present the output to the user as-is — the script already formats it nicely.
6. Offer follow-up actions:
   - Sort by engagement, views, or subscriber count (post-process the raw JSON).
   - Filter to a specific channel.
   - Look up a specific video in more detail with `yt-dlp --dump-json <url>`.

---

## Handling edge cases

- **No results returned**: Try widening the time window (`--months 24`) or simplifying the query.
- **Subscriber count is N/A**: YouTube sometimes omits subscriber data for small or private-ish channels; the engagement ratio will be `N/A` for those.
- **Slow / timeout**: yt-dlp can be slow on large fetch counts. If `--count 20` + `--months 6` is timing out, reduce `--count` or widen `--months` to reduce the internal multiplier.
- **Rate limiting**: If yt-dlp returns errors about rate limits or bot detection, wait a few minutes and try again. Do not scrape in a tight loop.

---

## Sorting and post-processing

If the user wants results ranked differently (e.g., by engagement ratio rather than YouTube's default relevance order), run the script with a higher `--count` and then sort in Python:

```python
import json, subprocess

result = subprocess.run(
    ["yt-dlp", "ytsearch50:your query", "--dump-json", "--quiet"],
    capture_output=True, text=True
)
videos = [json.loads(l) for l in result.stdout.strip().split("\n") if l]
videos.sort(key=lambda v: (v.get("view_count") or 0) / max(v.get("channel_follower_count") or 1, 1), reverse=True)
```
