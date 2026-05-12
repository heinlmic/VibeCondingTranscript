# Discord Assign

Přiřadí zparsované Discord zprávy k lekcím.
Vstup: JSON ze skillu `discord-parser` + název zdrojového souboru.

Logika přiřazení podle názvu souboru:
- Obsahuje číslo (např. `03`, `3`, `lekce03`, `lekce-3`, `chat3`...) → vše do té lekce
- Neobsahuje číslo → rozpadne podle datumů z `lekce-datumy.json`

## Kdy použít
Po `discord-parser`, před zpracováním lekce.

## Postup

Ulož Python kód do `/tmp/assign_discord.py` a spusť ho.

```python
import re
import json
import sys
from datetime import date

def detect_lesson_number(filename):
    """Zkus najít číslo lekce v názvu souboru."""
    # Hledej číslo kdekoliv v názvu: 03, 3, lekce03, lekce-3, chat_03 atd.
    m = re.search(r'(?<!\d)(\d{1,2})(?!\d)', filename)
    if m:
        return int(m.group(1))
    return None

def assign_by_dates(messages, lesson_dates):
    """Přiřaď zprávy podle datumů lekcí."""
    parsed = {k: date.fromisoformat(v) for k, v in lesson_dates.items()}
    sorted_lessons = sorted(parsed.items(), key=lambda x: x[1])

    result = {}
    for msg in messages:
        msg_date = date.fromisoformat(msg['date'])
        assigned = None
        for lesson_key, lesson_date in sorted_lessons:
            if msg_date >= lesson_date:
                assigned = lesson_key
        key = assigned if assigned else 'pred-lekcemi'
        result.setdefault(key, []).append(msg)
    return result

def assign_by_number(messages, lesson_number):
    """Všechny zprávy do jedné lekce."""
    key = f"lekce-{lesson_number:02d}"
    return {key: messages}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Použití: python assign_discord.py <discord_raw.json> <nazev_souboru> [lekce-datumy.json]")
        print("Příklad: python assign_discord.py /tmp/discord_raw.json zajimavosti.txt lekce-datumy.json")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        messages = json.load(f)

    filename = sys.argv[2]
    lesson_number = detect_lesson_number(filename)

    if lesson_number:
        result = assign_by_number(messages, lesson_number)
        print(f"# Detekováno číslo lekce {lesson_number} z názvu '{filename}'", file=sys.stderr)
    else:
        dates_file = sys.argv[3] if len(sys.argv) > 3 else 'lekce-datumy.json'
        with open(dates_file, encoding='utf-8') as f:
            lesson_dates = json.load(f)
        result = assign_by_dates(messages, lesson_dates)
        print(f"# Rozpadnuto podle datumů z '{dates_file}'", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## Spuštění

```bash
# Soubor bez čísla → rozpadne podle datumů
python /tmp/assign_discord.py /tmp/discord_raw.json zajimavosti.txt lekce-datumy.json > /tmp/discord_assigned.json

# Soubor s číslem → vše do lekce 3
python /tmp/assign_discord.py /tmp/discord_raw.json lekce03-chat.txt > /tmp/discord_assigned.json
```

## Formát výstupu

```json
{
  "lekce-01": [ { "author": "...", "date": "...", "text": "...", "links": [] } ],
  "lekce-02": [ ... ],
  "pred-lekcemi": [ ... ]
}
```

## Použití výsledku

Z výstupu vezmi jen sekci odpovídající právě zpracovávané lekci, např. `result["lekce-03"]`.
Kanál (název zdrojového souboru) zaznamenej do summary aby bylo jasné odkud obsah pochází.
ENDOFFILE