# Vibe Coding Course — Transcript Processor

Nástroj pro zpracování materiálů z vibe coding kurzu do strukturovaných summary.
Pro každou lekci se kombinují tři zdroje: **transcript** (Zoom), **repo** (kód), **Discord** (komunita).

---

## Obsah
1. [Požadavky a instalace](#1-požadavky-a-instalace)
2. [Stažení transcriptu ze Zoomu](#2-stažení-transcriptu-ze-zoomu)
3. [Analýza repo kurzu](#3-analýza-repo-kurzu)
4. [Prezentace](#4-prezentace)
5. [Discord — stažení a přiřazení k lekcím](#5-discord--stažení-a-přiřazení-k-lekcím)
6. [Zpracování lekce — kompletní postup](#6-zpracování-lekce--kompletní-postup)
7. [Slash commands přehled](#7-slash-commands-přehled)
8. [Struktura projektu](#8-struktura-projektu)
9. [Pre-check souborů](#9-pre-check-souborů)

---

## 1. Požadavky a instalace

Projekt používá [uv](https://docs.astral.sh/uv/) pro správu závislostí.

```bash
uv sync
```

Vytvoř soubor `.env` v kořeni projektu:

```
DISCORD_TOKEN=tvuj_discord_token
```

> Token získáš z Discord klienta: DevTools → Network → libovolný API request → hlavička `Authorization`.
> Do `.env` vlož hodnotu **bez** prefixu `Bot ` (jde o user token).

---

## 2. Stažení transcriptu ze Zoomu

### Jak exportovat z Zoom

1. Přihlaš se na [zoom.us](https://zoom.us) → **Recordings**
2. Otevři záznam → klikni **...** → **Download** → stáhni soubor s příponou `.transcript` nebo`.json`
   - Hledáš soubor s klíčem `result.transcriptList` uvnitř (Zoom Cloud Recording Transcript)
3. Ulož do `transcripts/lekce-XX.json`

### Parsování transcriptu

```bash
uv run python scripts/parse_transcript.py transcripts/lekce-03.json
```

Výstup jde na stdout — přesměruj ho nebo nech Claude číst přímo přes slash command.

Parsovaný výstup se automaticky cachuje do `transcripts/parsed/lekce-XX.txt` — při opakovaném spuštění `/zpracuj-lekci` se znovu neparsuje.

Skript automaticky:
- rozpozná hlavního řečníka
- opraví garblované termíny (SDK, MCP, CLI, LLM…)
- vypíše metadata (délka, řečníci, počet položek)

---

## 3. Analýza repo kurzu

Repo kurzu je naklonované lokálně — Claude ho **nikdy nečte přímo**, ale vytváří předgenerované summary.

### Jednou na začátku (nebo při větší změně v repo)

Spusť v Claude Code:

```
/analyzuj-repo /absolutni/cesta/k/repo-kurzu
```

Příklad:

```
/analyzuj-repo /home/michal/Projects/VibeCodingCourse
```

Výstup se uloží do `repo-summary/lekce-XX-repo.md` pro každou lekci zvlášť.

**Pojmenování složek v repo je flexibilní** — složky mohou být pojmenované libovolně (`1_LLM/`, `1-llm-intro/`, `01_basics/` apod.). Claude je detekuje automaticky podle číselného prefixu — stačí zadat pouze cestu k repo.

Chceš zpracovat jen jednu konkrétní lekci:

```
/analyzuj-repo /absolutni/cesta/k/repo-kurzu 4
```

### Jak zpracování funguje

- **Jedna lekce** — Claude najde složku s odpovídajícím číselným prefixem a zpracuje ji přímo.
- **Všechny lekce** — Claude spustí pro každou složku samostatný subagent paralelně (`claude --print`), čímž výrazně zkrátí dobu zpracování.

### Mapa čísel → lekce

Složky v repo jsou detekovány automaticky podle číselného prefixu. Orientační témata:

| Číslo | Lekce |
|-------|-------|
| 1 | Základy LLM, API |
| 2 | Codex manuálně |
| 3 | Codex SDK |
| 4 | Claude Code |
| 5 | Claude Agent SDK |
| 6 | Ostatní agenti |
| 7 | Office suite |
| 8 | Praktické kódování |

---

## 4. Prezentace

Prezentace jsou volitelný analytický zdroj (detekce kapitol, oprava termínů). Vlož do `presentations/`:

| Formát | Akce |
|--------|------|
| `lekce-XX.pdf` | Nic — Claude čte nativně |
| `lekce-XX.html` | Nic — Claude čte jako text |
| `lekce-XX.pptx` | Spusť parsování (viz níže) |

### Parsování PPTX

```bash
uv run python scripts/parse_presentation.py presentations/lekce-03.pptx
```

Výstup je plain text se slide tituly — Claude ho pak použije při analýze.

---

## 5. Discord — stažení a přiřazení k lekcím

### 5a. Nastavení kanálů

Uprav `discord-channel/channels.json` — seznam kanálů ke stažení:

```json
[
  {
    "id": "1234567890123456789",
    "name": "obecna-diskuze",
    "description": "Obecná diskuze"
  },
  {
    "id": "9876543210987654321",
    "name": "hot-news",
    "description": "Novinky a linky"
  }
]
```

Channel ID najdeš v Discordu: pravý klik na kanál → **Copy Channel ID** (nutno mít zapnutý Developer Mode).

### 5b. Stažení zpráv z Discordu

```bash
uv run python scripts/fetch_discord.py
```

Výstup: `discord-channel/export/{channel-name}.json`

### 5c. Přiřazení zpráv k lekcím

```bash
uv run python scripts/assign_discord.py discord-channel/export lekce-datumy.json
```

Výstup: `discord-parsed/lekce-XX-{channel}.json`

Soubor `lekce-datumy.json` obsahuje datum konání každé lekce:

```json
{
  "lekce-01": "2026-04-09",
  "lekce-02": "2026-04-14"
}
```

### 5d. Celý Discord workflow jedním příkazem

```
/rozpadni-discord
```

---

## 6. Zpracování lekce — kompletní postup

### Co musíš mít připraveno před zpracováním lekce XX

| Soubor / akce | Povinné? |
|---------------|----------|
| `transcripts/lekce-XX.json` | Ano |
| `repo-summary/lekce-XX-repo.md` | Ano (viz krok 3) |
| `discord-parsed/lekce-XX-*.json` | Doporučeno |
| `presentations/lekce-XX.*` | Volitelné |

> Nejsi si jistý, jestli máš všechny soubory? Spusť:
> ```bash
> uv run python scripts/check_lekce.py 5
> ```

### Krok 1 — Zpracuj lekci (průchod 1: identifikace nejasností)

```
/zpracuj-lekci 3
```

Vytvoří `output/summaries/lekce-03-review-nejasnosti.md` s:
- tabulkou rozpoznaných garblovaných termínů
- nejasnostmi k doplnění (s přesným časem a kontextem)
- prioritizovanou tabulkou akcí

### Krok 2 — Doplň nejasnosti

Projdi video na označených časech a doplň správné termíny nebo kontext.

### Krok 3 — Vygeneruj finální summary (průchod 2)

```
/dopln-nejasnosti lekce-03
```

Nebo — pokud nechceš čekat na manuální doplnění:

```
/zpracuj-lekci 3
```

a nejasnosti se doplní automaticky jako `[???]`.

Výsledek: `output/summaries/lekce-03-summary.md`

### Zpracování všech lekcí najednou

```
/zpracuj-vse
```

---

## 7. Slash commands přehled

| Příkaz | Popis |
|--------|-------|
| `/analyzuj-repo <cesta>` | Vygeneruje `repo-summary/` pro všechny lekce |
| `/zpracuj-lekci <číslo>` | Průchod 1 — identifikace nejasností pro jednu lekci |
| `/dopln-nejasnosti <lekce>` | Průchod 2 — finální summary po doplnění nejasností |
| `/zpracuj-vse` | Zpracuje všechny dostupné transkripty |
| `/vytvor-index` | Vygeneruje `output/index.md` přes všechny lekce |
| `/rozpadni-discord` | Stáhne Discord a přiřadí zprávy k lekcím |

### Pomocné skripty

| Příkaz | Popis |
|--------|-------|
| `uv run python scripts/check_lekce.py [N]` | Ověří stav souborů pro lekci N (nebo všechny 1–8) |

---

## 8. Struktura projektu

```
VibeCondingTranscript/
├── .env                          # DISCORD_TOKEN (gitignorováno)
├── lekce-datumy.json             # Datum konání každé lekce
├── scripts/
│   ├── parse_transcript.py       # Zoom JSON → čistý přepis
│   ├── fetch_discord.py          # Stáhne zprávy z Discord API
│   ├── assign_discord.py         # Přiřadí zprávy k lekcím
│   ├── parse_presentation.py     # PPTX → plain text
│   └── check_lekce.py            # Pre-check souborů před zpracováním
├── transcripts/                  # Zoom JSON exporty (gitignorováno)
│   └── parsed/                   # Cachované čisté přepisy (gitignorováno)
├── presentations/                # PDF/PPTX/HTML prezentace (gitignorováno)
├── discord-channel/
│   ├── channels.json             # Seznam kanálů ke stažení
│   └── export/                   # Stažená data (gitignorováno)
├── discord-parsed/               # Zprávy přiřazené k lekcím
├── repo-summary/                 # Generováno přes /analyzuj-repo
│   ├── lekce-01-repo.md
│   └── ...
└── output/
    ├── index.md
    ├── all-tools.md
    └── summaries/
        ├── lekce-03-review-nejasnosti.md
        └── lekce-03-summary.md
```

---

## 9. Pre-check souborů

Před spuštěním `/zpracuj-lekci` ověř, že jsou dostupné všechny potřebné soubory:

```bash
uv run python scripts/check_lekce.py 5
```

Výstup ukáže stav každého souboru:

```
Lekce 05 (2026-04-23):
  transcripts/     ⚠  transcript5.json  → lekce-05.json [přejmenovat? y/N]
  presentations/   ✗  nenalezeno
  discord-parsed/  ✓  lekce-05-dotazy-pri-lekci.json (36 zpráv)
  repo-summary/    ✓  lekce-05-repo.md
  output/summary   ✓  lekce-05-summary.md (hotovo)
```

Skript nabídne přejmenování souborů s nesprávným názvem (např. `transcript5.json` → `lekce-05.json`).

Bez argumentu zkontroluje všechny lekce 1–8:

```bash
uv run python scripts/check_lekce.py
```
