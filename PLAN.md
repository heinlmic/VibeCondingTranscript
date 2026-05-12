# Plán: Dokončení struktury VibeCondingTranscript repozitáře

## Context
Repo je z části hotové — všechny transcripts, repo-summary i základní commands/skills jsou na místě. Tři věci potřebují dokončit:
1. Python kód je vložený do SKILL.md souborů místo v samostatných `.py` souborech
2. `discord_channel/` přidán jako nový API-based přístup, ale není integrován do celého workflow (starý .txt přístup zůstává, nový není napojený)
3. `transcripts/` (datové soubory ~4 MB) nejsou v .gitignore

Cíl: čistá, konzistentní struktura kde veškerý spustitelný Python žije v `scripts/`, Discord flow jde jen přes API, a datové soubory jsou gitignorované.

---

## Výsledná struktura

```
VibeCondingTranscript/
├── .claude/
│   ├── commands/           ← beze změn (5 souborů)
│   └── skills/
│       ├── zoom-transcript/SKILL.md    ← zjednodušit, odkázat na scripts/
│       ├── discord-assign/SKILL.md     ← aktualizovat pro API JSON formát
│       └── discord-parser/             ← SMAZAT (obsoletní, .txt workflow)
├── scripts/                ← NOVÁ SLOŽKA
│   ├── parse_transcript.py             ← přesunout z zoom-transcript/SKILL.md
│   ├── assign_discord.py               ← přesunout z discord-assign/SKILL.md + aktualizovat
│   └── fetch_discord.py               ← přesunout z discord_channel/discord_fetch.py
├── discord_channel/        ← jen konfigurace
│   ├── channels.json
│   ├── .env.example
│   └── export/             ← NOVÁ složka pro stažená data (gitignorovaná)
│       └── .gitkeep
├── discord-parsed/         ← NOVÁ složka, výstup assign scriptu per lekce
│   └── .gitkeep
├── transcripts/            ← beze změn, ale GITIGNOROVANÁ
│   └── .gitkeep
├── discord/                ← SMAZAT (nahrazuje discord_channel/export/)
├── repo-summary/           ← beze změn, zůstává v gitu
├── output/                 ← beze změn
├── lekce-datumy.json
├── CLAUDE.md               ← aktualizovat
└── README.md               ← aktualizovat
```

---

## Kroky

### 1. .gitignore — přidat datové soubory

Soubory k přidání do `.gitignore`:
```
# Datové soubory (transcript exporty ze Zoomu)
transcripts/*.json

# Stažená Discord data (API export)
discord_channel/export/

# Generovaný výstup (volitelné — nebo ponechat v gitu jako "produkt")
# output/summaries/
```

Zachovat `transcripts/` složku v gitu přes `transcripts/.gitkeep`.

### 2. Vytvořit `scripts/` adresář

**`scripts/parse_transcript.py`** — zkopírovat kód z `.claude/skills/zoom-transcript/SKILL.md` (řádky s Pythonem). Zachovat `clean_text()` + `parse_zoom_json()`. Vstup: `transcripts/transcriptN.json`, výstup: stdout.

**`scripts/assign_discord.py`** — zkopírovat kód z `.claude/skills/discord-assign/SKILL.md` a **aktualizovat vstupní formát**: discord_fetch.py vrací `{ meta: {...}, messages: [{ id, author, content, timestamp, ... }] }` — assign script musí tuto strukturu přijmout místo starého formátu z parse_discord. Zachovat logiku přiřazení do lekcí podle `lekce-datumy.json`. Výstup: `discord-parsed/lekce-XX.json`.

**`scripts/fetch_discord.py`** — přesunout beze změny z `discord_channel/discord_fetch.py`. Výstup změnit na `discord_channel/export/{channel}.json`.

### 3. Aktualizovat skills

**`zoom-transcript/SKILL.md`** — zkrátit: odstranit embedded Python, přidat odkaz `Spusť: python scripts/parse_transcript.py <soubor>`.

**`discord-assign/SKILL.md`** — zkrátit: odkázat na `scripts/assign_discord.py`, dokumentovat nový vstupní formát (API JSON z `discord_channel/export/`).

**`discord-parser/SKILL.md`** — smazat celou složku (`.txt` workflow se ruší, API fetch ho nahrazuje).

### 4. Aktualizovat command `rozpadni-discord.md`

Nový workflow:
1. `python scripts/fetch_discord.py` → uloží do `discord_channel/export/`
2. `python scripts/assign_discord.py discord_channel/export/ lekce-datumy.json` → uloží do `discord-parsed/lekce-XX.json`

Odstranit reference na `.txt` soubory a starý `discord/` adresář.

### 5. Smazat `discord/` složku

Byla určena pro `.txt` soubory — nahrazena `discord_channel/export/`. Smazat.

### 6. Aktualizovat CLAUDE.md

- Sekce struktury: přidat `scripts/`, `discord_channel/export/`, `discord-parsed/`; odebrat `discord/`
- Discord sekce: aktualizovat popis na API-only přístup, dokumentovat výstupní formát `fetch_discord.py`
- Formáty vstupů: odebrat Discord `.txt` formát
- Workflow: aktualizovat `/rozpadni-discord` postup

### 7. Aktualizovat README.md

Krátká aktualizace struktury a kroků workflow.

---

## Kritické soubory

| Soubor | Akce |
|--------|------|
| `.gitignore` | Přidat `transcripts/*.json`, `discord_channel/export/` |
| `.claude/skills/zoom-transcript/SKILL.md` | Zjednodušit, odkázat na scripts/ |
| `.claude/skills/discord-assign/SKILL.md` | Aktualizovat pro API formát |
| `.claude/skills/discord-parser/` | Smazat celou složku |
| `.claude/commands/rozpadni-discord.md` | Přepsat workflow na API-only |
| `discord_channel/discord_fetch.py` | Přesunout → `scripts/fetch_discord.py` |
| `CLAUDE.md` | Aktualizovat strukturu a Discord sekci |

---

## Nové soubory k vytvoření

| Soubor | Obsah |
|--------|-------|
| `scripts/parse_transcript.py` | Python kód z zoom-transcript/SKILL.md |
| `scripts/assign_discord.py` | Python kód z discord-assign/SKILL.md + úprava vstupního formátu |
| `scripts/fetch_discord.py` | Kopie discord_channel/discord_fetch.py |
| `discord_channel/export/.gitkeep` | Zachovat prázdnou složku v gitu |
| `discord-parsed/.gitkeep` | Zachovat prázdnou složku v gitu |
| `transcripts/.gitkeep` | Zachovat složku po odebrání z gitu |

---

## Ověření po implementaci

1. `python scripts/parse_transcript.py transcripts/transcript1.json` — musí vrátit strukturovaný přepis na stdout
2. `python scripts/fetch_discord.py` (s nastaveným `DISCORD_TOKEN`) — musí zapsat do `discord_channel/export/`
3. `python scripts/assign_discord.py ...` — musí zapsat do `discord-parsed/lekce-XX.json`
4. `git status` — transcripts/*.json nesmí být tracked
5. Skill soubory v `.claude/skills/` musí být čisté (jen dokumentace, žádný embedded Python)
