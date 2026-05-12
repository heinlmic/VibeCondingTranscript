# Rozpadni Discord kanály do lekcí

Stáhne Discord kanály přes API a rozpadne zprávy do lekcí.
Spouštěj při prvním nastavení nebo po přidání nových zpráv.

## Použití
`/rozpadni-discord`

## Prerekvizity

Token je uložen v `.env` v kořeni projektu:
```
DISCORD_TOKEN=...
```

Skripty načítají `.env` automaticky přes `python-dotenv`. Kanály jsou nakonfigurované v `discord-channel/channels.json`.

## Postup

### 1. Stáhni zprávy z Discord API

```bash
python scripts/fetch_discord.py
```

Výstup: `discord-channel/export/{channel}.json` pro každý kanál.

### 2. Rozpadni podle lekcí

```bash
python scripts/assign_discord.py discord-channel/export lekce-datumy.json
```

Výstup: `discord-parsed/lekce-XX-{channel}.json`

## Na konci vypiš

- Seznam zpracovaných kanálů
- Počet zpráv celkem a rozpad po lekcích
- Kanály/lekce bez zpráv (přeskočeny)
