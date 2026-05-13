# Plán vylepšení — VibeCondingTranscript

## Kontext

Při zpracování lekce 5 se ukázaly opakující se problémy:
- Transcript soubory mají jiné jméno než workflow očekává (`transcript5.json` vs `lekce-05.json`) → manuální lookup při každém spuštění
- 252KB transcript se vždy znovu parsuje, i při opakovaném zpracování
- CLAUDE.md (228 řádků) se načítá do každé konverzace, ačkoli velká část obsahu (slovník glosáře, output šablona) se potřebuje jen při konkrétním kroku
- Discord JSON obsahuje redundantní pole `date` (derivovatelné z `datetime`)
- Neexistuje pre-check utilita, která by ověřila stav souborů před zpracováním

---

## Změny ke implementaci

### A. Nový skript `scripts/check_lekce.py`

**Účel:** Standalone utilita spustitelná před `/zpracuj-lekci`. Ověří dostupnost a správné pojmenování všech zdrojových souborů pro danou lekci.

**Vstup:** `python scripts/check_lekce.py [číslo_lekce]` — bez argumentu zkontroluje všechny lekce 1–8.

**Co kontroluje (per lekce):**
1. `transcripts/` — hledá `lekce-XX.json`; pokud nenajde, zkusí `transcript{N}.json` a reportuje jako ⚠
2. `presentations/` — hledá `lekce-XX.(pdf|pptx|html)` (adresář nemusí existovat)
3. `discord-parsed/` — hledá `lekce-XX-*.json` (přejmenování není potřeba, konvence je správná)
4. `repo-summary/` — hledá `lekce-XX-repo.md`
5. `output/summaries/` — hledá `lekce-XX-summary.md` (stav zpracování)
6. Datum lekce z `lekce-datumy.json`

**Výstupní formát:**
```
Lekce 05 (2026-04-23):
  transcripts/     ⚠  transcript5.json  → lekce-05.json [přejmenovat? y/N]
  presentations/   ✗  nenalezeno
  discord-parsed/  ✓  lekce-05-dotazy-pri-lekci.json (36 zpráv)
  repo-summary/    ✓  lekce-05-repo.md
  output/summary   ✓  lekce-05-summary.md (hotovo)
```

**Přejmenování:** Interaktivní potvrzení pro každý soubor s neshodou. Přejmenuje pouze soubory v `transcripts/` a `presentations/` (ostatní jsou OK). Po přejmenování vypíše souhrn.

**Soubory ke změně:**
- `scripts/check_lekce.py` — nový soubor
- `CLAUDE.md` — přidat do sekce "Struktura projektu"
- `.claude/commands/zpracuj-lekci.md` — v Krok 0 přidat zmínku: "pokud soubor nenalezen, navrhni `uv run python scripts/check_lekce.py {N}`"

---

### B. Transcript caching

**Účel:** Parsovaný transcript (252KB → čistý text) ukládat persistentně, neopakovat parsování při re-zpracování lekce.

**Jak:**
- Po úspěšném parsování uložit výstup do `transcripts/parsed/lekce-XX.txt`
- V `zpracuj-lekci.md` Krok 2: nejdřív zkontroluj `transcripts/parsed/lekce-XX.txt`; pokud existuje, načti přímo; pokud ne, spusť parse a ulož

**Soubory ke změně:**
- `.claude/commands/zpracuj-lekci.md` — Krok 2 rozšířit o cache check
- `.gitignore` — přidat `transcripts/parsed/`
- `CLAUDE.md` — přidat `transcripts/parsed/` do struktury projektu

**Bash příkaz pro uložení:**
```bash
python scripts/parse_transcript.py transcripts/lekce-XX.json > transcripts/parsed/lekce-XX.txt
```

---

### C. Discord JSON — odstranění redundantního pole `date`

**Problém:** Každá zpráva má 5 polí: `author`, `datetime`, `date`, `text`, `links`. Pole `date` je redundantní — jde o `datetime[:10]`. Pole `links` zůstane (potřebné pro analýzu).

**Změny v `assign_discord.py`:**

V `normalize_message()` — odstranit řádek `"date": ts[:10] if ts else ""`:
```python
def normalize_message(msg: dict) -> dict:
    ts = msg.get("timestamp", "")
    return {
        "author":   msg.get("author", "?"),
        "datetime": ts,
        # date odstraněno — redundantní s datetime
        "text":     msg.get("content", ""),
        "links":    msg.get("links", []),
    }
```

