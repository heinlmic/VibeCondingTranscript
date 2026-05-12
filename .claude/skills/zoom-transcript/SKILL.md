# Zoom Transcript Parser

Parsuje Zoom recording JSON do čistého přepisu.
Použij VŽDY před analýzou jakéhokoli `.json` transcriptu.

## Kdy použít
Kdykoli pracuješ se souborem v `transcripts/*.json`.

## Spuštění

```bash
python scripts/parse_transcript.py transcripts/lekce-03.json > /tmp/transcript_clean.txt
cat /tmp/transcript_clean.txt
```

## Formát výstupu

```
=== METADATA ===
Hlavní řečník: Lukáš Kellerstein
Délka: 02:45:13.000
Počet položek celkem: 1842
Řečníci: {"Lukáš Kellerstein": 1750, "Jan Novák": 92}

=== TRANSCRIPT ===
[00:04:23] * Tak, dobrý večer.
[00:04:31] [Jan Novák] Dobrý večer!
[00:04:45] * Dneska se podíváme na SDK...
```

`*` = hlavní řečník, `[Jméno]` = ostatní účastníci.
Garblované Zoom výrazy (initialsdkinitial, mcpíčko…) jsou automaticky opraveny.
