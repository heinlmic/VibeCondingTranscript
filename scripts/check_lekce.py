"""
Ověří dostupnost a správné pojmenování zdrojových souborů pro lekce.
Použití:
  uv run python scripts/check_lekce.py [číslo_lekce]
  Bez argumentu zkontroluje lekce 1–8.
"""
import json
import sys
from pathlib import Path


def find_transcript_alt(n: int, transcript_dir: Path, expected: Path) -> Path | None:
    for name in [f"transcript{n}.json", f"transcript{n:02d}.json"]:
        candidate = transcript_dir / name
        if candidate.exists():
            return candidate
    for candidate in sorted(transcript_dir.glob("*.json")):
        if candidate == expected:
            continue
        stem = candidate.stem
        if str(n) in stem:
            return candidate
    return None


def count_discord_messages(files: list[Path]) -> int:
    total = 0
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            total += len(data)
        except Exception:
            pass
    return total


def check_lesson(n: int, lesson_dates: dict[str, str]) -> None:
    xx = f"{n:02d}"
    lesson_key = f"lekce-{xx}"
    lesson_date = lesson_dates.get(lesson_key, "neznámo")
    print(f"\nLekce {xx} ({lesson_date}):")

    # transcripts/
    transcript_dir = Path("transcripts")
    expected = transcript_dir / f"lekce-{xx}.json"
    if expected.exists():
        print(f"  transcripts/     ✓  lekce-{xx}.json")
    elif transcript_dir.exists():
        alt = find_transcript_alt(n, transcript_dir, expected)
        if alt:
            sys.stdout.write(f"  transcripts/     ⚠  {alt.name}  → lekce-{xx}.json [přejmenovat? y/N] ")
            sys.stdout.flush()
            answer = sys.stdin.readline().strip().lower()
            if answer == "y":
                alt.rename(expected)
                print(f"     → přejmenováno na lekce-{xx}.json")
            else:
                print()
        else:
            print(f"  transcripts/     ✗  nenalezeno")
    else:
        print(f"  transcripts/     ✗  adresář neexistuje")

    # presentations/
    pres_dir = Path("presentations")
    pres_found = []
    if pres_dir.exists():
        for ext in ("pdf", "pptx", "html"):
            p = pres_dir / f"lekce-{xx}.{ext}"
            if p.exists():
                pres_found.append(p.name)
    if pres_found:
        print(f"  presentations/   ✓  {', '.join(pres_found)}")
    else:
        print(f"  presentations/   ✗  nenalezeno")

    # discord-parsed/
    discord_dir = Path("discord-parsed")
    discord_files = sorted(discord_dir.glob(f"lekce-{xx}-*.json")) if discord_dir.exists() else []
    if discord_files:
        total = count_discord_messages(discord_files)
        names = ", ".join(f.name for f in discord_files)
        print(f"  discord-parsed/  ✓  {names} ({total} zpráv)")
    else:
        print(f"  discord-parsed/  ✗  nenalezeno")

    # repo-summary/
    repo_file = Path("repo-summary") / f"lekce-{xx}-repo.md"
    if repo_file.exists():
        print(f"  repo-summary/    ✓  lekce-{xx}-repo.md")
    else:
        print(f"  repo-summary/    ✗  nenalezeno")

    # output/summaries/
    summary_file = Path("output/summaries") / f"lekce-{xx}-summary.md"
    if summary_file.exists():
        print(f"  output/summary   ✓  lekce-{xx}-summary.md (hotovo)")
    else:
        print(f"  output/summary   ✗  nenalezeno")


def main() -> None:
    dates_file = Path("lekce-datumy.json")
    lesson_dates: dict[str, str] = {}
    if dates_file.exists():
        lesson_dates = json.loads(dates_file.read_text(encoding="utf-8"))

    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print(f"Chyba: '{sys.argv[1]}' není platné číslo lekce", file=sys.stderr)
            sys.exit(1)
        check_lesson(n, lesson_dates)
    else:
        for n in range(1, 9):
            check_lesson(n, lesson_dates)
    print()


if __name__ == "__main__":
    main()
