#!/usr/bin/env python3
"""
YouTube search using yt-dlp metadata extraction (no downloading).

Usage:
    python youtube_search.py <query> [count]

Output:
    JSON array of videos with title, url, channel, view_count, duration, upload_date
"""

import json
import subprocess
import sys


def search_youtube(query: str, count: int = 5) -> list[dict]:
    cmd = [
        "yt-dlp",
        f"ytsearch{count}:{query}",
        "--dump-json",
        "--skip-download",
        "--quiet",
        "--no-warnings",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Duration formatting: yt-dlp returns seconds
        duration_secs = data.get("duration")
        if duration_secs:
            mins, secs = divmod(int(duration_secs), 60)
            hrs, mins = divmod(mins, 60)
            duration_str = f"{hrs}:{mins:02d}:{secs:02d}" if hrs else f"{mins}:{secs:02d}"
        else:
            duration_str = data.get("duration_string", "")

        # Upload date: yt-dlp returns YYYYMMDD
        raw_date = data.get("upload_date", "")
        if raw_date and len(raw_date) == 8:
            upload_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
        else:
            upload_date = raw_date

        videos.append({
            "title": data.get("title", ""),
            "url": data.get("url") or data.get("webpage_url") or f"https://youtube.com/watch?v={data.get('id', '')}",
            "channel": data.get("uploader") or data.get("channel", ""),
            "view_count": data.get("view_count"),
            "duration": duration_str,
            "upload_date": upload_date,
        })

    return videos


def main():
    if len(sys.argv) < 2:
        print("Usage: youtube_search.py <query> [count]", file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    videos = search_youtube(query, count)
    print(json.dumps(videos, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
