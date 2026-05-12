# Rozpadni Discord kanály do lekcí

Stáhne Discord kanály přes API a rozpadne zprávy do lekcí.
Spouštěj při prvním nastavení nebo po přidání nových zpráv.

## Použití
`/rozpadni-discord`

## Prerekvizity

Nastav token před spuštěním:
```bash
export DISCORD_TOKEN="tvuj_token"
```

Kanály jsou nakonfigurované v `discord_channel/channels.json`.

## Postup

### 1. Stáhni zprávy z Discord API

```bash
python scripts/fetch_discord.py
```

Výstup: `discord_channel/export/{channel}.json` pro každý kanál.

### 2. Rozpadni podle lekcí

```bash
python scripts/assign_discord.py discord_channel/export lekce-datumy.json
```

Výstup: `discord-parsed/lekce-XX-{channel}.json`

## Na konci vypiš

- Seznam zpracovaných kanálů
- Počet zpráv celkem a rozpad po lekcích
- Kanály/lekce bez zpráv (přeskočeny)
