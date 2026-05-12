"""
Discord Channel Fetcher.
Načte DISCORD_TOKEN z env/.env, kanály z discord_channel/channels.json,
stáhne všechny zprávy a uloží do discord_channel/export/{channel}.json.

Setup:
  export DISCORD_TOKEN="tvuj_token"
  python scripts/fetch_discord.py
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
import requests

load_dotenv()

PROJECT_ROOT  = Path(__file__).parent.parent
CHANNELS_FILE = PROJECT_ROOT / "discord_channel" / "channels.json"
OUTPUT_DIR    = PROJECT_ROOT / "discord_channel" / "export"

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("✗ DISCORD_TOKEN není nastaven (env nebo .env soubor)")

HEADERS = {
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Discord-Timezone": "Europe/Prague",
    "X-Discord-Locale": "cs",
}

URL_RE = re.compile(r"https?://\S+")


def parse_message(raw: dict) -> dict:
    author  = raw.get("author", {})
    content = raw.get("content", "")

    embeds = []
    for e in raw.get("embeds", []):
        embed: dict = {}
        if e.get("title"):                  embed["title"]       = e["title"]
        if e.get("description"):            embed["description"] = e["description"]
        if e.get("url"):                    embed["url"]         = e["url"]
        if e.get("type"):                   embed["type"]        = e["type"]
        if e.get("author", {}).get("name"): embed["author"]      = e["author"]["name"]
        if embed:
            embeds.append(embed)

    reactions = {
        r["emoji"]["name"]: r["count"]
        for r in raw.get("reactions", [])
        if r.get("emoji", {}).get("name")
    }

    msg: dict = {
        "id":        raw["id"],
        "timestamp": raw["timestamp"][:19],
        "author":    author.get("global_name") or author.get("username", "?"),
        "content":   content,
        "links":     URL_RE.findall(content),
    }
    if embeds:    msg["embeds"]    = embeds
    if reactions: msg["reactions"] = reactions

    return msg


def fetch_raw(channel_id: str) -> list[dict]:
    messages: list[dict] = []
    before = None
    page   = 0

    while True:
        params: dict = {"limit": 100}
        if before:
            params["before"] = before

        r = requests.get(
            f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=HEADERS,
            params=params,
        )

        if r.status_code == 401:
            print("  ✗ Neplatný token"); return []
        if r.status_code == 403:
            print("  ✗ Nemáš přístup k tomuto kanálu"); return []
        if r.status_code == 429:
            wait = r.json().get("retry_after", 5)
            print(f"  ⏳ Rate limit — čekám {wait:.1f}s...")
            time.sleep(wait); continue
        if r.status_code != 200:
            print(f"  ✗ HTTP {r.status_code}: {r.text[:200]}"); break

        batch = r.json()
        if not batch:
            break

        messages.extend(batch)
        before = batch[-1]["id"]
        page  += 1
        print(f"  stránka {page}: {len(messages)} zpráv celkem...")
        time.sleep(0.5)

    return messages


def export_channel(channel: dict) -> None:
    cid  = channel["id"]
    name = channel["name"]
    print(f"→ #{name} ({cid})")

    raw = fetch_raw(cid)
    if not raw:
        return

    parsed     = [parse_message(m) for m in raw]
    timestamps = [m["timestamp"] for m in parsed]

    output = {
        "meta": {
            "channel_id":    cid,
            "channel_name":  name,
            "description":   channel.get("description", ""),
            "exported_at":   datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "message_count": len(parsed),
            "oldest_message": min(timestamps),
            "newest_message": max(timestamps),
        },
        "messages": list(reversed(parsed)),
    }

    out = OUTPUT_DIR / f"{name}.json"
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ {len(parsed)} zpráv → {out.name}\n")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    if not CHANNELS_FILE.exists():
        raise SystemExit(f"✗ Nenalezen {CHANNELS_FILE}")

    channels = json.loads(CHANNELS_FILE.read_text(encoding="utf-8"))
    print(f"Discord Export — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Kanálů ke stažení: {len(channels)}\n")

    for ch in channels:
        export_channel(ch)

    print("Hotovo.")


if __name__ == "__main__":
    main()
