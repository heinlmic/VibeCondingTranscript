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
│   ├── parse_presentation.py
│   └── check_lekce.py      # pre-check souborů před zpracováním
├── transcripts/            # Zoom JSON exporty (gitignorované)
│   └── parsed/             # cachované čisté přepisy (gitignorované)
├── presentations/          # Prezentace k lekcím (gitignorované) — jen jako analytická pomůcka
│   ├── lekce-01.pdf        # .pdf čte Claude nativně
│   ├── lekce-02.pptx       # .pptx → spusť parse_presentation.py
│   └── lekce-03.html       # .html čte Claude jako text
├── discord-channel/        # Discord konfigurace + stažená data
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

Složky v repo jsou detekovány automaticky podle číselného prefixu — názvy se mohou lišit (`1_LLM/`, `1-llm-intro/` apod.). Číslo na začátku = číslo lekce.

| Prefix | Lekce | Téma |
|--------|-------|------|
| `1_*/` | Lekce 1 | Základy LLM — API volání (OpenAI, Anthropic, Ollama, HuggingFace, Gemini, Grok, LiteLLM...) |
| `2_*/` | Lekce 2 | Codex manuálně — tools, MCP, skills, subagents, hooks, plugins, marketplace |
| `3_*/` | Lekce 3 | Codex SDK (TypeScript) — single thread, multi-thread, workflows, patterns |
| `4_*/` | Lekce 4 | Claude Code — tools, MCP, skills, subagents, hooks, plugins, marketplace |
| `5_*/` | Lekce 5 | Claude Agent SDK (Python + TypeScript) — single agent, multi-agent, workflows |
| `6_*/` | Lekce 6 | Ostatní agenti — Copilot CLI+SDK, Gemini CLI, Cursor, OpenCode |
| `7_*/` | Lekce 7 | Office suite — grafy, obrázky, videa, TTS, PPTX, DOCX, XLSX, Google Workspace |
| `8_*/` | Lekce 8 | Praktické kódování — spec-kit, Ralph Wiggum pattern |
| `100_*/` | — | Infrastructure — Langfuse (observability), LiteLLM (proxy) |

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
Data stahuje `scripts/fetch_discord.py` z Discord API a ukládá do `discord-channel/export/{channel}.json`.

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

### MCP — fetch server
Projekt využívá MCP server `fetch` (`uvx mcp-server-fetch`) pro načítání URL obsahu.

Kdy použít `fetch` MCP tool:
- Při generování `output/all-tools.md` — pro každý nástroj načti jeho URL a doplň popis
- Při zpracování Discord zpráv — pokud `links[]` obsahují GitHub repa nebo dokumentaci, načti tituly/README
- Při nejasném termínu v transcriptu — ověř na webu, zda nástroj existuje a co dělá

Použití: `mcp__fetch__fetch` s parametrem `url`.

### Subagenti — `/analyzuj-repo`
Při zpracování všech lekcí najednou (`/analyzuj-repo <cesta>` bez čísla lekce) spouští hlavní agent
subagenty paralelně — jeden na lekci — přes `claude --print --allowedTools "Read,Bash"`.

Počet subagentů závisí na tom, kolik složek s číselným prefixem command v repo nalezne.
Každý subagent dostane cestu ke složce lekce a vrátí obsah repo-summary souboru.
Hlavní agent výstupy zapíše do `repo-summary/lekce-XX-repo.md`.

Při zpracování jedné konkrétní lekce se subagent nespouští.

---

## Discord workflow

```bash
# 1. Stáhni zprávy (potřeba DISCORD_TOKEN v env)
uv run python scripts/fetch_discord.py
# → discord-channel/export/{channel}.json

# 2. Rozpadni do lekcí
uv run python scripts/assign_discord.py discord-channel/export lekce-datumy.json
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

## Slovník garblovaných vzorů

Viz `.claude/glossary.md` — načti při Průchodu 1 (identifikace nejasností).

---

## Detekce kapitol

Signály pro novou kapitolu:
- Frázování: "teď se pojďme podívat na...", "ukážeme si...", "přejdeme k..."
- Přechod teorie → kód → demo → Q&A
- Zoom JSON: gap > 30s = pauza nebo přestávka

---

## Output formát

Viz `.claude/output-format.md` — načti při Průchodu 2 (finální summary).

---

## Pravidla

- Po každé změně (skripty, workflow, závislosti, struktura projektu) zkontroluj a aktualizuj všechny navazující soubory: `README.md`, `CLAUDE.md`, příslušné skills v `.claude/skills/`, slash commands v `.claude/commands/`. Nezanechávej dokumentaci v nekonzistentním stavu.
- Nikdy nečti repo přímo — vždy používej `repo-summary/`
- Nepřekládej anglické názvy nástrojů
- Pokud lektor ukázal konkrétní kód — zahrň název souboru z repo
- Zachovej češtinu v popisech, angličtinu v názvech nástrojů
- Hlavní řečník v Zoom JSON = nejvíce položek; filtruj pro detekci kapitol
- Python skripty spouštěj z kořene projektu přes `uv run python scripts/...`
