# Vibe Coding Course — Transcript Processor

## Struktura
```
vibe-coding-course/
├── CLAUDE.md
├── .claude/commands/
│   ├── analyzuj-repo.md          # /analyzuj-repo <cesta-k-repo>
│   ├── zpracuj-lekci.md          # /zpracuj-lekci <soubor>
│   ├── zpracuj-vse.md            # /zpracuj-vse
│   └── dopln-nejasnosti.md       # /dopln-nejasnosti <lekce>
├── transcripts/                   # Zoom JSON exporty
├── discord/                       # kopie Discord po lekcích
├── repo-summary/                  # generováno přes /analyzuj-repo
└── output/
    ├── all-tools.md
    └── summaries/
```

## Postup — poprvé

```bash
cd vibe-coding-course
claude

# 1. Jednou na začátku — analyzuj repo
/analyzuj-repo /cesta/k/Vibe-Coding-1

# 2. Pro každou lekci
/zpracuj-lekci lekce-03.json

# 3. Doplň nejasnosti ve videu (podle review souboru)
# 4. Finalizuj
/dopln-nejasnosti lekce-03
```

## Zdroje dat

**Transcript** — Zoom JSON export. Klíč: `result.transcriptList`.

**Repo** — lokálně naklonované, organizované po tématech odpovídajících lekcím:
`1_LLM` → `2_Codex` → `3_Codex_SDK` → `4_Claude_Code` → `5_Claude_Agent_SDK` → `6_Others` → `7_Practical_Office_suite` → `8_Practical_Code`

**Discord** — čistý text z kopie kanálu. Ulož jako `discord/lekce-XX.txt` (nebo `general.txt` pro celý kanál).
