# Zpracuj transcript lekce

## Použití
`/zpracuj-lekci $ARGUMENTS`
kde `$ARGUMENTS` je číslo lekce, např. `3` nebo `03`

## Krok 0 — Resolve čísla lekce na soubor

Z `$ARGUMENTS` odvoď:
- číslo lekce jako dvouciferné `XX` (např. `3` → `03`, `12` → `12`)
- hledej v `transcripts/` soubor odpovídající vzoru `lekce-XX.*` (json/srt/vtt/txt)
- pokud soubor neexistuje, vypiš dostupné soubory v `transcripts/` a skonči

## Krok 1 — Prezentace (volitelná analytická pomůcka)

Hledej `presentations/lekce-XX.*`:
- `.pdf` nebo `.html` — načti přímo přes Read tool
- `.pptx` — spusť `python scripts/parse_presentation.py presentations/lekce-XX.pptx` a načti výstup

Pokud soubor existuje, načti jej **před Průchodem 1** a použij pro:
- přesnější detekci kapitol (slide tituly = přirozené předěly)
- opravování garblovaných termínů (správná anglická slova jsou ve slidech)
- kontext nejasných pasáží

Pokud prezentace neexistuje, pokračuj bez ní.

## Krok 2 — Načtení transcriptu

Pro `.json` soubory použij skill `zoom-transcript`:
- Přečti `.claude/skills/zoom-transcript/SKILL.md`
- Ulož Python kód do `/tmp/parse_transcript.py`
- Spusť: `python /tmp/parse_transcript.py transcripts/lekce-XX.json > /tmp/transcript_clean.txt`

Pro `.srt` / `.vtt` / `.txt` čti přímo.

## Krok 3 — Zkontroluj dostupné zdroje

1. `repo-summary/lekce-XX-repo.md` — pokud neexistuje, upozorni uživatele ať spustí `/analyzuj-repo`
2. `discord-parsed/lekce-XX-*.json` — načti všechny soubory odpovídající této lekci; pokud žádné nejsou, upozorni uživatele ať spustí `/rozpadni-discord`

## Krok 4 — Průchod 1: Identifikace nejasností

Vytvoř `output/summaries/lekce-XX-review-nejasnosti.md`:
1. Tabulka úspěšně rozpoznaných garblovaných termínů
2. Pro každý nejasný termín: přesný čas + doslovný kontext + tip (hledej i v repo-summary)
3. Prioritizovaná tabulka: Vysoká / Střední / Nízká

## Krok 5 — Průchod 2: Summary

Vytvoř `output/summaries/lekce-XX-summary.md` kombinací zdrojů:
- **Transcript** → shrnutí, kapitoly s časy, tipy lektora
- **repo-summary** → sekce "Relevantní soubory v repo": max 2–3 soubory s jednořádkovým popisem, jen pokud jsou extra relevantní; pokud není co zdůraznit, sekci vynech
- **Discord** → sekce "Z Discordu — [název kanálu]" pro každý kanál zvlášť
- **Hlavička**: uveď `Prezentace: ano` pokud byl soubor v `presentations/` dostupný, jinak `Prezentace: ne`

Nejasnosti označuj `[???]` s odkazem na review soubor.

## Krok 6 — Aktualizace all-tools.md

Přidej nové nástroje ze všech zdrojů do `output/all-tools.md`.
Pro každý nový nástroj s URL použij MCP `fetch` tool (`mcp__fetch__fetch`) k načtení stránky a doplnění stručného popisu z oficiálního zdroje.

## Na konci vypiš
- Které zdroje byly použity (transcript / repo-summary / discord kanály)
- Počet nejasností Vysoké priority
