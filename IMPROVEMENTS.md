# Plán vylepšení — VibeCondingTranscript

## 1. Prezentace jako analytická pomůcka

**Proč:** Lektor má k většině lekcí prezentaci. Pomůže lépe detekovat kapitoly, opravit garblované termíny a pochopit kontext nejasných pasáží v transcriptu. V summary se neobjeví jako samostatná sekce — slouží jen při analýze.

**Co přidat:**

- Nový adresář `presentations/` — soubory pojmenované `lekce-01.pdf`, `lekce-02.pptx` atd.
- Přidat do `.gitignore` (stejně jako `transcripts/`)
- Podporované formáty:
  - `.pdf` — Claude čte nativně
  - `.html` — Claude čte jako text
  - `.pptx` — potřebuje nový skript `scripts/parse_presentation.py` (python-pptx), výstup = plain text se slide tituly
- V summary pouze v hlavičce přibude: `Prezentace: ano` (pokud soubor existuje)

**Změny v souborech:**

| Soubor | Co změnit |
|--------|-----------|
| `CLAUDE.md` | Přidat `presentations/` do struktury projektu; popsat jako volitelný analytický zdroj; uvést formáty a jak je číst |
| `.claude/commands/zpracuj-lekci.md` | Přidat krok před Průchod 1: hledej `presentations/lekce-XX.*`, pokud existuje načti před analýzou; použij pro lepší detekci kapitol a termínů |
| `CLAUDE.md` (output formát) | V hlavičce summary přidat volitelné pole `Prezentace:` |
| `.gitignore` | Přidat řádek `presentations/` |
| `scripts/parse_presentation.py` | Nový skript: vstup = `.pptx`, výstup = plain text (tituly snímků + obsah) |

---

## 2. Zjednodušení sekce "Kód z repozitáře" v summary

**Proč:** Detailní popis kódu je už v `repo-summary/lekce-XX-repo.md`. V summary stačí jen reference na relevantní soubory — duplikovat obsah nedává smysl.

**Jak:**
- Sekci přejmenovat na `## Relevantní soubory v repo`
- Formát: pouze seznam souborů s jednořádkovým popisem (max 2–3 položky, jen pokud jsou extra relevantní)
- Pokud není co zvláštního zdůraznit, sekci vynechat

**Změny v souborech:**

| Soubor | Co změnit |
|--------|-----------|
| `CLAUDE.md` (output formát) | Přejmenovat `## Kód z repozitáře` → `## Relevantní soubory v repo`; zkrátit instrukci |
| `.claude/commands/zpracuj-lekci.md` | Upravit Krok 4 — místo popisu kódu jen reference na soubory |

---

## 3. Nový příkaz `/vytvor-index`

**Proč:** Neexistuje žádný přehled přes všechny lekce najednou — kdo přijde po tobě, neví co je hotové a co ne.

**Co vytvoří:** `output/index.md`
- Tabulka všech lekcí: číslo, datum, téma, stav zpracování (summary hotová / chybí)
- Přehled nástrojů z `output/all-tools.md`
- Odkaz na každý summary soubor

**Kde přidat:** Nový soubor `.claude/commands/vytvor-index.md`

---

## Přehled souborů ke změně

| Soubor | Typ |
|--------|-----|
| `CLAUDE.md` | Upravit |
| `.gitignore` | Upravit |
| `.claude/commands/zpracuj-lekci.md` | Upravit |
| `scripts/parse_presentation.py` | Nový |
| `.claude/commands/vytvor-index.md` | Nový |
