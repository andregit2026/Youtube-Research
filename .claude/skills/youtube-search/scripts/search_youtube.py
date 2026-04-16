#!/usr/bin/env python3
"""
YouTube search using yt-dlp with metadata and engagement metrics.

Usage:
    python search_youtube.py "query" [--count N] [--months N]
"""

import argparse
import io
import json
import subprocess
import sys
from datetime import datetime, timedelta

# Force UTF-8 output on Windows (avoids cp1252 encoding errors with emoji/accented chars)
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def format_number(n):
    """Format large numbers with K/M/B suffixes."""
    if n is None:
        return "N/A"
    n = int(n)
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_duration(seconds):
    """Format seconds into H:MM:SS or M:SS."""
    if seconds is None:
        return "N/A"
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_date(upload_date):
    """Format YYYYMMDD string to readable date like 'Jan 15, 2025'."""
    if not upload_date:
        return "N/A"
    try:
        d = datetime.strptime(str(upload_date), "%Y%m%d")
        return d.strftime("%b %d, %Y")
    except Exception:
        return str(upload_date)


def main():
    parser = argparse.ArgumentParser(
        description="Search YouTube with yt-dlp and return structured results."
    )
    parser.add_argument("query", nargs="+", help="Search query terms")
    parser.add_argument(
        "--count", type=int, default=20, help="Number of results to return (default: 20)"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=6,
        help="Filter to videos uploaded in the last N months (default: 6)",
    )
    args = parser.parse_args()

    query = " ".join(args.query)
    cutoff = datetime.now() - timedelta(days=args.months * 30)
    cutoff_str = cutoff.strftime("%Y%m%d")

    # Fetch more than needed to account for date filtering
    fetch_count = max(args.count * 4, 80)

    cmd = [
        "yt-dlp",
        f"ytsearch{fetch_count}:{query}",
        "--dump-json",
        "--no-playlist",
        "--dateafter",
        cutoff_str,
        "--quiet",
        "--no-warnings",
    ]

    print(f"Searching YouTube for: '{query}' (last {args.months} months) ...\n")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    videos = []
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            video = json.loads(line)
            videos.append(video)
        except json.JSONDecodeError:
            continue

    # Trim to requested count
    videos = videos[: args.count]

    if not videos:
        print(f"No videos found for '{query}' in the last {args.months} months.")
        if result.stderr:
            print(f"\nyt-dlp stderr:\n{result.stderr[:500]}")
        sys.exit(0)

    # ── Output ────────────────────────────────────────────────────────────────
    divider = "-" * 80
    header = f"YouTube Search Results: '{query}'"
    sub_header = f"Last {args.months} months  |  Showing {len(videos)} result(s)"

    print(header)
    print(sub_header)
    print(divider)

    for i, v in enumerate(videos, 1):
        title = v.get("title", "N/A")
        channel = v.get("channel") or v.get("uploader") or "N/A"
        subs = v.get("channel_follower_count")
        views = v.get("view_count")
        duration = v.get("duration")
        upload_date = v.get("upload_date")
        url = v.get("webpage_url") or v.get("url") or "N/A"

        # Engagement: views per subscriber
        if subs and views and int(subs) > 0:
            ratio = int(views) / int(subs)
            ratio_str = f"{ratio:.2f}x"
        else:
            ratio_str = "N/A"

        print(f"#{i:02d}  {title}")
        print(f"      Channel:    {channel}  ({format_number(subs)} subscribers)")
        print(
            f"      Views:      {format_number(views)}   "
            f"Duration: {format_duration(duration)}   "
            f"Uploaded: {format_date(upload_date)}"
        )
        print(f"      Engagement: {ratio_str} (views / subscribers)")
        print(f"      URL:        {url}")
        print(divider)

    print(
        f"\nEngagement ratio > 1.0x means the video attracted more views than the channel has subscribers."
    )


if __name__ == "__main__":
    main()
