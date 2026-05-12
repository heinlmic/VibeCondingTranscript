# Vibe Coding Course — Transcript Processing

## Účel projektu
Zpracování transkriptů z vibe coding kurzu do strukturovaných summary.
Pro každou lekci vznikají tři zdroje dat: transcript (co lektor říkal), repo (kód který ukazoval), Discord (otázky a tipy komunity).

## Struktura projektu
```
VibeCondingTranscript/
├── .claude/
│   ├── commands/           # slash commands
│   └── skills/
│       ├── zoom-transcript/SKILL.md
│       └── discord-assign/SKILL.md
├── scripts/                # spustitelné Python skripty
│   ├── parse_transcript.py
│   ├── fetch_discord.py
│   ├── assign_discord.py
│   └── parse_presentation.py
├── transcripts/            # Zoom JSON exporty (gitignorované)
├── presentations/          # Prezentace k lekcím (gitignorované) — jen jako analytická pomůcka
│   ├── lekce-01.pdf        # .pdf čte Claude nativně
│   ├── lekce-02.pptx       # .pptx → spusť parse_presentation.py
│   └── lekce-03.html       # .html čte Claude jako text
├── discord_channel/        # Discord konfigurace + stažená data
│   ├── channels.json       # seznam kanálů ke stažení
│   └── export/             # výstup fetch_discord.py (gitignorovaný)
├── discord-parsed/         # výstup assign_discord.py, per lekce
├── repo-summary/           # generováno přes /analyzuj-repo — NEČÍST REPO PŘÍMO
│   ├── lekce-01-repo.md
│   └── ...
└── output/
    ├── all-tools.md
    ├── index.md
    └── summaries/
        ├── lekce-03-review-nejasnosti.md
        └── lekce-03-summary.md
```

## Cesta k repozitáři kurzu
Repo je naklonované lokálně — cestu poskytne uživatel při spuštění příkazu `/analyzuj-repo`.
Nikdy nečti repo přímo při zpracování lekce — vždy použij již vygenerované `repo-summary/lekce-XX-repo.md`.

## Mapa repo → lekce

| Složka v repo | Lekce | Téma |
|---------------|-------|------|
| `1_LLM/` | Lekce 1 | Základy LLM — API volání (OpenAI, Anthropic, Ollama, HuggingFace, Gemini, Grok, LiteLLM...) |
| `2_Codex/` | Lekce 2 | Codex manuálně — tools, MCP, skills, subagents, hooks, plugins, marketplace |
| `3_Codex_SDK/typescript/` | Lekce 3 | Codex SDK (TypeScript) — single thread, multi-thread, workflows, patterns |
| `4_Claude_Code/` | Lekce 4 | Claude Code — tools, MCP, skills, subagents, hooks, plugins, marketplace |
| `5_Claude_Agent_SDK/` | Lekce 5 | Claude Agent SDK (Python + TypeScript) — single agent, multi-agent, workflows |
| `6_Others/` | Lekce 6 | Ostatní agenti — Copilot CLI+SDK, Gemini CLI, Cursor, OpenCode |
| `7_Practical_Office_suite/` | Lekce 7 | Office suite — grafy, obrázky, videa, TTS, PPTX, DOCX, XLSX, Google Workspace |
| `8_Practical_Code/` | Lekce 8 | Praktické kódování — spec-kit, Ralph Wiggum pattern |
| `100_Others/` | — | Infrastructure — Langfuse (observability), LiteLLM (proxy) |

Poznámka: `1_LLM/99_providers/` obsahuje inference servery (Ollama, LM Studio, llama-server, vLLM, SGLang, RunPod, Vast.ai) — relevantní pro více lekcí.

---

## Formáty vstupů

### Transcript
| Formát | Zdroj | Jak zpracovat |
|--------|-------|---------------|
| `.json` | Zoom recording | `uv run python scripts/parse_transcript.py transcripts/lekce-XX.json` |
| `.srt` / `.vtt` | Video platformy | Standardní formát, přesné časy |
| `.txt` | Ruční export | Odhadni časy, označuj `[~odhad]` |

Formát časových značek: `[MM:SS]` nebo `[H:MM:SS]` pro lekce delší než hodinu.

### Discord (API)
Data stahuje `scripts/fetch_discord.py` z Discord API a ukládá do `discord_channel/export/{channel}.json`.

Formát: `{ "meta": { channel_name, exported_at, ... }, "messages": [{ id, timestamp, author, content, links, embeds? }] }`

`scripts/assign_discord.py` přiřadí zprávy do `discord-parsed/lekce-XX-{channel}.json`.

Při zpracování lekce vytáhni z `discord-parsed/lekce-XX-*.json`: nástroje a linky zmíněné komunitou, zajímavé diskuse, otázky na lektora.

### Prezentace (volitelný analytický zdroj)
Soubory v `presentations/lekce-XX.*` — slouží **pouze při analýze** (detekce kapitol, oprava garblovaných termínů, kontext nejasností). V summary se neobjeví jako samostatná sekce.

