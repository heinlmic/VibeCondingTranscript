# Vytvoř index lekcí

## Použití
`/vytvor-index`

Vytvoří nebo aktualizuje `output/index.md` — přehled všech lekcí a stavu zpracování.

## Krok 1 — Zjisti dostupné lekce

Prohledej:
- `transcripts/` — existující transcript soubory (`lekce-XX.*`)
- `output/summaries/` — hotové summary (`lekce-XX-summary.md`) a review soubory (`lekce-XX-review-nejasnosti.md`)
- `repo-summary/` — dostupné repo summaries (`lekce-XX-repo.md`)
- `discord-parsed/` — dostupná Discord data (`lekce-XX-*.json`)
- `presentations/` — dostupné prezentace (`lekce-XX.*`)

## Krok 2 — Zjisti metadata hotových lekcí

Pro každou lekci, která má hotové `output/summaries/lekce-XX-summary.md`, přečti hlavičku souboru a vytáhni:
- Datum lekce
- Délku lekce
- Téma (název za pomlčkou v `# Lekce XX — [Název]`)

## Krok 3 — Vytvoř output/index.md

Formát:

```markdown
# Index lekcí — Vibe Coding Course

> Aktualizováno: YYYY-MM-DD

## Přehled lekcí

| # | Téma | Datum | Délka | Transcript | Repo | Discord | Prezentace | Summary |
|---|------|-------|-------|------------|------|---------|------------|---------|
| 1 | Základy LLM | ... | ... | ✓/— | ✓/— | ✓/— | ✓/— | [summary](summaries/lekce-01-summary.md) / ✗ |

## Stav zpracování

- **Hotové summary:** X lekcí
- **Zbývá zpracovat:** seznam lekcí bez summary
- **Chybí zdroje:** seznam lekcí kde chybí transcript / repo-summary / discord

## Nástroje napříč lekcemi

(vložit obsah output/all-tools.md pokud existuje)
```

Symboly: `✓` = existuje, `—` = chybí.

## Na konci vypiš
- Celkový počet lekcí
- Počet hotových summary
- Co ještě chybí
