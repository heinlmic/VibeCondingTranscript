# Discord Parser

Parsuje čistý text zkopírovaný z Discord kanálu do strukturovaného JSON.
Tento skill POUZE parsuje formát — nepřiřazuje lekce. Pro přiřazení k lekcím použij skill `discord-assign`.

## Kdy použít
Jako první krok před `discord-assign`, kdykoli pracuješ s `discord/*.txt`.

## Postup

Ulož Python kód do `/tmp/parse_discord.py` a spusť ho.

```python
import re
import json
import sys
from datetime import datetime

def parse_discord(text):
    messages = []
    header_pattern = re.compile(r'^(.+?)\s+—\s+(\d{2}\.\d{2}\.\d{2})\s+(\d{2}:\d{2})\s*$')
    url_pattern = re.compile(r'https?://\S+')

    lines = text.split('\n')
    current = None
    content_lines = []

    def flush(current, content_lines):
        if current is None:
            return None
        raw_lines = [l for l in content_lines if l.strip().lower() != 'obrázek']

        links = []
        clean_lines = []
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i].strip()
            if url_pattern.match(line):
                url = line
                title, desc = '', ''
                j = i + 1
                candidates = []
                while j < len(raw_lines):
                    candidate = raw_lines[j].strip()
                    if not candidate or url_pattern.match(candidate) or header_pattern.match(candidate):
                        break
                    candidates.append(candidate)
                    j += 1
                seen = []
                for c in candidates:
                    if c not in seen:
                        seen.append(c)
                if seen:
                    title = seen[0]
                if len(seen) > 1:
                    desc = seen[1]
                links.append({'url': url, 'title': title, 'description': desc})
                i = j
            else:
                if line:
                    clean_lines.append(line)
                i += 1

        current['text'] = '\n'.join(clean_lines).strip()
        current['links'] = links
        return current

    for line in lines:
        m = header_pattern.match(line)
        if m:
            if current is not None:
                msg = flush(current, content_lines)
                if msg:
                    messages.append(msg)
            author, date_str, time_str = m.groups()
            dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%y %H:%M")
            current = {
                'author': author.strip(),
                'datetime': dt.isoformat(),
                'date': dt.strftime('%Y-%m-%d'),
                'time': time_str,
            }
            content_lines = []
        else:
            if current is not None:
                content_lines.append(line)

    if current is not None:
        msg = flush(current, content_lines)
        if msg:
            messages.append(msg)

    return messages

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Použití: python parse_discord.py <soubor.txt>")
        sys.exit(1)

    with open(sys.argv[1], encoding='utf-8') as f:
        text = f.read()

    print(json.dumps(parse_discord(text), ensure_ascii=False, indent=2))
```

## Spuštění

```bash
python /tmp/parse_discord.py discord/zajimavosti.txt > /tmp/discord_raw.json
```

## Formát výstupu

```json
[
  {
    "author": "LukasKellerstein",
    "datetime": "2026-04-09T18:53:00",
    "date": "2026-04-09",
    "time": "18:53",
    "text": "text zprávy",
    "links": [
      { "url": "https://...", "title": "...", "description": "..." }
    ]
  }
]
```
