# Zpracuj transcript lekce

## Použití
`/zpracuj-lekci $ARGUMENTS`
kde `$ARGUMENTS` je název souboru v `transcripts/`, např. `lekce-03.json`

## Krok 1 — Načtení transcriptu

Pro `.json` soubory použij skill `zoom-transcript`:
- Přečti `.claude/skills/zoom-transcript/SKILL.md`
- Ulož Python kód do `/tmp/parse_transcript.py`
- Spusť: `python /tmp/parse_transcript.py transcripts/$ARGUMENTS > /tmp/transcript_clean.txt`

Pro `.srt` / `.vtt` / `.txt` čti přímo.

## Krok 2 — Zkontroluj dostupné zdroje

1. `repo-summary/lekce-XX-repo.md` — pokud neexistuje, upozorni uživatele ať spustí `/analyzuj-repo`
2. `discord-parsed/lekce-XX-*.json` — načti všechny soubory odpovídající této lekci; pokud žádné nejsou, upozorni uživatele ať spustí `/rozpadni-discord`

## Krok 3 — Průchod 1: Identifikace nejasností

Vytvoř `output/summaries/[název-bez-přípony]-review-nejasnosti.md`:
1. Tabulka úspěšně rozpoznaných garblovaných termínů
2. Pro každý nejasný termín: přesný čas + doslovný kontext + tip (hledej i v repo-summary)
3. Prioritizovaná tabulka: Vysoká / Střední / Nízká

## Krok 4 — Průchod 2: Summary

Vytvoř `output/summaries/[název-bez-přípony]-summary.md` kombinací zdrojů:
- **Transcript** → shrnutí, kapitoly s časy, tipy lektora
- **repo-summary** → sekce "Kód z repozitáře" s názvy souborů
- **Discord** → sekce "Z Discordu — [název kanálu]" pro každý kanál zvlášť

Nejasnosti označuj `[???]` s odkazem na review soubor.

## Krok 5 — Aktualizace all-tools.md

Přidej nové nástroje ze všech zdrojů do `output/all-tools.md`.

## Na konci vypiš
- Které zdroje byly použity (transcript / repo-summary / discord kanály)
- Počet nejasností Vysoké priority
