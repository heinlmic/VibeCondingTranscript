# Doplň nejasnosti a vygeneruj finální summary

Tento příkaz se spouští po tom, co uživatel doplnil nejasné termíny v review souboru.

## Použití
`/dopln-nejasnosti $ARGUMENTS`
kde `$ARGUMENTS` je název lekce, např. `lekce-03`

## Postup

1. Přečti `output/summaries/$ARGUMENTS-review-nejasnosti.md`
2. Najdi všechny doplněné termíny (pole "Doplň:" již není prázdné)
3. Aktualizuj `output/summaries/$ARGUMENTS-summary.md`:
   - Nahraď všechny `[???]` správnými termíny
   - Uprav kapitoly pokud nový termín mění pochopení tématu
   - Aktualizuj sekci "Nástroje a repa" o nově identifikované nástroje
4. Aktualizuj `output/all-tools.md` o případné nové nástroje
5. Vypiš co bylo změněno
