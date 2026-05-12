# Zoom Transcript Parser

Tento skill načte Zoom recording JSON a vrátí čistý přepis připravený k analýze.
Použij tento skill VŽDY před analýzou jakéhokoli `.json` transcriptu.

## Kdy použít
Kdykoli pracuješ se souborem v `transcripts/*.json`.

## Postup

Ulož následující Python kód do `/tmp/parse_transcript.py` a spusť ho.

```python
import json
import re
import sys
from collections import Counter

def clean_text(text):
    """Oprav garblované zkratky z Zoom auto-transcriptu."""
    replacements = [
        (r'[Ll]angenglish[Ii]nitialsd[ií]k?[ai]?initial[Ll]angenglish', 'SDK'),
        (r'[Ii]nitialsd[ií]k?[ai]?initial(?:[Ll]angenglish)?', 'SDK'),
        (r'sdk[áa][čc]ke?m?|sdk[áa][čc]ko|sdékáčko', 'SDK'),
        (r'[Ll]angenglish[Ii]nitialapii?t?initial[Ll]angenglish', 'API'),
        (r'[Ii]nitialapii?t?initial(?:[Ll]angenglish)?', 'API'),
        (r'[Ll]angenglish[Ii]nitialid[ei]?initial[Ll]angenglish', 'IDE'),
        (r'[Ii]nitialid[ei]?initial(?:[Ll]angenglish)?', 'IDE'),
        (r'[Ll]angenglish[Ii]nitialmcp[Ii]nitial[Ll]angenglish', 'MCP'),
        (r'[Ii]nitialmcp[Ii]nitial(?:[Ll]angenglish)?', 'MCP'),
        (r'mcpíčko|mcp[íi][čc]ko', 'MCP'),
        (r'[Ll]angenglish[Ii]nitialmpm?[Ii]nitial(?:[Ll]angenglish)?', 'npm'),
        (r'[Ii]nitialmpm?[Ii]nitial(?:[Ll]angenglish)?', 'npm'),
        (r'[Ll]angenglish[Ii]nitialcla[Ii]nitial[Ll]angenglish', 'CLI'),
        (r'[Ii]nitialcla[Ii]nitial(?:[Ll]angenglish)?', 'CLI'),
        (r'[Ll]angenglish[Ii]nitialgpt[Ii]nitial[Ll]angenglish', 'GPT'),
        (r'[Ii]nitialgpt[Ii]nitial(?:[Ll]angenglish)?', 'GPT'),
        (r'[Ii]nitiallm\b', 'LLM'),
        (r'[Ii]nitialvs[Ii]nitial', 'VS'),
        (r'[Ii]nitialmd[Ii]nitial', '.md'),
        (r'[Ii]nitialcd[Ii]nitial', 'cd'),
        (r'\b[Ll]anggraf\b|\b[Ll]enggraf\b', 'LangGraph'),
        (r'\b[Ll]angčejn\b|\b[Ll]engčejn\b', 'LangChain'),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text

def parse_zoom_json(filepath):
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    items = data['result']['transcriptList']

    # Identifikuj hlavního řečníka (pro metadata)
    speaker_counts = Counter(i['username'] for i in items)
    main_speaker = speaker_counts.most_common(1)[0][0]

    # Metadata
    print(f"=== METADATA ===")
    print(f"Hlavní řečník: {main_speaker}")
    print(f"Délka: {items[-1]['ts']}")
    print(f"Počet položek celkem: {len(items)}")
    print(f"Řečníci: {dict(speaker_counts.most_common())}")
    print()

    # Celý transcript — všichni řečníci, hlavní označen hvězdičkou
    print("=== TRANSCRIPT ===")
    for i in items:
        speaker = i['username']
        prefix = "*" if speaker == main_speaker else f"[{speaker}]"
        print(f"[{i['ts']}] {prefix} {clean_text(i['text'])}")

if __name__ == '__main__':
    parse_zoom_json(sys.argv[1])
```

## Spuštění

```bash
python /tmp/parse_transcript.py transcripts/lekce-03.json > /tmp/transcript_clean.txt
cat /tmp/transcript_clean.txt
```

## Formát výstupu

```
=== METADATA ===
Hlavní řečník: Lukáš Kellerstein
Délka: 02:45:13.000
...

=== TRANSCRIPT ===
[00:04:23] * Tak, dobrý večer.
[00:04:31] [Jan Novák] Dobrý večer!
[00:04:45] * Dneska se podíváme na SDK...
```

`*` = hlavní řečník, `[Jméno]` = ostatní účastníci.
