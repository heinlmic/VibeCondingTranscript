# Rozpadni Discord kanály do lekcí

Tento příkaz se spouští JEDNOU (nebo při přidání nového Discord souboru).
Projde všechny soubory v `discord/`, každý zparsuje a rozpadne do lekcí.
Výsledky uloží do `discord-parsed/` jako jednotlivé JSON soubory.

## Použití
`/rozpadni-discord`

## Postup

1. Přečti skills:
   - `.claude/skills/discord-parser/SKILL.md` → ulož `/tmp/parse_discord.py`
   - `.claude/skills/discord-assign/SKILL.md` → ulož `/tmp/assign_discord.py`

2. Přečti `lekce-datumy.json`

3. Pro každý `.txt` soubor v `discord/`:

```bash
python /tmp/parse_discord.py discord/<soubor>.txt > /tmp/discord_raw.json
python /tmp/assign_discord.py /tmp/discord_raw.json <soubor>.txt lekce-datumy.json > /tmp/discord_assigned.json
```

4. Z výsledku rozbal každou lekci do samostatného souboru:
   - `discord-parsed/lekce-01-<název-kanálu>.json`
   - `discord-parsed/lekce-02-<název-kanálu>.json`
   - atd.

   Název kanálu = název souboru bez přípony a bez čísla lekce pokud bylo v názvu.
   Příklad: `zajimavosti.txt` → `lekce-01-zajimavosti.json`, `lekce-02-zajimavosti.json`...
   Příklad: `lekce03-chat.txt` → pouze `lekce-03-chat.json`

5. Vytvoř `discord-parsed/README.md` s přehledem co bylo vygenerováno.

## Na konci vypiš
- Seznam zpracovaných Discord souborů
- Počet zpráv celkem a rozpad po lekcích
- Soubory kde nebyla žádná zpráva pro danou lekci (přeskočeny)