V `assign_by_dates()` — opravit čtení date z msg:
```python
# bylo: msg_date = date.fromisoformat(msg["date"])
msg_date = date.fromisoformat(msg["datetime"][:10])
```

**Poznámka:** Existující soubory v `discord-parsed/` stále mají `date` pole — po změně skriptu nové soubory pole nebudou mít. Starší soubory lze sjednotit spuštěním `assign_discord.py` znovu.

**Soubory ke změně:**
- `scripts/assign_discord.py` — 2 řádky

---

### D. CLAUDE.md — extrakce glosáře a output formátu

**Problém:** CLAUDE.md (228 řádků) se načítá do každé konverzace. Obsahuje sekce, které jsou relevantní jen při konkrétním kroku:
- Slovník garblovaných vzorů (řádky 148–179, 31 řádků) — potřebný jen při Průchodu 1
- Output formát summary (řádky 191–216, 26 řádků) — potřebný jen při Průchodu 2

**Jak:**
1. Přesunout slovník do `.claude/glossary.md`
2. Přesunout output formát do `.claude/output-format.md`
3. V CLAUDE.md nahradit každou sekci jedním odkazem: "Slovník: viz `.claude/glossary.md`"
4. V `zpracuj-lekci.md`:
   - Krok 4 (Průchod 1): přidat "Načti `.claude/glossary.md` pro slovník garblovaných vzorů"
   - Krok 5 (Průchod 2): přidat "Načti `.claude/output-format.md` pro formát summary"

**Úspora:** ~57 řádků z CLAUDE.md → ~2 800 tokenů ušetřeno každou konverzaci.

**Soubory ke změně:**
- `.claude/CLAUDE.md` — odstranit 2 sekce, nahradit odkazy
- `.claude/glossary.md` — nový soubor
- `.claude/output-format.md` — nový soubor
- `.claude/commands/zpracuj-lekci.md` — přidat Read instrukce v Krocích 4 a 5

---

### E. Auto-detect zpracovaných lekcí v `zpracuj-lekci.md`

**Přidat do Kroku 0** (po resolve čísla lekce):
"Zkontroluj jestli `output/summaries/lekce-XX-summary.md` existuje. Pokud ano, vypiš upozornění a čekej na potvrzení před přepsáním."

**Soubory ke změně:**
- `.claude/commands/zpracuj-lekci.md` — 3 řádky do Kroku 0

---

## Pořadí implementace

1. **`assign_discord.py`** (C, 2 řádky) — nejrychlejší, okamžitá úspora
2. **`check_lekce.py`** (A, nový skript ~80 řádků) — hlavní přínos, odstraní naming problémy
3. **Transcript caching** (B, update `.md` + `.gitignore`) — přínos při re-zpracování
4. **CLAUDE.md split** (D, přesuny + update `.md`) — token úspora per konverzace
5. **Auto-detect** (E, 3 řádky) — bezpečnostní pojistka

## Kritické soubory

| Soubor | Typ změny |
|--------|-----------|
| `scripts/assign_discord.py` | Upravit — 2 řádky |
| `scripts/check_lekce.py` | Nový (~80 řádků) |
| `.claude/commands/zpracuj-lekci.md` | Upravit — Kroky 0, 2, 4, 5 |
| `.claude/CLAUDE.md` | Upravit — odstranit 57 řádků, přidat 2 |
| `.claude/glossary.md` | Nový (přesun z CLAUDE.md) |
| `.claude/output-format.md` | Nový (přesun z CLAUDE.md) |
| `.gitignore` | Upravit — přidat `transcripts/parsed/` |

## Verifikace

1. `python scripts/check_lekce.py 5` — vypíše stav lekce 5, nabídne přejmenování `transcript5.json`
2. Po přejmenování: `/zpracuj-lekci 5` proběhne bez manuálního lookup v Krok 0
3. Při druhém spuštění `/zpracuj-lekci 5`: Krok 2 načte z cache `transcripts/parsed/lekce-05.txt` a Krok 0 zeptá na přepsání
4. `python scripts/assign_discord.py ...` — výstupní JSON neobsahuje pole `date`
5. Token count CLAUDE.md: 228 → ~170 řádků
