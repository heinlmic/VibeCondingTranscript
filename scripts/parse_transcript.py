"""
Zoom transcript parser.
Vstup: transcripts/*.json
Výstup: čistý přepis na stdout
Použití: python scripts/parse_transcript.py transcripts/lekce-03.json
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path


def clean_text(text: str) -> str:
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


def parse_zoom_json(filepath: str) -> None:
    with open(filepath, encoding='utf-8') as f:
        data = json.load(f)

    items = data['result']['transcriptList']

    speaker_counts: Counter = Counter(i['username'] for i in items)
    main_speaker = speaker_counts.most_common(1)[0][0]

    print("=== METADATA ===")
    print(f"Hlavní řečník: {main_speaker}")
    print(f"Délka: {items[-1]['ts']}")
    print(f"Počet položek celkem: {len(items)}")
    print(f"Řečníci: {dict(speaker_counts.most_common())}")
    print()

    print("=== TRANSCRIPT ===")
    for i in items:
        speaker = i['username']
        prefix = "*" if speaker == main_speaker else f"[{speaker}]"
        print(f"[{i['ts']}] {prefix} {clean_text(i['text'])}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Použití: python {Path(__file__).name} <transcript.json>")
        sys.exit(1)
    parse_zoom_json(sys.argv[1])
