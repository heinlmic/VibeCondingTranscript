# Discord Assign

Přiřadí Discord zprávy z API exportu k lekcím.
Vstup: `discord_channel/export/*.json` (výstup `scripts/fetch_discord.py`)
Výstup: `discord-parsed/lekce-XX-{channel}.json`

## Kdy použít
Po `scripts/fetch_discord.py`, před zpracováním lekce — nebo jako součást `/rozpadni-discord`.

## Spuštění

```bash
python scripts/assign_discord.py discord_channel/export lekce-datumy.json
```

## Vstupní formát (API JSON z fetch_discord.py)

```json
{
  "meta": {
    "channel_id": "...",
    "channel_name": "hot-news",
    "exported_at": "2026-05-10T18:00:00",
    "message_count": 142
  },
  "messages": [
    {
      "id": "...",
      "timestamp": "2026-04-09T18:53:00",
      "author": "LukasKellerstein",
      "content": "text zprávy",
      "links": ["https://..."],
      "embeds": [{ "title": "...", "url": "..." }]
    }
  ]
}
```

## Logika přiřazení

- Název souboru obsahuje číslo (`hot-news-3.json`, `lekce03.json`) → vše do té lekce
- Název souboru bez čísla → rozpad podle datumů z `lekce-datumy.json` (každá zpráva jde do lekce, po jejímž datu přišla)

## Výstupní formát

Jeden soubor per lekce per kanál: `discord-parsed/lekce-03-hot-news.json`

```json
[
  {
    "author": "LukasKellerstein",
    "datetime": "2026-04-09T18:53:00",
    "date": "2026-04-09",
    "text": "text zprávy",
    "links": ["https://..."]
  }
]
```

## Použití výsledku

Při zpracování lekce načti `discord-parsed/lekce-XX-*.json` a zahrň do sekce "Z Discordu".