| Formát | Jak číst |
|--------|----------|
| `.pdf` | Claude čte nativně přes Read tool |
| `.html` | Claude čte jako text přes Read tool |
| `.pptx` | Spusť `uv run python scripts/parse_presentation.py presentations/lekce-XX.pptx` → plain text se slide tituly |

Pokud prezentace existuje, uveď v hlavičce summary: `Prezentace: ano`.

### Repo summary
Předgenerovaný popis složky odpovídající lekci. Obsahuje: popis souborů, klíčové funkce, struktura, na co se zaměřit. Vždy použij místo přímého čtení repo.

---

## Discord workflow

```bash
# 1. Stáhni zprávy (potřeba DISCORD_TOKEN v env)
uv run python scripts/fetch_discord.py
# → discord_channel/export/{channel}.json

# 2. Rozpadni do lekcí
uv run python scripts/assign_discord.py discord_channel/export lekce-datumy.json
# → discord-parsed/lekce-XX-{channel}.json
```

Nebo použij `/rozpadni-discord` pro celý postup.

---

## Dvoupůchodový workflow (vždy dodržuj)

### Průchod 1 — Identifikace nejasností
Vytvoř `output/summaries/lekce-XX-review-nejasnosti.md`:
1. Tabulka úspěšně rozpoznaných garblovaných termínů
2. Detailní sekce pro každý nejasný termín: přesný čas + doslovný kontext + tip
3. Prioritizovaná tabulka akcí: Vysoká / Střední / Nízká

### Průchod 2 — Finální summary
Vytvoř `output/summaries/lekce-XX-summary.md` kombinací všech tří zdrojů.
Pokud uživatel nedoplnil nejasnosti, použij `[???]`.

---

## Slovník garblovaných vzorů (Zoom auto-transcript CZ)

Vzor: `Initial*initial` nebo `Langenglish*` = zkomolenina anglické zkratky

| Přepis | Správně |
|--------|---------|
| `initialsdkinitial`, `sdkáčko`, `sdékáčko` | SDK |
| `initialmcpinitial`, `mcpíčko` | MCP |
| `initialideinitial`, `initialvsinitial` | IDE / VS Code |
| `initialmpminitial`, `initialmpinitial` | npm |
| `initialclainitiallangenglish` | CLI |
| `initialgptinitiallangenglish` | GPT |
| `Initiallm` | LLM |
| `initialmdiniitial` | .md (markdown) |
| `initialcdiniitial` | cd (terminálový příkaz) |

Fonetické přepisy:

| Přepis | Správně |
|--------|---------|
| `lenggraf`, `langgraf` | LangGraph |
| `lengčejn` | LangChain |
| `klod`, `kloud kód` | Claude / Claude Code |
| `kopajtot`, `kopajlot`, `kopilot` | Copilot |
| `ralph wigum`, `ralf liggum` | Ralph Wiggum (pattern/projekt v `8_Practical_Code/`) |
| `džejson` | JSON |
| `gethab`, `gid hub` | GitHub |
| `tůl`, `tuli` | tool/tools |
| `skil`, `skilly` | skill/skills |
| `patern`, `paterny` | pattern/patterns |
| `tred`, `tredy` | thread/threads |

---

## Detekce kapitol

Signály pro novou kapitolu:
- Frázování: "teď se pojďme podívat na...", "ukážeme si...", "přejdeme k..."
- Přechod teorie → kód → demo → Q&A
- Zoom JSON: gap > 30s = pauza nebo přestávka

---

## Output formát — lekce-XX-summary.md

```
# Lekce XX — [Název]

> Datum: | Délka: | Repo: [složka v repo] | Prezentace: ano/ne

## Shrnutí
2-4 věty.

## Kapitoly
| Čas | Kapitola | Popis |
|-----|----------|-------|

## Relevantní soubory v repo
- `cesta/k/souboru.py` — jednořádkový popis (max 2–3 položky, jen extra relevantní; pokud není co zdůraznit, sekci vynech)

## Nástroje a repa
- **Nástroj** — popis

## Z Discordu — tipy komunity
- zajímavé linky, otázky, diskuse

## Klíčové poznatky a tipy lektora
- konkrétní doporučení
```

---

## Pravidla

- Po každé změně (skripty, workflow, závislosti, struktura projektu) zkontroluj a aktualizuj všechny navazující soubory: `README.md`, `CLAUDE.md`, příslušné skills v `.claude/skills/`, slash commands v `.claude/commands/`. Nezanechávej dokumentaci v nekonzistentním stavu.
- Nikdy nečti repo přímo — vždy používej `repo-summary/`
- Nepřekládej anglické názvy nástrojů
- Pokud lektor ukázal konkrétní kód — zahrň název souboru z repo
- Zachovej češtinu v popisech, angličtinu v názvech nástrojů
- Hlavní řečník v Zoom JSON = nejvíce položek; filtruj pro detekci kapitol
- Python skripty spouštěj z kořene projektu přes `uv run python scripts/...`
