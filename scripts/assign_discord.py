"""
Discord Assign — přiřadí zprávy z API exportu k lekcím.
Vstup:  discord-channel/export/*.json  (výstup fetch_discord.py)
Výstup: discord-parsed/lekce-XX-{channel}.json

Použití:
  python scripts/assign_discord.py discord-channel/export lekce-datumy.json
"""

import json
import re
import sys
from datetime import date
from pathlib import Path


def detect_lesson_number(filename: str) -> int | None:
    m = re.search(r'(?<!\d)(\d{1,2})(?!\d)', filename)
    return int(m.group(1)) if m else None


def assign_by_dates(messages: list[dict], lesson_dates: dict[str, str]) -> dict[str, list[dict]]:
    parsed = {k: date.fromisoformat(v) for k, v in lesson_dates.items()}
    sorted_lessons = sorted(parsed.items(), key=lambda x: x[1])

    result: dict[str, list[dict]] = {}
    for msg in messages:
        msg_date = date.fromisoformat(msg["date"])
        assigned = None
        for lesson_key, lesson_date in sorted_lessons:
            if msg_date >= lesson_date:
                assigned = lesson_key
        key = assigned if assigned else "pred-lekcemi"
        result.setdefault(key, []).append(msg)
    return result


def normalize_message(msg: dict) -> dict:
    ts = msg.get("timestamp", "")
    return {
        "author":   msg.get("author", "?"),
        "datetime": ts,
        "date":     ts[:10] if ts else "",
        "text":     msg.get("content", ""),
        "links":    msg.get("links", []),
    }


def process_file(
    filepath: Path,
    lesson_dates: dict[str, str],
    output_dir: Path,
) -> dict[str, int]:
    data = json.loads(filepath.read_text(encoding="utf-8"))
    channel_name = data["meta"]["channel_name"]
    messages = [normalize_message(m) for m in data["messages"]]

    lesson_number = detect_lesson_number(filepath.stem)
    if lesson_number:
        result = {f"lekce-{lesson_number:02d}": messages}
        print(f"  #{channel_name}: číslo lekce {lesson_number} z názvu", file=sys.stderr)
    else:
        result = assign_by_dates(messages, lesson_dates)
        print(f"  #{channel_name}: rozpadnuto podle datumů", file=sys.stderr)

    output_dir.mkdir(exist_ok=True)
    counts: dict[str, int] = {}
    for lesson_key, lesson_msgs in result.items():
        if not lesson_msgs:
            continue
        out = output_dir / f"{lesson_key}-{channel_name}.json"
        out.write_text(json.dumps(lesson_msgs, ensure_ascii=False, indent=2), encoding="utf-8")
        counts[lesson_key] = len(lesson_msgs)
        print(f"  → {out.name} ({len(lesson_msgs)} zpráv)")

    return counts


def main() -> None:
    if len(sys.argv) < 2:
        print("Použití: python scripts/assign_discord.py <export_dir> [lekce-datumy.json]")
        sys.exit(1)

    export_dir = Path(sys.argv[1])
    dates_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("lekce-datumy.json")
    output_dir = Path("discord-parsed")

    if not dates_file.exists():
        raise SystemExit(f"✗ Nenalezen {dates_file}")

    lesson_dates: dict[str, str] = json.loads(dates_file.read_text(encoding="utf-8"))

    json_files = sorted(export_dir.glob("*.json"))
    if not json_files:
        raise SystemExit(f"✗ Žádné JSON soubory v {export_dir}")

    print(f"Zpracovávám {len(json_files)} kanálů z {export_dir}...")
    total = 0
    for f in json_files:
        counts = process_file(f, lesson_dates, output_dir)
        total += sum(counts.values())

    print(f"\nHotovo — {total} zpráv celkem → {output_dir}/")


if __name__ == "__main__":
    main()
